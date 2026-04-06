"""
LinkedIn Authentication Script

This script opens LinkedIn, you log in, and saves your session for future use.

Usage:
    python linkedin_login.py "D:/path/to/vault"
"""

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


def login_to_linkedin(vault_path: str):
    """Open LinkedIn and save session after user logs in."""
    
    vault = Path(vault_path).resolve()
    session_path = vault / 'linkedin_session'
    session_path.mkdir(parents=True, exist_ok=True)
    
    logs_folder = vault / 'Logs'
    logs_folder.mkdir(parents=True, exist_ok=True)
    
    print()
    print('=' * 70)
    print('  LINKEDIN AUTHENTICATION')
    print('=' * 70)
    print()
    print('STEP 1: Browser will open in 3 seconds...')
    print()
    print('STEP 2: LinkedIn login page will appear')
    print()
    print('STEP 3: Sign in with your LinkedIn account')
    print()
    print('STEP 4: After logging in, wait for "Session saved" message')
    print()
    print('=' * 70)
    print()
    
    with sync_playwright() as p:
        # Launch browser with persistent context
        print('[INFO] Launching browser...')
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,  # Visible browser
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ],
            viewport={'width': 1280, 'height': 720}
        )
        
        page = browser.pages[0]
        
        # Navigate to LinkedIn
        print('[INFO] Opening LinkedIn...')
        page.goto('https://www.linkedin.com/login', wait_until='domcontentloaded')
        
        print()
        print('-' * 70)
        print('  BROWSER IS OPEN - PLEASE LOG IN NOW')
        print('-' * 70)
        print()
        print('In the browser window:')
        print('  1. Enter your LinkedIn email')
        print('  2. Enter your password')
        print('  3. Click "Sign in"')
        print()
        print('After successful login, the script will detect it and save session.')
        print()
        print('Waiting for login... (this may take a minute)')
        print()
        
        # Wait for user to log in (max 5 minutes)
        max_wait = 300  # 5 minutes
        check_interval = 2  # Check every 2 seconds
        elapsed = 0
        
        while elapsed < max_wait:
            try:
                # Check if we're on the feed page (logged in)
                current_url = page.url
                
                if 'feed' in current_url.lower() or 'mynetwork' in current_url.lower():
                    print()
                    print('=' * 70)
                    print('  LOGIN DETECTED!')
                    print('=' * 70)
                    print()
                    print('[OK] You are logged in to LinkedIn')
                    
                    # Wait a bit for cookies to settle
                    print('[INFO] Saving session...')
                    time.sleep(3)
                    
                    # Close browser (session is saved in session_path)
                    browser.close()
                    
                    print()
                    print('[OK] Session saved to:', session_path)
                    print()
                    print('=' * 70)
                    print('  AUTHENTICATION COMPLETE!')
                    print('=' * 70)
                    print()
                    print('You can now use LinkedIn Poster:')
                    print()
                    print('  # Create a post draft')
                    print('  python linkedin_poster.py "../AI_Employee_Vault" --draft "Your post"')
                    print()
                    print('  # Post approved content')
                    print('  python linkedin_poster.py "../AI_Employee_Vault" --execute-approved')
                    print()
                    return True
                
                elif 'login' in current_url.lower():
                    # Still on login page, keep waiting
                    pass
                
            except Exception as e:
                print(f'[WARN] Error checking status: {e}')
            
            time.sleep(check_interval)
            elapsed += check_interval
            
            # Show progress every 10 seconds
            if elapsed % 10 == 0:
                print(f'[INFO] Still waiting... ({elapsed}/{max_wait}s)')
        
        # Timeout
        print()
        print('=' * 70)
        print('  TIMEOUT - Login not detected')
        print('=' * 70)
        print()
        print('The browser was open for 5 minutes but login was not detected.')
        print()
        print('Possible issues:')
        print('  - You didn\'t complete the login')
        print('  - LinkedIn page didn\'t load properly')
        print('  - Network issues')
        print()
        print('Please run the script again.')
        print()
        
        browser.close()
        return False


def main():
    if len(sys.argv) < 2:
        print('Usage: python linkedin_login.py <vault_path>')
        print()
        print('Example:')
        print('  python linkedin_login.py "D:/Download/working_hackthoon_zero_0/AI_Employee_Vault"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    success = login_to_linkedin(vault_path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
