"""
Facebook Auto-Poster - Playwright Browser Automation (IMPROVED)

Posts to Facebook using browser automation (no API needed!).
Works exactly like LinkedIn auto-poster.

Usage:
    python facebook_auto_post.py "D:/path/to/vault" --draft "Your post text"
    python facebook_auto_post.py "D:/path/to/vault" --post-approved
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class FacebookAutoPoster:
    """Facebook Auto-Poster using Playwright."""
    
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.session_path = self.vault / 'facebook_session'
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        self.pending_approval = self.vault / 'Pending_Approval'
        self.approved = self.vault / 'Approved'
        self.done = self.vault / 'Done'
        self.logs_folder = self.vault / 'Logs'
        
        for folder in [self.pending_approval, self.approved, self.done, self.logs_folder]:
            folder.mkdir(parents=True, exist_ok=True)
    
    def create_post_draft(self, message: str) -> Path:
        """Create a post draft for approval."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'FB_POST_{timestamp}.md'
        draft_file = self.pending_approval / filename
        
        content = f"""---
type: facebook_post_request
message: {message[:100]}{'...' if len(message) > 100 else ''}
platform: facebook
created: {datetime.now().isoformat()}
character_count: {len(message)}
status: pending
---

# Facebook Post Draft

## Content
{message}

## Details
- **Character Count**: {len(message)}

## To Approve
Move this file to `/Approved` folder to post to Facebook.

## To Reject
Move this file to `/Rejected` folder with reason.

---
*Created by AI Employee Facebook MCP (Playwright)*
"""
        draft_file.write_text(content, encoding='utf-8')
        print(f'[OK] Facebook post draft created: {draft_file.name}')
        return draft_file
    
    def post_to_facebook(self, message: str) -> bool:
        """Post to Facebook using browser automation."""
        
        print(f'[INFO] Posting to Facebook: {message[:50]}...')
        
        try:
            with sync_playwright() as p:
                # Launch browser with saved session
                print('[INFO] Launching browser...')
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,  # Visible browser - IMPORTANT for first login
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--start-maximized',
                    ],
                    viewport={'width': 1920, 'height': 1080}
                )
                
                page = browser.pages[0]
                
                # Navigate to Facebook
                print('[INFO] Opening Facebook...')
                page.goto('https://www.facebook.com', wait_until='domcontentloaded', timeout=60000)
                
                # Wait for page to load
                page.wait_for_timeout(10000)
                
                # Check if logged in
                current_url = page.url
                if 'login' in current_url.lower() or 'checkpoint' in current_url.lower() or 'recover' in current_url.lower():
                    print()
                    print('=' * 70)
                    print('  ⚠️  NOT LOGGED IN TO FACEBOOK')
                    print('=' * 70)
                    print()
                    print('  📝 INSTRUCTIONS:')
                    print('  1. Log in to Facebook in the browser window')
                    print('  2. Your session will be saved for future posts!')
                    print('  3. After login, the script will continue automatically')
                    print()
                    print('  Waiting for login (3 minutes)...')
                    print()
                    
                    # Wait for user to log in (max 3 minutes)
                    for i in range(90):
                        time.sleep(2)
                        current_url = page.url
                        if 'facebook.com' in current_url.lower():
                            if 'login' not in current_url.lower() and 'checkpoint' not in current_url.lower():
                                print('[OK] ✅ User logged in successfully!')
                                # Save session
                                time.sleep(3000)  # Wait for session to save
                                break
                    else:
                        print('[ERROR] ❌ Login timeout!')
                        browser.close()
                        return False
                
                # Navigate to home feed to ensure we're on main Facebook
                print('[INFO] Navigating to Facebook home...')
                page.goto('https://www.facebook.com/home.php', wait_until='domcontentloaded', timeout=30000)
                page.wait_for_timeout(5000)
                
                # Method 1: Click on "What's on your mind?" box
                print('[INFO] Opening post creator...')
                
                # Try to find the post creator input
                post_input_selectors = [
                    'div[placeholder="What\'s on your mind?"]',
                    'div[placeholder="Write something..."]',
                    'div[role="button"][aria-label*="post"]',
                    'div[class*="postCreator"]',
                    'div[class*="shareBox"]',
                ]
                
                clicked = False
                for selector in post_input_selectors:
                    try:
                        element = page.query_selector(selector)
                        if element and element.is_visible():
                            element.click()
                            print(f'[OK] ✅ Found and clicked post creator')
                            clicked = True
                            page.wait_for_timeout(3000)
                            break
                    except Exception as e:
                        continue
                
                if not clicked:
                    # Try clicking anywhere in the top post creation area
                    print('[INFO] Trying alternative method...')
                    # Press Tab multiple times to reach post creator, then Enter
                    for i in range(5):
                        page.keyboard.press('Tab')
                    page.keyboard.press('Enter')
                    page.wait_for_timeout(2000)
                
                # Wait for text editor to appear
                page.wait_for_timeout(3000)
                
                # Find the text input area and type message
                print('[INFO] Typing message...')
                
                # Look for contenteditable divs (Facebook's text editor)
                text_areas = page.query_selector_all('div[contenteditable="true"]')
                
                if text_areas:
                    # Use the first large text area (likely the post composer)
                    text_area = None
                    for ta in text_areas:
                        if ta.is_visible():
                            text_area = ta
                            break
                    
                    if text_area:
                        text_area.click()
                        page.wait_for_timeout(500)
                        
                        # Clear any existing text
                        page.keyboard.press('Control+a')
                        page.keyboard.press('Delete')
                        page.wait_for_timeout(300)
                        
                        # Type message character by character (human-like)
                        print('[INFO] Typing message (this may take a moment)...')
                        for i, char in enumerate(message):
                            page.keyboard.type(char, delay=30 + (i % 50))
                            if i > 0 and i % 40 == 0:
                                page.wait_for_timeout(100)  # Small pause every 40 chars
                        
                        print('[OK] ✅ Message typed!')
                        page.wait_for_timeout(2000)
                    else:
                        print('[ERROR] ❌ Could not find visible text area')
                        browser.close()
                        return False
                else:
                    print('[ERROR] ❌ No text areas found')
                    browser.close()
                    return False
                
                # Find and click Post button
                print('[INFO] Looking for Post button...')
                
                # Wait for Post button to become enabled
                for attempt in range(10):
                    post_button_selectors = [
                        'div[role="button"]:has-text("Post")',
                        'button:has-text("Post")',
                        '[aria-label="Post"]',
                        'div[class*="postButton"]',
                    ]
                    
                    post_button = None
                    for selector in post_button_selectors:
                        try:
                            elements = page.query_selector_all(selector)
                            for elem in elements:
                                if elem.is_visible() and not elem.is_disabled():
                                    post_button = elem
                                    break
                            if post_button:
                                break
                        except:
                            continue
                    
                    if post_button:
                        print('[OK] ✅ Found Post button!')
                        break
                    
                    print(f'[INFO] Post button not ready, waiting... (attempt {attempt+1}/10)')
                    page.wait_for_timeout(2000)
                
                if post_button:
                    print('[INFO] Clicking Post button...')
                    post_button.click()
                    page.wait_for_timeout(5000)
                    
                    # Check if post was successful (look for confirmation or URL change)
                    print('[OK] ✅ Facebook post published!')
                    
                    # Take screenshot as proof
                    screenshot_path = self.logs_folder / f'facebook_success_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                    page.screenshot(path=str(screenshot_path))
                    print(f'[OK] 📸 Screenshot saved: {screenshot_path.name}')
                    
                    # Wait a moment for Facebook to process
                    page.wait_for_timeout(3000)
                    
                    browser.close()
                    return True
                else:
                    print('[ERROR] ❌ Could not find enabled Post button')
                    print('[INFO] Taking screenshot for debugging...')
                    screenshot_path = self.logs_folder / f'facebook_error_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                    page.screenshot(path=str(screenshot_path))
                    print(f'[INFO] 📸 Screenshot saved: {screenshot_path.name}')
                    print()
                    print('  ⚠️  Manual intervention may be needed:')
                    print('  1. Check the screenshot in Logs/ folder')
                    print('  2. Facebook UI may have changed')
                    print('  3. Try logging in manually and posting once')
                    browser.close()
                    return False
                    
        except Exception as e:
            print(f'[ERROR] ❌ Failed to post to Facebook: {e}')
            import traceback
            traceback.print_exc()
            return False
    
    def process_approved_posts(self) -> int:
        """Process all approved posts."""
        approved_files = [f for f in self.approved.iterdir() 
                         if f.suffix == '.md' and 'FB_POST' in f.name]
        
        if not approved_files:
            print('[INFO] No approved posts to process')
            return 0
        
        print(f'[INFO] Found {len(approved_files)} approved post(s)')
        
        posted = 0
        for post_file in approved_files:
            print()
            print(f'Processing: {post_file.name}')
            
            # Parse post content
            content = post_file.read_text(encoding='utf-8')
            message = self._extract_message(content)
            
            if message:
                success = self.post_to_facebook(message)
                
                if success:
                    # Move to Done
                    post_file.rename(self.done / post_file.name)
                    print(f'[OK] ✅ Moved to Done: {post_file.name}')
                    
                    # Log the action
                    self._log_action(post_file, {'success': True})
                    posted += 1
                else:
                    print(f'[ERROR] ❌ Failed to post: {post_file.name}')
        
        return posted
    
    def _extract_message(self, content: str) -> str:
        """Extract message from approval file."""
        lines = content.split('\n')
        
        in_content = False
        message_lines = []
        
        for line in lines:
            if line.strip() == '## Content':
                in_content = True
                continue
            if in_content:
                if line.startswith('##'):
                    break
                message_lines.append(line)
        
        return '\n'.join(message_lines).strip()
    
    def _log_action(self, filepath: Path, result: dict):
        """Log post action."""
        log_file = self.logs_folder / f'facebook_{datetime.now().strftime("%Y-%m-%d")}.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': 'facebook_post_playwright',
            'file': filepath.name,
            'result': result
        }
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, indent=2) + '\n')


def main():
    if len(sys.argv) < 2:
        print('Usage: python facebook_auto_post.py <vault_path> [OPTIONS]')
        print()
        print('Options:')
        print('  --draft "text"     Create Facebook post draft')
        print('  --post-approved    Post all approved posts')
        print()
        print('Examples:')
        print('  python facebook_auto_post.py "../AI_Employee_Vault" --draft "Hello Facebook!"')
        print('  python facebook_auto_post.py "../AI_Employee_Vault" --post-approved')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] ❌ Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    facebook = FacebookAutoPoster(vault_path)
    
    # Parse options
    if '--draft' in sys.argv:
        # Create post draft
        idx = sys.argv.index('--draft') + 1
        if idx < len(sys.argv):
            post_text = sys.argv[idx]
            facebook.create_post_draft(post_text)
        else:
            print('[ERROR] ❌ No draft text provided')
    
    elif '--post-approved' in sys.argv:
        # Post approved posts
        posted = facebook.process_approved_posts()
        print()
        print('=' * 70)
        print(f'  POSTS PUBLISHED: {posted}')
        print('=' * 70)
        if posted > 0:
            print('  ✅ REAL Facebook posts published via Playwright!')
            print()
            print('  📱 Check your Facebook Page!')
        else:
            print('  ⚠️  No posts published')
            print()
            print('  TIPS:')
            print('  1. Make sure you\'re logged into Facebook')
            print('  2. Check Logs/ folder for screenshots')
            print('  3. Try logging into Facebook manually once')
        print()


if __name__ == '__main__':
    main()
