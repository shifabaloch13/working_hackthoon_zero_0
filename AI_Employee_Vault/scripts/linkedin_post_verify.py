"""
LinkedIn Auto Poster - With Manual Verification

Posts automatically but keeps browser open so you can verify the post was published.

Usage:
    python linkedin_post_verify.py "D:/path/to/vault" --execute-approved
"""

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


class LinkedInPostVerifier:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.session_path = self.vault / 'linkedin_session'
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        self.approved = self.vault / 'Approved'
        self.done = self.vault / 'Done'
        self.logs_folder = self.vault / 'Logs'
    
    def post_and_verify(self, content: str) -> bool:
        """Post to LinkedIn and keep browser open for verification."""
        
        print()
        print('=' * 70)
        print('  LINKEDIN POST - WITH VERIFICATION')
        print('=' * 70)
        print()
        print('Content to post:')
        print('-' * 70)
        # Print without emojis to avoid encoding issues
        safe_content = content.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        print(safe_content)
        print('-' * 70)
        print()
        
        try:
            with sync_playwright() as p:
                # Launch browser - KEEP IT OPEN
                print('[INFO] Launching browser...')
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,  # MUST be visible
                    args=[
                        '--disable-blink-features=AutomationControlled',
                    ],
                    viewport={'width': 1366, 'height': 768}
                )
                
                page = browser.pages[0]
                
                # Go to LinkedIn
                print('[INFO] Opening LinkedIn...')
                page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=60000)
                page.wait_for_timeout(10000)
                
                if 'login' in page.url.lower():
                    print('[ERROR] Not logged in!')
                    print('[INFO] Please log in manually in the browser')
                    print('[INFO] Script will wait 2 minutes...')
                    
                    # Wait for manual login
                    for i in range(60):
                        time.sleep(2)
                        if 'feed' in page.url.lower():
                            print('[OK] Login detected!')
                            break
                    else:
                        print('[ERROR] Login timeout')
                        browser.close()
                        return False
                
                # Click "Start a post"
                print('[INFO] Finding "Start a post" button...')
                post_btn = page.query_selector('button:has-text("Start a post")')
                
                if post_btn:
                    post_btn.click()
                    page.wait_for_timeout(5000)
                    print('[OK] Post editor opened')
                else:
                    print('[ERROR] Could not find "Start a post" button')
                    print('[INFO] Please click it manually in the browser')
                
                # Wait for editor
                page.wait_for_timeout(5000)
                
                # Type content
                print('[INFO] Typing content...')
                text_input = page.query_selector('div[contenteditable="true"][role="textbox"]')
                
                if text_input:
                    text_input.click()
                    page.wait_for_timeout(500)
                    
                    # Type content character by character (more human-like)
                    for char in safe_content:
                        text_input.type(char, delay=30 + (hash(char) % 50))
                        if len(safe_content) > 50 and safe_content.index(char) % 30 == 0:
                            page.wait_for_timeout(100)
                    
                    page.wait_for_timeout(3000)
                    print('[OK] Content typed!')
                else:
                    print('[ERROR] Could not find text input')
                    print('[INFO] Please type manually in the browser')
                
                # Find and highlight Post button
                print()
                print('=' * 70)
                print('  MANUAL VERIFICATION REQUIRED')
                print('=' * 70)
                print()
                print('The script has typed the content.')
                print()
                print('In the browser window:')
                print('  1. Review the content')
                print('  2. Click the "Post" button YOURSELF')
                print('  3. Wait for "Your post has been shared" message')
                print('  4. The script will detect when post is published')
                print()
                print('Waiting for you to click Post... (2 minutes timeout)')
                print()
                
                # Wait for user to click Post and for success message
                for i in range(60):
                    time.sleep(2)
                    
                    # Check for success message
                    success_messages = [
                        'Your post has been shared',
                        'Post published',
                        'View post',
                    ]
                    
                    for msg in success_messages:
                        try:
                            if page.is_visible(f'text="{msg}"'):
                                print()
                                print('=' * 70)
                                print('  POST DETECTED!')
                                print('=' * 70)
                                print()
                                print(f'[OK] Found success message: "{msg}"')
                                print()
                                print('[INFO] Waiting 5 seconds then closing browser...')
                                time.sleep(5)
                                browser.close()
                                return True
                        except:
                            pass
                    
                    # Show progress
                    if (i + 1) % 10 == 0:
                        print(f'[INFO] Still waiting... ({(i+1)*2}/120 seconds)')
                
                print()
                print('=' * 70)
                print('  TIMEOUT - Post not detected')
                print('=' * 70)
                print()
                print('The script waited 2 minutes but did not detect a successful post.')
                print()
                print('Possible issues:')
                print('  - You didn\'t click the Post button')
                print('  - LinkedIn didn\'t show success message')
                print('  - Post failed to publish')
                print()
                print('Browser will stay open. Close it manually when done.')
                print()
                
                # Don't close browser - let user verify
                return False
                    
        except Exception as e:
            print(f'[ERROR] Exception: {e}')
            return False
    
    def process_approved(self) -> int:
        """Process approved posts."""
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
            
            content = self._extract_content(post_file)
            
            if content:
                success = self.post_and_verify(content)
                
                if success:
                    post_file.rename(self.done / post_file.name)
                    print(f'[OK] Moved to Done: {post_file.name}')
                    processed += 1
                else:
                    print(f'[WARN] Post not verified: {post_file.name}')
                    print('[INFO] File left in Approved folder for retry')
        
        return processed
    
    def _extract_content(self, filepath: Path) -> str:
        """Extract content from markdown file."""
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
    if len(sys.argv) < 3 or '--execute-approved' not in sys.argv:
        print('Usage: python linkedin_post_verify.py <vault_path> --execute-approved')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    poster = LinkedInPostVerifier(vault_path)
    count = poster.process_approved()
    
    print()
    print('=' * 70)
    print(f'  COMPLETED: {count} post(s) processed')
    print('=' * 70)
    print()


if __name__ == '__main__':
    main()
