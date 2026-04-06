"""
Facebook Auto-Poster - Simple Anti-Refresh Version

This version waits for page to stabilize before allowing login.

Usage:
    python facebook_simple.py "D:/path/to/vault" --login-first  # Login first
    python facebook_simple.py "D:/path/to/vault" --post-approved  # Then auto-post
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright


def login_first(vault_path: str):
    """Open Facebook for manual login with anti-refresh protection."""
    
    session_path = Path(vault_path) / 'facebook_session'
    session_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("  FACEBOOK LOGIN - ANTI-REFRESH VERSION")
    print("=" * 70)
    print()
    print("📝 CRITICAL INSTRUCTIONS:")
    print()
    print("  1. Browser will open and load Facebook login page")
    print("  2. WAIT 10 SECONDS - DO NOT TYPE ANYTHING!")
    print("     (Page needs to stabilize)")
    print("  3. AFTER 10 seconds, you can type email/password")
    print("  4. If page refreshes, STOP and wait 5 seconds")
    print("  5. Then try typing again SLOWLY")
    print("  6. Once logged in, session will be saved")
    print()
    print("  ⏱️  Opening browser...")
    print()
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins',
            ],
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = browser.pages[0]
        
        # Execute anti-detection script
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
        print("[INFO] Loading Facebook...")
        page.goto('https://www.facebook.com', wait_until='domcontentloaded', timeout=60000)
        
        print()
        print("=" * 70)
        print("  WAIT 10 SECONDS BEFORE TYPING!")
        print("=" * 70)
        print()
        
        # Countdown
        for i in range(10, 0, -1):
            print(f'  ⏱️  Wait: {i} seconds remaining...')
            time.sleep(1)
        
        print()
        print("=" * 70)
        print("  ✅ NOW YOU CAN TYPE!")
        print("=" * 70)
        print()
        print("  📝 Type your email and password SLOWLY")
        print()
        print("  ⏱️  Waiting for login (3 minutes)...")
        print()
        
        # Wait for login
        for i in range(90):
            time.sleep(2)
            try:
                url = page.url
                if 'facebook.com' in url and 'login' not in url.lower() and 'checkpoint' not in url.lower():
                    print('[OK] ✅ Login detected!')
                    print('[INFO] Saving session...')
                    time.sleep(5)
                    print()
                    print("=" * 70)
                    print("  ✅ LOGIN COMPLETE! SESSION SAVED!")
                    print("=" * 70)
                    print()
                    print("  You can now auto-post with:")
                    print("  python facebook_simple.py \"../AI_Employee_Vault\" --post-approved")
                    print()
                    browser.close()
                    return True
            except:
                pass
        
        print('[ERROR] ❌ Login timeout!')
        browser.close()
        return False


def auto_post(vault_path: str):
    """Auto-post to Facebook."""
    
    session_path = Path(vault_path) / 'facebook_session'
    approved = Path(vault_path) / 'Approved'
    done = Path(vault_path) / 'Done'
    logs = Path(vault_path) / 'Logs'
    
    for folder in [approved, done, logs]:
        folder.mkdir(parents=True, exist_ok=True)
    
    posts = [f for f in approved.iterdir() if f.suffix == '.md' and 'FB_POST' in f.name]
    
    if not posts:
        print('[INFO] No posts to post')
        return 0
    
    print(f'[INFO] Found {len(posts)} post(s)')
    
    posted = 0
    for post_file in posts:
        print()
        print(f'Processing: {post_file.name}')
        
        content = post_file.read_text(encoding='utf-8')
        # Extract message
        lines = content.split('\n')
        in_content = False
        msg = []
        for line in lines:
            if line.strip() == '## Content':
                in_content = True
                continue
            if in_content and not line.startswith('##'):
                msg.append(line)
        message = '\n'.join(msg).strip()
        
        if not message:
            continue
        
        print(f'[INFO] Posting: {message[:50]}...')
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(session_path),
                    headless=False,
                    args=['--disable-blink-features=AutomationControlled'],
                    viewport={'width': 1920, 'height': 1080}
                )
                
                page = browser.pages[0]
                
                page.goto('https://www.facebook.com', wait_until='domcontentloaded', timeout=60000)
                time.sleep(5)
                
                # Check if logged in
                if 'login' in page.url.lower():
                    print('[ERROR] ❌ Not logged in! Run --login-first first')
                    browser.close()
                    continue
                
                # Go to home
                page.goto('https://www.facebook.com/home.php', timeout=30000)
                time.sleep(5)
                
                # Find post creator
                try:
                    post_btn = page.query_selector('div[placeholder="What\'s on your mind?"]')
                    if post_btn:
                        post_btn.click()
                        time.sleep(2)
                    
                    # Type message
                    text_areas = page.query_selector_all('div[contenteditable="true"]')
                    if text_areas:
                        text_areas[0].click()
                        time.sleep(1)
                        page.keyboard.press('Control+a')
                        page.keyboard.press('Delete')
                        time.sleep(0.5)
                        
                        for char in message:
                            page.keyboard.type(char, delay=50)
                        
                        time.sleep(2)
                        
                        # Post button
                        post_btn = page.query_selector('div[role="button"]:has-text("Post")')
                        if post_btn and post_btn.is_visible():
                            post_btn.click()
                            time.sleep(5)
                            print('[OK] ✅ Posted!')
                            
                            # Screenshot
                            screenshot = logs / f'fb_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                            page.screenshot(path=str(screenshot))
                            
                            posted += 1
                            post_file.rename(done / post_file.name)
                        else:
                            print('[ERROR] ❌ Post button not found')
                    else:
                        print('[ERROR] ❌ No text area')
                except Exception as e:
                    print(f'[ERROR] ❌ Error: {e}')
                
                browser.close()
        except Exception as e:
            print(f'[ERROR] ❌ Failed: {e}')
    
    print()
    print('=' * 70)
    print(f'  POSTED: {posted}')
    print('=' * 70)
    
    return posted


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage:')
        print('  python facebook_simple.py <vault_path> --login-first')
        print('  python facebook_simple.py <vault_path> --post-approved')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if '--login-first' in sys.argv:
        success = login_first(vault_path)
        sys.exit(0 if success else 1)
    elif '--post-approved' in sys.argv:
        auto_post(vault_path)
    else:
        print('[ERROR] Unknown option')
        sys.exit(1)
