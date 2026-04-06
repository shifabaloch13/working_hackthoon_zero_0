"""
Facebook Login - Use Your Regular Browser

This script generates a link for you to log in with your REGULAR Chrome browser.
Your session will be saved for auto-posting.

Usage:
    python facebook_login_manual.py "D:/path/to/vault"
"""

import sys
import time
import webbrowser
from pathlib import Path
from playwright.sync_api import sync_playwright


def login_with_regular_browser(vault_path: str):
    """Guide user to log in with their regular browser."""
    
    session_path = Path(vault_path) / 'facebook_session'
    session_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("  FACEBOOK LOGIN - MANUAL METHOD")
    print("=" * 70)
    print()
    print("📝 INSTRUCTIONS:")
    print()
    print("  STEP 1: Open Facebook in your REGULAR browser")
    print("          (Chrome, Edge, Firefox - whichever you use daily)")
    print()
    print("  STEP 2: Go to: https://www.facebook.com")
    print()
    print("  STEP 3: Log in to Facebook")
    print()
    print("  STEP 4: After logging in, come back here and press ENTER")
    print()
    print("  ⚠️  IMPORTANT: Use your REGULAR browser, NOT the automated one!")
    print()
    
    # Open Facebook in user's default browser
    print("[INFO] Opening Facebook in your default browser...")
    webbrowser.open('https://www.facebook.com')
    
    # Wait for user to log in
    input("Press ENTER when you've logged in to Facebook...")
    
    print()
    print("[OK] ✅ Great!")
    print()
    print("  Now the script will verify your login and save the session...")
    print()
    
    # Now try to use Playwright with the user's Chrome profile
    # This will attempt to use the same session
    try:
        with sync_playwright() as p:
            # Try to launch with user data directory
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                ],
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = browser.pages[0]
            
            print("[INFO] Checking Facebook login status...")
            page.goto('https://www.facebook.com', wait_until='domcontentloaded', timeout=30000)
            page.wait_for_timeout(5000)
            
            current_url = page.url
            
            if 'login' in current_url.lower() or 'checkpoint' in current_url.lower():
                print()
                print("=" * 70)
                print("  ⚠️  NOT LOGGED IN")
                print("=" * 70)
                print()
                print("  Please log in NOW in this browser window...")
                print("  (You have 2 minutes)")
                print()
                
                # Wait for login
                for i in range(60):
                    time.sleep(2)
                    if 'login' not in page.url.lower() and 'checkpoint' not in page.url.lower():
                        print("[OK] ✅ Login detected!")
                        break
                else:
                    print("[ERROR] ❌ Login timeout!")
                    browser.close()
                    return False
            
            print("[OK] ✅ Logged in successfully!")
            print("[INFO] Saving session...")
            time.sleep(5)
            
            browser.close()
            
            print()
            print("=" * 70)
            print("  ✅ SESSION SAVED!")
            print("=" * 70)
            print()
            print("  You can now auto-post to Facebook:")
            print()
            print("  python facebook_auto_post.py \"../AI_Employee_Vault\" --post-approved")
            print()
            
            return True
            
    except Exception as e:
        print(f"[ERROR] ❌ Failed to save session: {e}")
        print()
        print("  Alternative: Try logging in directly in the automated browser")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python facebook_login_manual.py <vault_path>')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    success = login_with_regular_browser(vault_path)
    
    if success:
        print("\n✅ Facebook login complete! You can now use auto-posting.\n")
    else:
        print("\n❌ Login failed. Please try again.\n")
    
    sys.exit(0 if success else 1)
