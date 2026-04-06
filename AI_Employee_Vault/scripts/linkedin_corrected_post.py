"""
LinkedIn Auto-Post - CORRECTED VERSION

Based on user feedback, the CORRECT flow is:
1. Click "Start a post" → Modal opens
2. Type content
3. Click blue "Post" button → Visibility popup opens
4. Click "Done" button in popup
5. Post is submitted

Usage:
    python linkedin_corrected_post.py "Your post content"
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
# LINKEDIN CORRECTED POSTER
# ============================================================================

def post_to_linkedin(content):
    """Post to LinkedIn with CORRECT flow"""
    
    print("=" * 70)
    print("  LINKEDIN AUTO-POST - CORRECTED VERSION")
    print("=" * 70)
    print()
    print("CORRECT Flow:")
    print("  1. Click 'Start a post'")
    print("  2. Type content")
    print("  3. Click blue 'Post' button")
    print("  4. WAIT for visibility popup")
    print("  5. Click 'Done' button")
    print("  6. Post submitted!")
    print()
    
    try:
        with sync_playwright() as p:
            # Launch browser
            print("[1/7] Opening browser...")
            browser = p.chromium.launch_persistent_context(
                str(SESSION_PATH),
                headless=False,
                args=['--disable-blink-features=AutomationControlled'],
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = browser.pages[0]
            
            # Go to LinkedIn
            print("[2/7] Going to LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', wait_until='networkidle', timeout=60000)
            time.sleep(10)
            print("[OK] LinkedIn loaded")
            page.screenshot(path=str(SCREENSHOT_PATH / '01_loaded.png'))
            
            # Click "Start a post"
            print("[3/7] Clicking 'Start a post'...")
            post_box = page.query_selector('[class*="share-box-feed-entry__closed-share-box"]')
            if post_box:
                post_box.scroll_into_view_if_needed()
                time.sleep(3)
                post_box.click()
                print("[OK] Post box clicked")
                time.sleep(5)
                page.screenshot(path=str(SCREENSHOT_PATH / '02_modal_open.png'))
            else:
                print("[ERROR] Could not find post box!")
                browser.close()
                return False
            
            # Type content
            print("[4/7] Typing content...")
            text_input = page.query_selector('div[contenteditable="true"]')
            if text_input:
                text_input.click()
                time.sleep(2)
                text_input.press('Control+a')
                time.sleep(1)
                text_input.press('Delete')
                time.sleep(1)
                
                print(f"    Content: {content[:50]}...")
                text_input.type(content)
                time.sleep(5)
                print("[OK] Content typed")
                page.screenshot(path=str(SCREENSHOT_PATH / '03_content_typed.png'))
            else:
                print("[ERROR] Could not find text input!")
                browser.close()
                return False
            
            # Click blue Post button
            print("[5/7] Clicking blue 'Post' button...")
            time.sleep(3)
            
            post_button = page.query_selector('button:has-text("Post")')
            if post_button:
                post_button.scroll_into_view_if_needed()
                time.sleep(2)
                post_button.click()
                print("[OK] Post button clicked!")
                page.screenshot(path=str(SCREENSHOT_PATH / '04_post_clicked.png'))
            else:
                print("[ERROR] Could not find Post button!")
                browser.close()
                return False
            
            # WAIT for visibility popup
            print("[6/7] Waiting for visibility popup...")
            print("    (This is the popup with 'Done' button)")
            
            # Wait longer for popup to appear
            time.sleep(10)
            
            # Take screenshot to see what's on screen
            page.screenshot(path=str(SCREENSHOT_PATH / '05_waiting_popup.png'))
            print("[OK] Screenshot taken - checking for popup")
            
            # Look for Done button with multiple selectors
            done_button_selectors = [
                'button:has-text("Done")',
                'button[aria-label="Done"]',
                '.artdeco-button--secondary:has-text("Done")',
                'button[class*="share-box__update-control"]',
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
                print("[OK] Done button found!")
                done_button.scroll_into_view_if_needed()
                time.sleep(2)
                done_button.click()
                print("[OK] Done button CLICKED!")
                page.screenshot(path=str(SCREENSHOT_PATH / '06_done_clicked.png'))
                
                # Wait for post to submit
                print("[7/7] Waiting for post to submit...")
                time.sleep(15)
                page.screenshot(path=str(SCREENSHOT_PATH / '07_final.png'))
                
                print()
                print("=" * 70)
                print("  ✅ ALL STEPS COMPLETED!")
                print("=" * 70)
                print()
                print("Screenshots saved to:")
                print(f"  {SCREENSHOT_PATH}")
                print()
                print("Please check these screenshots:")
                print("  1. 05_waiting_popup.png - Shows the visibility popup")
                print("  2. 06_done_clicked.png - Shows after Done button click")
                print("  3. 07_final.png - Final state")
                print()
                print("=" * 70)
                print("  CHECK YOUR LINKEDIN FEED NOW!")
                print("=" * 70)
                print()
                print("Browser will stay open for 120 seconds.")
                print("Please refresh your feed and check for the post.")
                print()
                print("Post content:")
                print(f"  {content}")
                print()
                
                # Keep browser open
                time.sleep(120)
                browser.close()
                return True
            else:
                print("[ERROR] Could not find Done button!")
                print("[INFO] Popup might not have appeared or has different UI")
                print()
                print("=" * 70)
                print("  ⚠️ VISIBILITY POPUP NOT FOUND")
                print("=" * 70)
                print()
                print("Screenshots saved:")
                print(f"  {SCREENSHOT_PATH}")
                print()
                print("Please check the screenshots to see what happened.")
                print("Browser will stay open for 120 seconds.")
                print("You may need to complete the post manually.")
                print()
                
                time.sleep(120)
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
        print("Usage: python linkedin_corrected_post.py \"Your post content\"")
        sys.exit(1)
    
    content = " ".join(sys.argv[1:])
    
    if "#" not in content:
        content += " #AI #Automation #CorrectedTest"
    
    SCREENSHOT_PATH.mkdir(parents=True, exist_ok=True)
    
    success = post_to_linkedin(content)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
