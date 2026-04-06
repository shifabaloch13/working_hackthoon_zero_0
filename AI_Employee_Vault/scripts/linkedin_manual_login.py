"""
LinkedIn Login - Manual Browser Method

This method uses YOUR existing browser session where you're already logged in.

Usage:
    python linkedin_manual_login.py
"""

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


def main():
    vault_path = "D:/Download/working_hackthoon_zero_0/AI_Employee_Vault"
    session_path = Path(vault_path) / 'linkedin_session'
    session_path.mkdir(parents=True, exist_ok=True)
    
    print()
    print('=' * 70)
    print('  LINKEDIN SESSION CAPTURE')
    print('=' * 70)
    print()
    print('This script will:')
    print('  1. Open a browser window')
    print('  2. You log in to LinkedIn')
    print('  3. Script saves your session')
    print('  4. Future posts will use saved session')
    print()
    print('IMPORTANT: Keep the browser window OPEN until script completes!')
    print()
    print('=' * 70)
    print()
    
    with sync_playwright() as p:
        # Launch browser
        print('[INFO] Opening browser...')
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
            ],
            viewport={'width': 1280, 'height': 800}
        )
        
        page = browser.pages[0]
        
        # Go to LinkedIn
        print('[INFO] Opening LinkedIn...')
        page.goto('https://www.linkedin.com/login', wait_until='domcontentloaded')
        
        print()
        print('-' * 70)
        print('  PLEASE LOG IN TO LINKEDIN IN THE BROWSER WINDOW')
        print('-' * 70)
        print()
        print('After you see your LinkedIn feed, the script will save your session.')
        print()
        print('Waiting for login...')
        print('(Script will wait up to 5 minutes)')
        print()
        
        # Wait for login (up to 5 minutes)
        logged_in = False
        for i in range(150):  # 5 minutes max
            try:
                current_url = page.url
                
                # Check if logged in (on feed or any page other than login)
                if 'feed' in current_url.lower() or '/in/' in current_url.lower():
                    logged_in = True
                    print()
                    print('=' * 70)
                    print('  LOGIN DETECTED!')
                    print('=' * 70)
                    print()
                    print('[OK] You are logged in!')
                    print('[INFO] Saving session...')
                    
                    # Wait for cookies to be set
                    time.sleep(5)
                    
                    print('[OK] Session saved!')
                    print()
                    print('Session location:', session_path)
                    print()
                    print('=' * 70)
                    print('  AUTHENTICATION COMPLETE!')
                    print('=' * 70)
                    print()
                    print('You can now post to LinkedIn:')
                    print()
                    print('  # Create post draft')
                    print('  python linkedin_poster.py "../AI_Employee_Vault" --draft "Your post"')
                    print()
                    print('  # Post approved content')
                    print('  python linkedin_poster.py "../AI_Employee_Vault" --execute-approved')
                    print()
                    break
            
            except Exception as e:
                print(f'[WARN] Error: {e}')
            
            time.sleep(2)
            
            # Progress indicator
            if (i + 1) % 15 == 0:
                print(f'[INFO] Still waiting... ({(i+1)*2}/300 seconds)')
        
        if not logged_in:
            print()
            print('=' * 70)
            print('  TIMEOUT - Login not completed')
            print('=' * 70)
            print()
            print('Please try again.')
        
        browser.close()


if __name__ == '__main__':
    main()
