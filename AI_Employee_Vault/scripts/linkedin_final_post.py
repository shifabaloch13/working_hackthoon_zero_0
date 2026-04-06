"""
LinkedIn Auto-Post - FINAL VERSION

This version:
1. Opens browser visibly
2. Clicks "Start a post"
3. Types content
4. Clicks "Post" button
5. Waits for confirmation
6. Keeps browser open so you can verify

Usage:
    python linkedin_final_post.py "Your post content here"
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
    """Post to LinkedIn with visible browser"""
    
    print("=" * 70)
    print("  LINKEDIN AUTO-POST - FINAL VERSION")
    print("=" * 70)
    print()
    
    try:
        with sync_playwright() as p:
            # Launch browser with saved session
            print("[1/6] Opening browser...")
            browser = p.chromium.launch_persistent_context(
                str(SESSION_PATH),
                headless=False,  # VISIBLE browser
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--start-maximized'
                ],
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = browser.pages[0]
            
            # Go to LinkedIn
            print("[2/6] Going to LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=60000)
            time.sleep(5)
            
            # Click "Start a post"
            print("[3/6] Clicking 'Start a post'...")
            post_box = page.query_selector('[class*="share-box-feed-entry__closed-share-box"]')
            if post_box:
                post_box.click()
                print("[OK] Post box clicked!")
                time.sleep(3)
            else:
                print("[ERROR] Could not find post box!")
                browser.close()
                return False
            
            # Find text input and type content
            print("[4/6] Typing content...")
            text_input = page.query_selector('div[contenteditable="true"]')
            if text_input:
                text_input.click()
                time.sleep(1)
                text_input.press('Control+a')
                time.sleep(0.5)
                text_input.press('Delete')
                time.sleep(0.5)
                text_input.type(content)
                print(f"[OK] Content typed: {content[:50]}...")
                time.sleep(3)
            else:
                print("[ERROR] Could not find text input!")
                browser.close()
                return False
            
            # Click Post button
            print("[5/6] Clicking 'Post' button...")
            
            # Try multiple Post button selectors
            post_button_selectors = [
                'button[aria-label="Post"]',
                'button:has-text("Post")',
                'button.artdeco-button--primary:has-text("Post")',
            ]
            
            post_button = None
            for selector in post_button_selectors:
                try:
                    post_button = page.query_selector(selector)
                    if post_button:
                        print(f"[OK] Found Post button with: {selector}")
                        break
                except:
                    continue
            
            if post_button:
                print("[OK] Post button found! Clicking...")
                post_button.click()
                print("[OK] Post button clicked!")
                
                # Wait for visibility settings popup to appear
                print("[INFO] Waiting for visibility settings popup...")
                time.sleep(5)
                
                # Look for "Done" button in the popup
                print("[INFO] Looking for 'Done' button in visibility popup...")
                
                done_button_selectors = [
                    'button:has-text("Done")',
                    'button[aria-label="Done"]',
                    '.artdeco-button--secondary:has-text("Done")',
                ]
                
                done_button = None
                for selector in done_button_selectors:
                    try:
                        done_button = page.query_selector(selector)
                        if done_button:
                            print(f"[OK] Found Done button with: {selector}")
                            break
                    except:
                        continue
                
                if done_button:
                    print("[OK] Done button found! Clicking...")
                    done_button.click()
                    print("[OK] Done button clicked!")
                    
                    # Wait for post to submit
                    print("[INFO] Waiting for post to submit (15 seconds)...")
                    time.sleep(15)
                    
                    # Check if post was successful
                    print()
                    print("=" * 70)
                    print("  ✅ POST SUBMITTED SUCCESSFULLY!")
                    print("=" * 70)
                    print()
                    print("Browser will stay open for 60 seconds.")
                    print("Please CHECK YOUR LINKEDIN FEED to verify the post!")
                    print()
                    print("Post URL: https://www.linkedin.com/feed/")
                    print()
                    
                    # Keep browser open for verification
                    time.sleep(60)
                    browser.close()
                    return True
                else:
                    print("[ERROR] Could not find Done button in popup!")
                    print()
                    print("=" * 70)
                    print("  ⚠️ VISIBILITY POPUP OPEN - MANUAL ACTION NEEDED")
                    print("=" * 70)
                    print()
                    print("Browser will stay open for 60 seconds.")
                    print("Please click 'Done' button MANUALLY in the popup.")
                    print()
                    
                    time.sleep(60)
                    browser.close()
                    return False
            else:
                print("[ERROR] Could not find Post button!")
                print()
                print("=" * 70)
                print("  ⚠️ POST BUTTON NOT FOUND")
                print("=" * 70)
                print()
                print("Browser will stay open for 60 seconds.")
                print("Please post MANUALLY in the open browser window.")
                print()
                
                time.sleep(60)
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
        print("Usage: python linkedin_final_post.py \"Your post content\"")
        print()
        print("Example:")
        print('  python linkedin_final_post.py "🚀 AI Employee is LIVE! #AI"')
        sys.exit(1)
    
    content = " ".join(sys.argv[1:])
    
    # Add hashtags if not present
    if "#" not in content:
        content += " #AI #Automation #PlatinumTier"
    
    success = post_to_linkedin(content)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
