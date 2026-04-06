"""
LinkedIn Watcher/Poster for AI Employee (Silver Tier)

Automates LinkedIn posting for business marketing and lead generation.
Uses Playwright for browser automation. Requires human approval before posting.

Usage:
    # Create post draft
    python linkedin_poster.py "D:/path/to/vault" --draft "Your post content here"
    
    # Execute approved posts
    python linkedin_poster.py "D:/path/to/vault" --execute-approved
    
    # Direct post (for testing)
    python linkedin_poster.py "D:/path/to/vault" --post "Content" --headless

Dependencies:
    pip install playwright
    playwright install chromium
"""

import sys
import argparse
import time
from pathlib import Path
from datetime import datetime

# Add scripts folder to path
sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class LinkedInPoster:
    """
    Posts content to LinkedIn using Playwright automation.
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize the LinkedIn poster.
        
        Args:
            vault_path: Path to the Obsidian vault root
        """
        self.vault = Path(vault_path).resolve()
        self.session_path = self.vault / 'linkedin_session'
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        self.pending_approval = self.vault / 'Pending_Approval'
        self.approved = self.vault / 'Approved'
        self.done = self.vault / 'Done'
        
        for folder in [self.pending_approval, self.approved, self.done]:
            folder.mkdir(parents=True, exist_ok=True)
        
        self.logs_folder = self.vault / 'Logs'
        self.logs_folder.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup logging to file."""
        import logging
        log_file = self.logs_folder / f'linkedin_{datetime.now().strftime("%Y-%m-%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('LinkedInPoster')
    
    def create_post_draft(self, content: str, image_path: str = None) -> Path:
        """
        Create a post draft for approval.
        
        Args:
            content: Post content text
            image_path: Optional path to image file
            
        Returns:
            Path to the created draft file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'SOCIAL_POST_{timestamp}_linkedin.md'
        filepath = self.pending_approval / filename
        
        image_info = f'\n- Image: {image_path}' if image_path else ''
        
        content_text = f'''---
type: social_post
platform: linkedin
content_length: {len(content)}
created: {datetime.now().isoformat()}
status: pending_approval
image_path: {image_path if image_path else 'none'}
---

# LinkedIn Post Draft

## Content
{content}
{image_info}

## To Approve
Move this file to `/Approved` folder to schedule for posting.

## To Reject
Move this file to `/Rejected` folder with reason.

---
*Created by LinkedInPoster (Qwen Code AI Employee)*
'''
        
        filepath.write_text(content_text, encoding='utf-8')
        self.logger.info(f'Created post draft: {filename}')
        
        return filepath
    
    def post(self, content: str, image_path: str = None, headless: bool = False) -> bool:
        """
        Post content to LinkedIn.
        
        Args:
            content: Post content text
            image_path: Optional path to image file
            headless: Run browser in headless mode
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info('Starting LinkedIn post...')
        
        try:
            with sync_playwright() as p:
                # Launch browser with persistent context
                self.logger.info('Launching browser...')
                browser = p.chromium.launch_persistent_context(
                    self.session_path,
                    headless=headless,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox'
                    ],
                    viewport={'width': 1280, 'height': 720}
                )
                
                page = browser.pages[0]
                
                # Navigate to LinkedIn
                self.logger.info('Navigating to LinkedIn...')
                page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=60000)
                
                # Wait for page to load
                self.logger.info('Waiting for page to load...')
                page.wait_for_timeout(10000)  # Wait 10 seconds for full load
                
                # Debug: Print current URL
                self.logger.info(f'Current URL: {page.url}')
                
                # Check if logged in
                if 'login' in page.url.lower() or 'checkpoint' in page.url.lower():
                    self.logger.warning('Not logged in. Session may have expired.')
                    self.logger.warning('Please run: python linkedin_manual_login.py')
                    browser.close()
                    return False
                
                # Find and click the post input - try multiple selectors
                self.logger.info('Finding post editor...')
                post_input = None
                
                # UPDATED SELECTORS (March 16, 2026)
                # Based on current LinkedIn UI screenshot analysis
                # Strategy: Click the "Start a post" box first, then find contenteditable div
                
                self.logger.info('Clicking "Start a post" to open composer...')
                
                # First, click the post box to open the modal
                post_box_selectors = [
                    '[class*="share-box-feed-entry__closed-share-box"]',  # ✅ Main post box container
                    '.share-box-feed-entry__trigger',  # Classic trigger
                ]
                
                post_box_clicked = False
                for selector in post_box_selectors:
                    post_box = page.query_selector(selector)
                    if post_box:
                        self.logger.info(f'Found post box with: {selector}')
                        post_box.click()
                        page.wait_for_timeout(3000)  # Wait for modal to open
                        post_box_clicked = True
                        self.logger.info('Post box clicked, modal should be open')
                        break
                
                if post_box_clicked:
                    # Now find the contenteditable div inside the modal
                    self.logger.info('Looking for contenteditable div in modal...')
                    text_input_selectors = [
                        'div[contenteditable="true"]',  # Contenteditable div
                        'div[role="textbox"]',  # Textbox role
                        '[data-testid="update-editor-text-input"]',  # Test ID
                    ]
                    
                    for selector in text_input_selectors:
                        post_input = page.query_selector(selector)
                        if post_input:
                            self.logger.info(f'Found text input with: {selector}')
                            break
                    self.logger.info('Post editor found, typing content...')
                    post_input.click()
                    page.wait_for_timeout(1000)

                    # Type the content (using type instead of fill for contenteditable)
                    self.logger.info('Typing content...')
                    post_input.press('Control+a')  # Select all
                    page.wait_for_timeout(200)
                    post_input.press('Delete')  # Clear
                    page.wait_for_timeout(200)
                    post_input.type(content)  # Type new content
                    page.wait_for_timeout(2000)

                    # Add image if provided
                    if image_path:
                        self.logger.info(f'Uploading image: {image_path}')
                        media_button = page.query_selector('[aria-label*="photo"]') or \
                                      page.query_selector('[aria-label*="media"]')

                        if media_button:
                            media_button.click()
                            page.wait_for_timeout(2000)
                            page.set_input_files('input[type="file"]', image_path)
                            page.wait_for_timeout(3000)

                    # Click post button - UPDATED SELECTORS
                    self.logger.info('Clicking Post button...')
                    
                    # Wait for Post button to be enabled
                    page.wait_for_timeout(3000)
                    
                    # Try multiple Post button selectors
                    post_button_selectors = [
                        'button[aria-label="Post"]',
                        'button:has-text("Post")',
                        'button.artdeco-button--primary:has-text("Post")',
                        '[class*="share-box__update-control"]'
                    ]
                    
                    post_button = None
                    for selector in post_button_selectors:
                        try:
                            post_button = page.query_selector(selector)
                            if post_button:
                                self.logger.info(f'Found Post button with: {selector}')
                                break
                        except:
                            continue
                    
                    if post_button:
                        self.logger.info('Post button found, clicking...')
                        post_button.click()
                        page.wait_for_timeout(8000)  # Wait 8 seconds for post to submit
                        
                        # Verify post was submitted
                        self.logger.info('Post submitted! Checking status...')
                        page.wait_for_timeout(3000)
                        
                        self.logger.info('Post submitted successfully!')
                        browser.close()
                        return True
                    else:
                        self.logger.error('Could not find Post button')
                        # Take screenshot for debugging
                        screenshot_path = self.logs_folder / 'linkedin_error.png'
                        page.screenshot(path=str(screenshot_path))
                        self.logger.info(f'Screenshot saved: {screenshot_path}')
                        browser.close()
                        return False
                else:
                    self.logger.error('Could not find post editor')
                    self.logger.error(f'Page URL: {page.url}')
                    # Take screenshot for debugging
                    screenshot_path = self.logs_folder / 'linkedin_error.png'
                    page.screenshot(path=str(screenshot_path))
                    self.logger.info(f'Screenshot saved: {screenshot_path}')
                    browser.close()
                    return False
                    
        except Exception as e:
            self.logger.error(f'Error posting to LinkedIn: {e}')
            return False
    
    def process_approved_posts(self, headless: bool = False) -> int:
        """
        Process all approved post files.
        
        Args:
            headless: Run browser in headless mode
            
        Returns:
            Number of posts processed
        """
        processed = 0
        
        approved_files = [f for f in self.approved.iterdir() 
                         if f.suffix == '.md' and 'SOCIAL_POST' in f.name]
        
        if not approved_files:
            self.logger.info('No approved posts to process')
            return 0
        
        self.logger.info(f'Found {len(approved_files)} approved post(s)')
        
        for approval_file in approved_files:
            content = self._parse_post_content(approval_file)
            image_path = self._parse_image_path(approval_file)
            
            if content:
                self.logger.info(f'Processing: {approval_file.name}')
                success = self.post(content, image_path, headless)
                
                if success:
                    # Move to Done
                    approval_file.rename(self.done / approval_file.name)
                    self.logger.info(f'Posted and moved to Done: {approval_file.name}')
                    processed += 1
                else:
                    self.logger.error(f'Failed to post: {approval_file.name}')
        
        return processed
    
    def _parse_post_content(self, filepath: Path) -> str:
        """Extract post content from approval file."""
        content = filepath.read_text(encoding='utf-8')
        
        # Find content section
        lines = content.split('\n')
        in_content = False
        post_lines = []
        
        for line in lines:
            if line.strip() == '## Content':
                in_content = True
                continue
            if in_content:
                if line.startswith('##') or line.startswith('---'):
                    break
                if line.strip() and not line.startswith('- Image:'):
                    post_lines.append(line)
        
        return '\n'.join(post_lines).strip()
    
    def _parse_image_path(self, filepath: Path) -> str:
        """Extract image path from approval file."""
        content = filepath.read_text(encoding='utf-8')
        
        for line in content.split('\n'):
            if line.startswith('- Image:') and line != '- Image: none':
                return line.replace('- Image:', '').strip()
        
        return None


def main():
    """Main entry point for the LinkedIn poster."""
    parser = argparse.ArgumentParser(
        description='LinkedIn Poster for AI Employee',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    # Create a post draft for approval
    python linkedin_poster.py "../AI_Employee_Vault" --draft "Excited to announce our new service!"
    
    # Execute all approved posts
    python linkedin_poster.py "../AI_Employee_Vault" --execute-approved
    
    # Direct post (testing only)
    python linkedin_poster.py "../AI_Employee_Vault" --post "Test post" --headless
        '''
    )
    parser.add_argument(
        'vault_path',
        type=str,
        help='Path to the Obsidian vault root'
    )
    parser.add_argument(
        '--draft',
        type=str,
        help='Create a post draft for approval'
    )
    parser.add_argument(
        '--post',
        type=str,
        help='Post content directly (for testing)'
    )
    parser.add_argument(
        '--execute-approved',
        action='store_true',
        help='Execute all approved posts'
    )
    parser.add_argument(
        '--image',
        type=str,
        help='Path to image file'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )
    
    args = parser.parse_args()
    
    vault_path = Path(args.vault_path).resolve()
    
    if not vault_path.exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    poster = LinkedInPoster(str(vault_path))
    
    if args.draft:
        # Create draft for approval
        draft_file = poster.create_post_draft(args.draft, args.image)
        print(f'[OK] Post draft created: {draft_file}')
        print('[INFO] Move the file to /Approved folder to post')
        
    elif args.execute_approved:
        # Execute approved posts
        print('[INFO] Processing approved posts...')
        count = poster.process_approved_posts(args.headless)
        print(f'[OK] Processed {count} post(s)')
        
    elif args.post:
        # Direct post (testing)
        print('[WARN] Direct posting - for testing only!')
        success = poster.post(args.post, args.image, args.headless)
        if success:
            print('[OK] Posted successfully!')
        else:
            print('[ERROR] Failed to post')
            sys.exit(1)
        
    else:
        parser.print_help()
        print()
        print('[INFO] Use --draft to create a post for approval')
        print('[INFO] Use --execute-approved to post approved content')


if __name__ == '__main__':
    main()
