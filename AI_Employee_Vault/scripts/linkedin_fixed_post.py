"""
LinkedIn Auto-Post - FIXED VERSION

Based on screenshot analysis, LinkedIn's current flow is:
1. Click "Start a post"
2. Type content
3. Click blue "Post" button (THIS IS THE FINAL BUTTON - no popup!)

Usage:
    python linkedin_fixed_post.py "Your post content"
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
SCREENSHOT_PATH = VAULT_PATH / 'Logs'

# ============================================================================
# LINKEDIN FIXED POSTER
# ============================================================================

def post_to_linkedin(content):
    """Post to LinkedIn with FIXED flow"""
    
    print("=" * 70)
    print("  LINKEDIN AUTO-POST - FIXED VERSION")
    print("=" * 70)
    print()
    print("Based on screenshot analysis:")
    print("  - No visibility popup")
    print("  - Blue 'Post' button is the final button")
    print("  - Just need to click it once!")
    print()
    
    try:
        with sync_playwright() as p:
            # Launch browser
            print("[1/5] Opening browser...")
            browser = p.chromium.launch_persistent_context(
                str(SESSION_PATH),
                headless=False,
                args=['--disable-blink-features=AutomationControlled'],
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = browser.pages[0]
            
            # Go to LinkedIn
            print("[2/5] Going to LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', wait_until='networkidle', timeout=60000)
            time.sleep(10)
            print("[OK] LinkedIn loaded")
            
            # Click "Start a post"
            print("[3/5] Clicking 'Start a post'...")
            post_box = page.query_selector('[class*="share-box-feed-entry__closed-share-box"]')
            if post_box:
                post_box.scroll_into_view_if_needed()
                time.sleep(2)
                post_box.click()
                print("[OK] Post box clicked")
                time.sleep(5)
            else:
                print("[ERROR] Could not find post box!")
                browser.close()
                return False
            
            # Type content
            print("[4/5] Typing content...")
            text_input = page.query_selector('div[contenteditable="true"]')
            if text_input:
                text_input.click()
                time.sleep(2)
                text_input.press('Control+a')
                time.sleep(1)
                text_input.press('Delete')
                time.sleep(1)
                
                # Type content
                print(f"    Content: {content[:50]}...")
                text_input.type(content)
                time.sleep(5)
                print("[OK] Content typed")
            else:
                print("[ERROR] Could not find text input!")
                browser.close()
                return False
            
            # Click the blue Post button (FINAL BUTTON)
            print("[5/5] Clicking blue 'Post' button...")
            time.sleep(3)
            
            # Take screenshot before clicking
            page.screenshot(path=str(SCREENSHOT_PATH / 'before_post_click.png'))
            
            # Find and click the blue Post button
            post_button = page.query_selector('button:has-text("Post")')
            
            if post_button:
                # Check if button is enabled
                is_disabled = post_button.get_attribute('disabled')
                if is_disabled:
                    print("[ERROR] Post button is disabled!")
                    print("[INFO] LinkedIn might require more content or interaction")
                    browser.close()
                    return False
                
                print("[OK] Post button found and enabled!")
                post_button.scroll_into_view_if_needed()
                time.sleep(2)
                post_button.click()
                print("[OK] Post button CLICKED!")
                
                # Wait for post to submit
                print("[INFO] Waiting for post to submit (30 seconds)...")
                time.sleep(30)
                
                # Take screenshot after
                page.screenshot(path=str(SCREENSHOT_PATH / 'after_post_click.png'))
                
                print()
                print("=" * 70)
                print("  ✅ POST BUTTON CLICKED!")
                print("=" * 70)
                print()
                print("Screenshots saved:")
                print(f"  - before_post_click.png")
                print(f"  - after_post_click.png")
                print()
                print("=" * 70)
                print("  CHECK YOUR LINKEDIN FEED NOW!")
                print("=" * 70)
                print()
                print("Browser will stay open for 120 seconds.")
                print("Please refresh your feed and check for the post.")
                print()
                
                # Keep browser open
                time.sleep(120)
                browser.close()
                return True
            else:
                print("[ERROR] Could not find Post button!")
                print("[INFO] Taking screenshot for debugging...")
                page.screenshot(path=str(SCREENSHOT_PATH / 'post_button_not_found.png'))
                browser.close()
                return False
            
    except Exception as e:
        print()
        print("=" * 70)
        print(f"  ❌ ERROR: {str(e)}")
        print("=" * 70)
        return False

# ============================================================================
# MAIN
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python linkedin_fixed_post.py \"Your post content\"")
        sys.exit(1)
    
    content = " ".join(sys.argv[1:])
    
    if "#" not in content:
        content += " #AI #Automation #FixedTest"
    
    SCREENSHOT_PATH.mkdir(parents=True, exist_ok=True)
    
    success = post_to_linkedin(content)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
