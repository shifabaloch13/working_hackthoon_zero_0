"""
Simple LinkedIn Poster - Uses YOUR Browser Session

This script uses the session saved from linkedin_manual_login.py
It opens a visible browser where you're already logged in.

Usage:
    python simple_linkedin_post.py "Your post content here"
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# ============================================================================
# CONFIGURATION
# ============================================================================
VAULT_PATH = Path("D:/Download/working_hackthoon_zero_0/AI_Employee_Vault")
SESSION_PATH = VAULT_PATH / 'linkedin_session'

# ============================================================================
# LINKEDIN POSTER
# ============================================================================

def post_to_linkedin(content):
    """Post to LinkedIn using saved session"""
    
    print("=" * 70)
    print("  SIMPLE LINKEDIN POSTER")
    print("=" * 70)
    print()
    
    try:
        with sync_playwright() as p:
            # Launch browser with saved session
            print("[1/4] Opening browser with saved session...")
            browser = p.chromium.launch_persistent_context(
                str(SESSION_PATH),
                headless=False,  # Visible browser
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--start-maximized'
                ],
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = browser.pages[0]
            
            # Go to LinkedIn
            print("[2/4] Going to LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=60000)
            
            # Wait for page to fully load
            print("[3/4] Waiting for page to load...")
            time.sleep(5)  # Wait 5 seconds for full load
            
            # Check if logged in
            if 'login' in page.url.lower():
                print("[ERROR] Not logged in!")
                print("Please run: python linkedin_manual_login.py first")
                browser.close()
                return False
            
            print(f"[OK] Logged in as: {page.url}")
            print()
            
            # Try to post
            print("[4/4] Creating post...")
            print(f"Content: {content[:50]}...")
            print()
            
            # Method 1: Try to find and click the post button
            print("Trying Method 1: Post button...")
            
            # Wait for post button to be visible
            time.sleep(3)
            
            # Try multiple selectors for "Start a post" button
            selectors = [
                'button[aria-label*="Create a post"]',
                'button[aria-label*="start a post"]',
                '.share-box-feed-entry__trigger',
                '[data-testid="share-box-feed-entry"]',
                'div.ember-view > button'
            ]
            
            post_button = None
            for selector in selectors:
                try:
                    post_button = page.query_selector(selector)
                    if post_button:
                        print(f"Found button with: {selector}")
                        break
                except:
                    continue
            
            if post_button:
                print("[OK] Found post button!")
                post_button.click()
                time.sleep(2)
                
                # Find the text input and type content
                text_input = page.query_selector('div[contenteditable="true"]')
                if text_input:
                    text_input.fill(content)
                    time.sleep(2)
                    
                    # Find and click Post button
                    post_submit = page.query_selector('button[aria-label*="Post"]')
                    if post_submit:
                        post_submit.click()
                        time.sleep(3)
                        
                        print()
                        print("=" * 70)
                        print("  ✅ SUCCESS! Check your LinkedIn - post should be created!")
                        print("=" * 70)
                        print()
                        print("The browser window will stay open so you can verify.")
                        print("Close it manually when done.")
                        
                        # Keep browser open for verification
                        time.sleep(10)
                        browser.close()
                        return True
            
            # Method 2: Just open the composer
            print("Method 1 failed, trying Method 2...")
            
            # Navigate to post creation URL
            page.goto('https://www.linkedin.com/feed/?createContent=true', wait_until='domcontentloaded')
            time.sleep(3)
            
            # Try to fill content
            text_input = page.query_selector('div[contenteditable="true"]')
            if text_input:
                text_input.fill(content)
                time.sleep(2)
                
                print()
                print("=" * 70)
                print("  ⚠️ Post composer opened - please click 'Post' button manually")
                print("=" * 70)
                print()
                print("Browser will stay open for you to verify and click Post.")
                
                # Keep browser open
                time.sleep(30)
                browser.close()
                return True
            
            print()
            print("=" * 70)
            print("  ⚠️ Could not auto-post, but browser is open")
            print("=" * 70)
            print()
            print("Please post manually in the open browser window.")
            print("Browser will stay open for 30 seconds.")
            
            time.sleep(30)
            browser.close()
            return True
            
    except Exception as e:
        print()
        print("=" * 70)
        print(f"  ❌ ERROR: {str(e)}")
        print("=" * 70)
        print()
        return False

# ============================================================================
# MAIN
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python simple_linkedin_post.py \"Your post content\"")
        print()
        print("Example:")
        print('  python simple_linkedin_post.py "🚀 AI Employee is LIVE! #AI"')
        sys.exit(1)
    
    content = " ".join(sys.argv[1:])
    
    # Add hashtags if not present
    if "#" not in content:
        content += " #AI #Automation #PlatinumTier"
    
    success = post_to_linkedin(content)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
