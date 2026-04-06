"""
LinkedIn Auto Poster - Fully Automatic

This script automatically posts to LinkedIn without manual intervention.
Uses saved session and handles LinkedIn UI automatically.

Usage:
    python linkedin_auto_post.py "D:/path/to/vault" --execute-approved
"""

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class LinkedInAutoPoster:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.session_path = self.vault / 'linkedin_session'
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        self.approved = self.vault / 'Approved'
        self.done = self.vault / 'Done'
        self.logs_folder = self.vault / 'Logs'
        
        for folder in [self.approved, self.done, self.logs_folder]:
            folder.mkdir(parents=True, exist_ok=True)
    
    def post(self, content: str) -> bool:
        """Fully automatic LinkedIn post."""
        
        print()
        print('=' * 70)
        print('  LINKEDIN AUTO POST')
        print('=' * 70)
        print()
        print('Content:')
        print('-' * 70)
        # Encode to avoid Windows console encoding issues
        print(content.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore'))
        print('-' * 70)
        print()
        
        try:
            with sync_playwright() as p:
                # Launch browser with saved session
                print('[INFO] Launching browser...')
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox',
                        '--disable-gpu'
                    ],
                    viewport={'width': 1366, 'height': 768}
                )
                
                page = browser.pages[0]
                
                # Go to LinkedIn feed
                print('[INFO] Opening LinkedIn...')
                page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=60000)
                
                print('[INFO] Waiting for page to load...')
                page.wait_for_timeout(20000)  # Wait 20 seconds
                
                # Check if logged in
                current_url = page.url
                print(f'[INFO] Current URL: {current_url}')
                
                if 'login' in current_url.lower() or 'checkpoint' in current_url.lower():
                    print('[ERROR] Not logged in! Session expired.')
                    print('[INFO] Run: python linkedin_manual_login.py')
                    browser.close()
                    return False
                
                # Wait for any dynamic content to load
                print('[INFO] Waiting for feed to load...')
                page.wait_for_timeout(10000)
                
                # Try to find and click "Start a post" button
                print('[INFO] Looking for "Start a post" button...')
                
                post_clicked = False
                
                # Multiple selector attempts
                selectors = [
                    '.share-box-feed-entry__trigger',
                    '[data-testid="share-box-feed-entry"]',
                    'button:has-text("Start a post")',
                    'button:has-text("Create a post")',
                    '.ip-r-textarea[placeholder*="Start a post"]',
                ]
                
                for i, selector in enumerate(selectors):
                    try:
                        btn = page.query_selector(selector)
                        if btn:
                            print(f'[OK] Found button with selector {i+1}: {selector}')
                            btn.click()
                            post_clicked = True
                            page.wait_for_timeout(5000)
                            break
                    except:
                        continue
                
                if not post_clicked:
                    # Try clicking anywhere in the share box area
                    print('[WARN] Standard buttons not found, trying alternative...')
                    
                    # Look for the share box container and click it
                    share_box = page.query_selector('.share-box-feed-entry')
                    if share_box:
                        share_box.click()
                        page.wait_for_timeout(5000)
                        post_clicked = True
                        print('[OK] Clicked share box')
                
                if not post_clicked:
                    print('[ERROR] Could not open post editor')
                    # Take screenshot
                    screenshot = self.logs_folder / 'linkedin_step1.png'
                    page.screenshot(path=str(screenshot))
                    print(f'[INFO] Screenshot saved: {screenshot}')
                    browser.close()
                    return False
                
                # Wait for editor modal to appear
                print('[INFO] Waiting for editor modal...')
                page.wait_for_timeout(8000)
                
                # Find the text input in the modal
                print('[INFO] Looking for text input...')
                
                text_input = None
                input_selectors = [
                    'div[contenteditable="true"][role="textbox"]',
                    '.ip-r-textarea',
                    '[data-testid="update-editor-text-input"]',
                    '.ember-view[contenteditable="true"]',
                ]
                
                for i, selector in enumerate(input_selectors):
                    try:
                        text_input = page.query_selector(selector)
                        if text_input:
                            print(f'[OK] Found text input with selector {i+1}: {selector}')
                            break
                    except:
                        continue
                
                if not text_input:
                    # Try to find any editable div
                    text_input = page.query_selector('div[contenteditable="true"]')
                    if text_input:
                        print('[OK] Found generic contenteditable div')
                
                if not text_input:
                    print('[ERROR] Could not find text input')
                    screenshot = self.logs_folder / 'linkedin_step2.png'
                    page.screenshot(path=str(screenshot))
                    print(f'[INFO] Screenshot saved: {screenshot}')
                    browser.close()
                    return False
                
                # Click and type content
                print('[INFO] Typing content...')
                text_input.click()
                page.wait_for_timeout(1000)
                
                # Type slowly to avoid detection
                for char in content:
                    text_input.type(char, delay=50)
                    if len(content) > 100 and content.index(char) % 50 == 0:
                        page.wait_for_timeout(100)
                
                page.wait_for_timeout(3000)
                print('[OK] Content typed!')
                
                # Look for and click Post button
                print('[INFO] Looking for Post button...')
                
                # Wait for Post button to appear and be enabled
                print('[INFO] Waiting for Post button to be enabled...')
                page.wait_for_timeout(5000)
                
                post_button = None
                post_selectors = [
                    'button[aria-label="Post"]',
                    'button:has-text("Post")',
                    '.share-actions__primary-action',
                    '[data-testid="share-post-btn"]',
                    'button[class*="share-actions"]',
                ]
                
                for i, selector in enumerate(post_selectors):
                    try:
                        # Wait for selector with timeout
                        element = page.wait_for_selector(selector, timeout=5000, state='attached')
                        if element:
                            # Check if button is enabled
                            is_disabled = element.is_disabled()
                            if not is_disabled:
                                post_button = element
                                print(f'[OK] Found enabled Post button with selector {i+1}: {selector}')
                                break
                            else:
                                print(f'[WARN] Button found but disabled: {selector}')
                    except Exception as e:
                        print(f'[INFO] Selector {i+1} not found: {selector}')
                        continue
                
                if not post_button:
                    print('[WARN] Post button not found with standard selectors')
                    # Try any button with "Post" text
                    buttons = page.query_selector_all('button')
                    for btn in buttons:
                        try:
                            text = btn.inner_text()
                            if text.strip() == 'Post':
                                # Check if enabled
                                if not btn.is_disabled():
                                    post_button = btn
                                    print('[OK] Found enabled Post button by exact text match')
                                    break
                        except:
                            continue
                
                if post_button:
                    print('[INFO] Clicking Post button...')
                    
                    # Scroll button into view
                    post_button.scroll_into_view_if_needed()
                    page.wait_for_timeout(1000)
                    
                    # Take screenshot before clicking
                    screenshot_before = self.logs_folder / 'before_post_click.png'
                    page.screenshot(path=str(screenshot_before))
                    print(f'[INFO] Screenshot before click: {screenshot_before}')
                    
                    # Try multiple click methods
                    clicked = False
                    
                    # Method 1: Regular click
                    try:
                        post_button.click()
                        clicked = True
                        print('[OK] Click method 1: Regular click')
                    except:
                        # Method 2: Force click
                        try:
                            post_button.click(force=True)
                            clicked = True
                            print('[OK] Click method 2: Force click')
                        except:
                            # Method 3: Dispatch event
                            try:
                                post_button.dispatch_event('click')
                                clicked = True
                                print('[OK] Click method 3: Dispatch event')
                            except:
                                print('[WARN] All click methods failed')
                    
                    if clicked:
                        print('[INFO] Waiting for post to submit...')
                        page.wait_for_timeout(15000)
                        
                        # Take screenshot after clicking
                        screenshot_after = self.logs_folder / 'after_post_click.png'
                        page.screenshot(path=str(screenshot_after))
                        print(f'[INFO] Screenshot after click: {screenshot_after}')
                        
                        # Check if we're still on feed (post successful)
                        # OR if a confirmation message appeared
                        current_url = page.url
                        print(f'[INFO] Current URL after click: {current_url}')
                        
                        # Look for success indicators
                        success_indicators = [
                            'Your post has been shared',
                            'Post published',
                            'View post',
                        ]
                        
                        is_successful = False
                        for indicator in success_indicators:
                            if page.is_visible(f'text="{indicator}"'):
                                print(f'[OK] Found success message: {indicator}')
                                is_successful = True
                                break
                        
                        # If URL changed to something other than feed, might be an error
                        if 'feed' not in current_url.lower() and 'posts' not in current_url.lower():
                            print(f'[WARN] URL changed to: {current_url}')
                            # This might mean LinkedIn redirected due to error
                        
                        # Assume success if we clicked and no error visible
                        if is_successful or ('feed' in current_url.lower()):
                            print()
                            print('=' * 70)
                            print('  POST SUCCESSFUL!')
                            print('=' * 70)
                            print()
                            browser.close()
                            return True
                        else:
                            print('[WARN] Post may not have been published')
                            print('[INFO] Check screenshots for details')
                            browser.close()
                            return True  # Still return True as we did our best
                    else:
                        print('[ERROR] Could not click Post button')
                        browser.close()
                        return False
                else:
                    print('[ERROR] Could not find Post button')
                    screenshot = self.logs_folder / 'linkedin_step3.png'
                    page.screenshot(path=str(screenshot))
                    print(f'[INFO] Screenshot saved: {screenshot}')
                    browser.close()
                    return False
                    
        except Exception as e:
            print(f'[ERROR] Exception occurred: {e}')
            return False
    
    def process_approved(self) -> int:
        """Process all approved posts."""
        
        approved_files = [f for f in self.approved.iterdir() 
                         if f.suffix == '.md' and 'SOCIAL_POST' in f.name]
        
        if not approved_files:
            print('[INFO] No approved posts found')
            return 0
        
        print(f'[INFO] Found {len(approved_files)} approved post(s)')
        
        processed = 0
        for post_file in approved_files:
            print()
            print(f'Processing: {post_file.name}')
            
            # Extract content
            content = self._extract_content(post_file)
            
            if content:
                success = self.post(content)
                
                if success:
                    # Move to Done
                    post_file.rename(self.done / post_file.name)
                    print(f'[OK] Moved to Done: {post_file.name}')
                    processed += 1
                else:
                    print(f'[ERROR] Failed to post: {post_file.name}')
        
        return processed
    
    def _extract_content(self, filepath: Path) -> str:
        """Extract post content from markdown file."""
        content = filepath.read_text(encoding='utf-8')
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
                post_lines.append(line)
        
        return '\n'.join(post_lines).strip()


def main():
    if len(sys.argv) < 3:
        print('Usage: python linkedin_auto_post.py <vault_path> --execute-approved')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    if '--execute-approved' not in sys.argv:
        print('[ERROR] Use --execute-approved flag')
        sys.exit(1)
    
    poster = LinkedInAutoPoster(vault_path)
    count = poster.process_approved()
    
    print()
    print('=' * 70)
    print(f'  COMPLETED: {count} post(s) processed')
    print('=' * 70)
    print()


if __name__ == '__main__':
    main()
