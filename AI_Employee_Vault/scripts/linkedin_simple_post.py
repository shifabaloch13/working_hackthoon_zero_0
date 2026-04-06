"""
LinkedIn Poster - Simple Method

This script posts to LinkedIn using your existing browser session.
Make sure you're already logged into LinkedIn in your default browser.

Usage:
    python linkedin_simple_post.py "D:/path/to/vault" "Your post content here"
"""

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


def post_to_linkedin(vault_path: str, content: str):
    """Post to LinkedIn using existing session."""
    
    vault = Path(vault_path).resolve()
    session_path = vault / 'linkedin_session'
    session_path.mkdir(parents=True, exist_ok=True)
    
    logs_folder = vault / 'Logs'
    logs_folder.mkdir(parents=True, exist_ok=True)
    
    print()
    print('=' * 70)
    print('  LINKEDIN POSTER - SIMPLE MODE')
    print('=' * 70)
    print()
    print('This script will use your saved LinkedIn session.')
    print()
    print('Content to post:')
    print('-' * 70)
    print(content)
    print('-' * 70)
    print()
    
    with sync_playwright() as p:
        # Launch browser with persistent context (uses saved session)
        print('[INFO] Launching browser with saved session...')
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,  # Visible browser so you can see what's happening
            args=[
                '--disable-blink-features=AutomationControlled',
            ],
            viewport={'width': 1280, 'height': 720}
        )
        
        page = browser.pages[0]
        
        # Go to LinkedIn
        print('[INFO] Opening LinkedIn...')
        page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=60000)
        
        # Wait for page to load
        print('[INFO] Waiting for page to load...')
        page.wait_for_timeout(10000)
        
        print(f'[INFO] Current URL: {page.url}')
        
        # Check if logged in
        if 'login' in page.url.lower():
            print()
            print('=' * 70)
            print('  NOT LOGGED IN!')
            print('=' * 70)
            print()
            print('Please log in to LinkedIn in the browser window.')
            print('After logging in, the script will continue automatically.')
            print()
            
            # Wait for user to log in (up to 5 minutes)
            for i in range(150):
                time.sleep(2)
                if 'feed' in page.url.lower():
                    print('[OK] Login detected!')
                    break
            else:
                print('[ERROR] Login timeout')
                browser.close()
                return False
        
        print('[OK] You are logged in!')
        print()
        print('-' * 70)
        print('  MANUAL STEP REQUIRED')
        print('-' * 70)
        print()
        print('In the browser window:')
        print('  1. Click "Start a post" or "Create a post"')
        print('  2. The script will type your content automatically')
        print('  3. Then click "Post" button manually')
        print()
        print('OR wait for automatic posting to attempt...')
        print()
        
        # Try to find and click the post creator
        print('[INFO] Looking for post creator...')
        
        # Click on the "Start a post" button
        post_trigger = page.query_selector('.share-box-feed-entry__trigger')
        
        if post_trigger:
            print('[OK] Found "Start a post" button')
            post_trigger.click()
            page.wait_for_timeout(3000)
        else:
            print('[WARN] Could not find "Start a post" button')
            print('[INFO] Please click it manually in the browser')
        
        # Wait for editor to appear
        print('[INFO] Waiting for editor...')
        page.wait_for_timeout(5000)
        
        # Find the text input and type content
        text_input = page.query_selector('div[contenteditable="true"][role="textbox"]')
        
        if text_input:
            print('[OK] Found text editor')
            print('[INFO] Typing content...')
            
            # Type the content
            text_input.click()
            page.wait_for_timeout(500)
            text_input.fill(content)
            page.wait_for_timeout(2000)
            
            print('[OK] Content typed!')
            print()
            print('-' * 70)
            print('  FINAL STEP')
            print('-' * 70)
            print()
            print('In the browser window:')
            print('  -> Click the "Post" button to publish')
            print()
            print('The script will wait 60 seconds for you to click Post...')
            print()
            
            # Wait for user to click Post
            time.sleep(60)
            
            print('[INFO] Closing browser...')
            browser.close()
            
            print()
            print('=' * 70)
            print('  DONE!')
            print('=' * 70)
            print()
            print('Your post should be live on LinkedIn!')
            print()
            
            return True
        else:
            print('[ERROR] Could not find text editor')
            print('[INFO] Please try again manually')
            browser.close()
            return False


def main():
    if len(sys.argv) < 3:
        print('Usage: python linkedin_simple_post.py <vault_path> <post_content>')
        print()
        print('Example:')
        print('  python linkedin_simple_post.py "../AI_Employee_Vault" "Hello LinkedIn!"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    content = sys.argv[2]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    success = post_to_linkedin(vault_path, content)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
