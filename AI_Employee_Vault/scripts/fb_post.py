"""
Facebook Auto-Poster - FINAL WORKING VERSION

Usage:
    python fb_post.py "D:/path/to/vault" --login-first   # Login once
    python fb_post.py "D:/path/to/vault" --post         # Auto-post
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright


def login(vault_path):
    """Login to Facebook and save session."""
    session = Path(vault_path) / 'facebook_session'
    session.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("  FACEBOOK LOGIN")
    print("="*70)
    print()
    print("📝 INSTRUCTIONS:")
    print("  1. Browser opens with Facebook")
    print("  2. WAIT 10 SECONDS - Don't type!")
    print("  3. Then type email/password SLOWLY")
    print("  4. Wait for home feed to load")
    print("  5. Session saves automatically")
    print()
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session),
            headless=False,
            args=['--disable-blink-features=AutomationControlled'],
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = browser.pages[0]
        page.goto('https://www.facebook.com', wait_until='domcontentloaded')
        
        print("\n⏱️  WAIT 10 SECONDS...\n")
        for i in range(10, 0, -1):
            print(f"  {i}...")
            time.sleep(1)
        
        print("\n✅ NOW TYPE YOUR EMAIL/PASSWORD!\n")
        print("Waiting for login (3 min)...\n")
        
        for i in range(90):
            time.sleep(2)
            try:
                url = page.url
                if 'facebook.com' in url and 'login' not in url.lower():
                    print("\n✅ Login detected! Saving session...\n")
                    time.sleep(5)
                    print("="*70)
                    print("  ✅ LOGIN COMPLETE!")
                    print("="*70)
                    print("\nNow run: python fb_post.py \"../AI_Employee_Vault\" --post\n")
                    browser.close()
                    return True
            except:
                pass
        
        print("\n❌ Login timeout!\n")
        browser.close()
        return False


def post(vault_path):
    """Auto-post to Facebook."""
    session = Path(vault_path) / 'facebook_session'
    approved = Path(vault_path) / 'Approved'
    done = Path(vault_path) / 'Done'
    logs = Path(vault_path) / 'Logs'
    
    for f in approved.glob('FB_POST_*.md'):
        print(f"\nProcessing: {f.name}")
        
        # Extract message
        content = f.read_text(encoding='utf-8')
        msg = []
        in_content = False
        for line in content.split('\n'):
            if line.strip() == '## Content':
                in_content = True
            elif in_content and not line.startswith('##'):
                msg.append(line)
        message = '\n'.join(msg).strip()
        
        if not message:
            continue
        
        print(f"Posting: {message[:50]}...")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(session),
                    headless=False,
                    args=['--disable-blink-features=AutomationControlled'],
                    viewport={'width': 1920, 'height': 1080}
                )
                
                page = browser.pages[0]
                page.goto('https://www.facebook.com', wait_until='domcontentloaded', timeout=60000)
                time.sleep(5)
                
                # Check login
                if 'login' in page.url.lower():
                    print("❌ Not logged in! Run --login-first first\n")
                    browser.close()
                    continue
                
                # Go to home
                page.goto('https://www.facebook.com/home.php', timeout=30000)
                time.sleep(5)
                
                # Try to post
                try:
                    # Click post creator
                    btn = page.query_selector('div[placeholder="What\'s on your mind?"]')
                    if btn:
                        btn.click()
                        time.sleep(2)
                    
                    # Type message
                    areas = page.query_selector_all('div[contenteditable="true"]')
                    if areas:
                        areas[0].click()
                        time.sleep(1)
                        page.keyboard.press('Control+a')
                        page.keyboard.press('Delete')
                        time.sleep(0.5)
                        
                        for char in message:
                            page.keyboard.type(char, delay=50)
                        
                        time.sleep(2)
                        
                        # Click Post
                        post_btn = page.query_selector('div[role="button"]:has-text("Post")')
                        if post_btn and post_btn.is_visible():
                            post_btn.click()
                            time.sleep(5)
                            print("✅ Posted!\n")
                            
                            # Screenshot
                            screenshot = logs / f'fb_{time.strftime("%Y%m%d_%H%M%S")}.png'
                            page.screenshot(path=str(screenshot))
                            
                            f.rename(done / f.name)
                        else:
                            print("❌ Post button not found\n")
                    else:
                        print("❌ No text area found\n")
                except Exception as e:
                    print(f"❌ Error: {e}\n")
                
                browser.close()
        except Exception as e:
            print(f"❌ Failed: {e}\n")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python fb_post.py <vault> --login-first")
        print("  python fb_post.py <vault> --post")
        sys.exit(1)
    
    vault = sys.argv[1]
    
    if '--login-first' in sys.argv:
        login(vault)
    elif '--post' in sys.argv:
        post(vault)
