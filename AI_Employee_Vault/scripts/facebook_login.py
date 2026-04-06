"""
Facebook Login & Auto-Poster - Playwright

First run: Opens Facebook for you to log in manually, saves session
Future runs: Auto-posts using saved session

Usage:
    python facebook_login.py "D:/path/to/vault"  # Login first
    python facebook_auto_post.py "D:/path/to/vault" --post-approved  # Then auto-post
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright


def login_to_facebook(vault_path: str):
    """Open Facebook for manual login and save session."""
    
    session_path = Path(vault_path) / 'facebook_session'
    session_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("  FACEBOOK LOGIN - SAVE SESSION")
    print("=" * 70)
    print()
    print("📝 INSTRUCTIONS:")
    print()
    print("  1. A browser window will open")
    print("  2. Log in to Facebook manually")
    print("  3. Wait for your Facebook home feed to load")
    print("  4. The session will be saved automatically")
    print("  5. Close the browser when done")
    print()
    print("  ⏱️  Waiting 5 minutes for you to log in...")
    print()
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            args=['--disable-blink-features=AutomationControlled'],
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = browser.pages[0]
        
        # Go to Facebook
        print("[INFO] Opening Facebook...")
        page.goto('https://www.facebook.com', wait_until='domcontentloaded')
        
        # Wait for user to log in (5 minutes)
        for i in range(150):
            time.sleep(2)
            
            # Check if logged in
            current_url = page.url
            if 'facebook.com' in current_url.lower():
                if 'login' not in current_url.lower() and 'checkpoint' not in current_url.lower():
                    print()
                    print("[OK] ✅ Login detected!")
                    print("[INFO] Waiting for session to save...")
                    time.sleep(5)
                    print("[OK] ✅ Session saved successfully!")
                    print()
                    print("=" * 70)
                    print("  LOGIN COMPLETE!")
                    print("=" * 70)
                    print()
                    print("  You can now use auto-posting:")
                    print("  python facebook_auto_post.py \"../AI_Employee_Vault\" --post-approved")
                    print()
                    browser.close()
                    return True
        
        print("[ERROR] ❌ Login timeout!")
        browser.close()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python facebook_login.py <vault_path>')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    success = login_to_facebook(vault_path)
    sys.exit(0 if success else 1)
