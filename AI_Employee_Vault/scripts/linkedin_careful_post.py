"""
LinkedIn Auto-Post - CAREFUL VERSION

This version:
1. Takes screenshots at each step
2. Waits longer between actions
3. Uses natural typing (with delays)
4. Verifies each step
5. Keeps browser open for manual verification

Usage:
    python linkedin_careful_post.py "Your post content"
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
# LINKEDIN CAREFUL POSTER
# ============================================================================

def post_to_linkedin(content):
    """Post to LinkedIn very carefully with screenshots"""
    
    print("=" * 70)
    print("  LINKEDIN AUTO-POST - CAREFUL VERSION")
    print("=" * 70)
    print()
    
    try:
        with sync_playwright() as p:
            # Launch browser
            print("[1/8] Opening browser...")
            browser = p.chromium.launch_persistent_context(
                str(SESSION_PATH),
                headless=False,
                args=['--disable-blink-features=AutomationControlled'],
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = browser.pages[0]
            
            # Go to LinkedIn
            print("[2/8] Going to LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', wait_until='networkidle', timeout=60000)
            time.sleep(10)  # Wait 10 seconds for full load
            page.screenshot(path=str(SCREENSHOT_PATH / 'step2_loaded.png'))
            print("[OK] LinkedIn loaded")
            
            # Click "Start a post"
            print("[3/8] Clicking 'Start a post'...")
            post_box = page.query_selector('[class*="share-box-feed-entry__closed-share-box"]')
            if post_box:
                post_box.scroll_into_view_if_needed()
                time.sleep(2)
                post_box.click()
                print("[OK] Post box clicked")
                time.sleep(5)  # Wait for modal
                page.screenshot(path=str(SCREENSHOT_PATH / 'step3_modal_open.png'))
            else:
                print("[ERROR] Could not find post box!")
                browser.close()
                return False
            
            # Find text input
            print("[4/8] Finding text input...")
            text_input = page.query_selector('div[contenteditable="true"]')
            if text_input:
                print("[OK] Text input found")
                page.screenshot(path=str(SCREENSHOT_PATH / 'step4_input_found.png'))
            else:
                print("[ERROR] Could not find text input!")
                browser.close()
                return False
            
            # Type content naturally
            print("[5/8] Typing content naturally...")
            text_input.click()
            time.sleep(2)
            
            # Clear existing text
            text_input.press('Control+a')
            time.sleep(1)
            text_input.press('Delete')
            time.sleep(1)
            
            # Type character by character (more natural)
            print(f"    Typing: {content[:50]}...")
            for char in content:
                text_input.type(char)
                time.sleep(0.05)  # Small delay between characters
            print("[OK] Content typed")
            time.sleep(5)  # Wait for LinkedIn to process
            page.screenshot(path=str(SCREENSHOT_PATH / 'step5_content_typed.png'))
            
            # Click Post button
            print("[6/8] Clicking 'Post' button...")
            post_button = page.query_selector('button:has-text("Post")')
            if post_button:
                post_button.scroll_into_view_if_needed()
                time.sleep(2)
                post_button.click()
                print("[OK] Post button clicked")
                time.sleep(5)  # Wait for popup
                page.screenshot(path=str(SCREENSHOT_PATH / 'step6_post_clicked.png'))
            else:
                print("[ERROR] Could not find Post button!")
                browser.close()
                return False
            
            # Find and click Done button in popup
            print("[7/8] Finding and clicking 'Done' button...")
            time.sleep(3)  # Wait for popup to fully render
            
            done_button = page.query_selector('button:has-text("Done")')
            if done_button:
                done_button.scroll_into_view_if_needed()
                time.sleep(2)
                done_button.click()
                print("[OK] Done button clicked")
                time.sleep(10)  # Wait for post to submit
                page.screenshot(path=str(SCREENSHOT_PATH / 'step7_done_clicked.png'))
            else:
                print("[ERROR] Could not find Done button!")
                print("[INFO] Popup might have different visibility options")
                # Try alternative selectors
                done_button = page.query_selector('button[aria-label="Done"]')
                if done_button:
                    done_button.click()
                    print("[OK] Done button clicked (aria-label)")
                    time.sleep(10)
                    page.screenshot(path=str(SCREENSHOT_PATH / 'step7_done_clicked_alt.png'))
                else:
                    print("[ERROR] Still could not find Done button!")
                    print("[INFO] Browser will stay open for manual completion")
                    time.sleep(60)
                    browser.close()
                    return False
            
            # Verify post
            print("[8/8] Verifying post...")
            time.sleep(10)
            page.screenshot(path=str(SCREENSHOT_PATH / 'step8_final.png'))
            
            print()
            print("=" * 70)
            print("  ✅ ALL STEPS COMPLETED!")
            print("=" * 70)
            print()
            print("Screenshots saved to:")
            print(f"  {SCREENSHOT_PATH}")
            print()
            print("Screenshot files:")
            print("  - step2_loaded.png")
            print("  - step3_modal_open.png")
            print("  - step4_input_found.png")
            print("  - step5_content_typed.png")
            print("  - step6_post_clicked.png")
            print("  - step7_done_clicked.png")
            print("  - step8_final.png")
            print()
            print("=" * 70)
            print("  PLEASE CHECK YOUR LINKEDIN FEED NOW!")
            print("=" * 70)
            print()
            print("Browser will stay open for 120 seconds.")
            print("Please verify if the post appears on your feed.")
            print()
            print("If you can see the post: ✅ SUCCESS!")
            print("If not: Check the screenshots to see what happened.")
            print()
            
            # Keep browser open for verification
            time.sleep(120)
            browser.close()
            return True
            
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
        print("Usage: python linkedin_careful_post.py \"Your post content\"")
        sys.exit(1)
    
    content = " ".join(sys.argv[1:])
    
    if "#" not in content:
        content += " #AI #Automation #Test"
    
    # Create screenshot folder
    SCREENSHOT_PATH.mkdir(parents=True, exist_ok=True)
    
    success = post_to_linkedin(content)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
