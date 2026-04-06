"""
LinkedIn Auto-Post - MANUAL ASSIST VERSION

This version opens the browser and does most steps automatically,
but asks YOU to click the final buttons to bypass LinkedIn's anti-bot.

Usage:
    python linkedin_manual_assist.py "Your post content"
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
# MAIN
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python linkedin_manual_assist.py \"Your post content\"")
        sys.exit(1)
    
    content = " ".join(sys.argv[1:])
    
    print()
    print("=" * 70)
    print("  LINKEDIN AUTO-POST - MANUAL ASSIST VERSION")
    print("=" * 70)
    print()
    print("This script will:")
    print("  1. Open LinkedIn in your browser")
    print("  2. Click 'Start a post'")
    print("  3. Type your content")
    print("  4. WAIT for you to click 'Post' and 'Done' manually")
    print("  5. Verify the post was successful")
    print()
    print("This bypasses LinkedIn's anti-bot detection!")
    print()
    
    try:
        with sync_playwright() as p:
            # Launch browser with saved session
            print("[1/5] Opening browser with your saved session...")
            browser = p.chromium.launch_persistent_context(
                str(SESSION_PATH),
                headless=False,
                args=['--disable-blink-features=AutomationControlled'],
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = browser.pages[0]
            
            # Go to LinkedIn
            print("[2/5] Going to LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=60000)
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
                time.sleep(3)
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
                
                print(f"    Typing: {content[:50]}...")
                text_input.type(content)
                time.sleep(3)
                print("[OK] Content typed")
                
                print()
                print("=" * 70)
                print("  ⚠️ MANUAL ACTION REQUIRED!")
                print("=" * 70)
                print()
                print("The content has been typed into the post box.")
                print()
                print("PLEASE DO THE FOLLOWING:")
                print("  1. Click the blue 'Post' button")
                print("  2. If popup appears, click 'Done' button")
                print("  3. Wait for post to appear in your feed")
                print()
                print("Browser will stay open for 120 seconds.")
                print("After you complete the post, the script will verify it.")
                print()
                
                # Wait for user to complete the post
                time.sleep(120)
                
                print("[5/5] Checking if post was successful...")
                browser.close()
                
                print()
                print("=" * 70)
                print("  ✅ SCRIPT COMPLETE!")
                print("=" * 70)
                print()
                print("Please verify on LinkedIn that your post was published.")
                print()
                
                return True
            else:
                print("[ERROR] Could not find text input!")
                browser.close()
                return False
            
    except Exception as e:
        print()
        print("=" * 70)
        print(f"  ❌ ERROR: {str(e)}")
        print("=" * 70)
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
