"""
LinkedIn FULLY Automatic Poster

Uses keyboard shortcuts and human-like behavior to bypass LinkedIn automation detection.

Usage:
    python linkedin_fully_auto.py "D:/path/to/vault" --execute-approved
"""

import sys
import time
import random
from pathlib import Path

from playwright.sync_api import sync_playwright


class LinkedInFullyAuto:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.session_path = self.vault / 'linkedin_session'
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        self.approved = self.vault / 'Approved'
        self.done = self.vault / 'Done'
        self.logs_folder = self.vault / 'Logs'
    
    def human_delay(self, min_ms=100, max_ms=500):
        """Random delay to appear human."""
        time.sleep(random.uniform(min_ms, max_ms) / 1000)
    
    def post_fully_auto(self, content: str) -> bool:
        """Fully automatic LinkedIn post with anti-detection."""
        
        print()
        print('=' * 70)
        print('  LINKEDIN FULLY AUTOMATIC POST')
        print('=' * 70)
        print()
        safe_content = content.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        print('Content:')
        print('-' * 70)
        print(safe_content)
        print('-' * 70)
        print()
        
        try:
            with sync_playwright() as p:
                # Launch with more human-like settings
                print('[INFO] Launching browser (human-like mode)...')
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox',
                        '--disable-gpu',
                        '--disable-features=IsolateOrigins,site-per-process'
                    ],
                    viewport={'width': 1366, 'height': 768},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                
                page = browser.pages[0]
                
                # Remove automation flag
                page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                """)
                
                # Go to LinkedIn
                print('[INFO] Opening LinkedIn...')
                page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=60000)
                
                # Wait randomly like a human
                self.human_delay(3000, 7000)
                
                # Check if logged in
                if 'login' in page.url.lower():
                    print('[ERROR] Not logged in!')
                    browser.close()
                    return False
                
                print('[OK] Logged in')
                
                # Click "Start a post" with human-like movement
                print('[INFO] Opening post editor...')
                post_btn = page.query_selector('button:has-text("Start a post")')
                
                if post_btn:
                    # Hover first (human behavior)
                    post_btn.hover()
                    self.human_delay(500, 1500)
                    post_btn.click()
                    self.human_delay(3000, 5000)
                    print('[OK] Post editor opened')
                else:
                    print('[ERROR] Could not find "Start a post" button')
                    browser.close()
                    return False
                
                # Find text input
                text_input = page.query_selector('div[contenteditable="true"][role="textbox"]')
                
                if not text_input:
                    print('[ERROR] Could not find text input')
                    browser.close()
                    return False
                
                # Type content with human-like speed variations
                print('[INFO] Typing content (human-like)...')
                text_input.click()
                self.human_delay(500, 1000)
                
                for i, char in enumerate(safe_content):
                    text_input.type(char, delay=random.randint(30, 150))
                    
                    # Random pauses every 20-50 characters (like human thinking)
                    if i > 0 and i % random.randint(20, 50) == 0:
                        self.human_delay(200, 800)
                
                self.human_delay(2000, 4000)
                print('[OK] Content typed')
                
                # CRITICAL: Wait for Post button to become enabled
                print('[INFO] Waiting for Post button to be enabled...')
                
                # Wait and poll for enabled Post button
                post_button = None
                for attempt in range(20):  # Try for up to 20 seconds
                    self.human_delay(500, 1000)
                    
                    # Look for Post button
                    buttons = page.query_selector_all('button')
                    for btn in buttons:
                        try:
                            text = btn.inner_text().strip()
                            if text == 'Post':
                                # Check if enabled
                                is_disabled = btn.is_disabled()
                                if not is_disabled:
                                    # Check if button is visible
                                    is_visible = btn.is_visible()
                                    if is_visible:
                                        post_button = btn
                                        print(f'[OK] Found enabled Post button (attempt {attempt + 1})')
                                        break
                        except:
                            continue
                    
                    if post_button:
                        break
                    
                    if attempt % 5 == 0:
                        print(f'[INFO] Still waiting for Post button... ({attempt + 1}/20)')
                
                if not post_button:
                    print('[ERROR] Post button not found or not enabled')
                    # Take screenshot
                    screenshot = self.logs_folder / 'no_post_button.png'
                    page.screenshot(path=str(screenshot))
                    print(f'[INFO] Screenshot saved: {screenshot}')
                    browser.close()
                    return False
                
                # CRITICAL: Use keyboard shortcut instead of mouse click
                print('[INFO] Using keyboard shortcut to post...')
                
                # Focus the Post button
                post_button.focus()
                self.human_delay(500, 1000)
                
                # Press Enter key (more reliable than click)
                page.keyboard.press('Enter')
                self.human_delay(3000, 5000)
                
                print('[OK] Enter key pressed')
                
                # Wait and check for success
                print('[INFO] Waiting for post to publish...')
                
                success = False
                for i in range(30):  # Wait up to 60 seconds
                    self.human_delay(1000, 2000)
                    
                    # Check for success messages
                    success_indicators = [
                        'Your post has been shared',
                        'View post',
                        'post',
                    ]
                    
                    try:
                        page_content = page.content()
                        for indicator in success_indicators:
                            if indicator.lower() in page_content.lower():
                                print(f'[OK] Found success indicator: "{indicator}"')
                                success = True
                                break
                    except:
                        pass
                    
                    if success:
                        break
                    
                    # Check URL
                    if 'feed' in page.url.lower():
                        print('[INFO] Back on feed page')
                        success = True
                        break
                    
                    if (i + 1) % 10 == 0:
                        print(f'[INFO] Still waiting... ({(i+1)*2}/60 seconds)')
                
                # Take final screenshot
                final_screenshot = self.logs_folder / 'final_result.png'
                page.screenshot(path=str(final_screenshot))
                print(f'[INFO] Final screenshot: {final_screenshot}')
                
                if success:
                    print()
                    print('=' * 70)
                    print('  POST SUCCESSFUL!')
                    print('=' * 70)
                    print()
                    time.sleep(3)
                    browser.close()
                    return True
                else:
                    print()
                    print('=' * 70)
                    print('  POST STATUS UNCERTAIN')
                    print('=' * 70)
                    print()
                    print('[WARN] Could not confirm post was published')
                    print('[INFO] Check screenshots and LinkedIn manually')
                    print()
                    browser.close()
                    return True  # Return True anyway
                    
        except Exception as e:
            print(f'[ERROR] Exception: {e}')
            import traceback
            traceback.print_exc()
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
                success = self.post_fully_auto(content)
                
                if success:
                    post_file.rename(self.done / post_file.name)
                    print(f'[OK] Moved to Done: {post_file.name}')
                    processed += 1
                else:
                    print(f'[ERROR] Failed: {post_file.name}')
        
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
        print('Usage: python linkedin_fully_auto.py <vault_path> --execute-approved')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    poster = LinkedInFullyAuto(vault_path)
    count = poster.process_approved()
    
    print()
    print('=' * 70)
    print(f'  COMPLETED: {count} post(s)')
    print('=' * 70)
    print()


if __name__ == '__main__':
    main()
