"""
LinkedIn UI Screenshot Tool

Takes a screenshot of LinkedIn's current UI to see the actual selectors.

Usage:
    python linkedin_screenshot.py
"""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# ============================================================================
# CONFIGURATION
# ============================================================================
VAULT_PATH = Path("D:/Download/working_hackthoon_zero_0/AI_Employee_Vault")
SESSION_PATH = VAULT_PATH / 'linkedin_session'
SCREENSHOT_PATH = VAULT_PATH / 'Logs' / 'linkedin_ui_screenshot.png'
HTML_PATH = VAULT_PATH / 'Logs' / 'linkedin_ui_source.html'

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("  LINKEDIN UI SCREENSHOT TOOL")
    print("=" * 70)
    print()
    
    try:
        with sync_playwright() as p:
            # Launch browser with saved session
            print("[1/5] Opening browser with saved session...")
            browser = p.chromium.launch_persistent_context(
                str(SESSION_PATH),
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--start-maximized'
                ],
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = browser.pages[0]
            
            # Go to LinkedIn feed
            print("[2/5] Going to LinkedIn feed...")
            page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=60000)
            
            # Wait for page to fully load
            print("[3/5] Waiting for page to load (10 seconds)...")
            time.sleep(10)
            
            # Take screenshot
            print("[4/5] Taking screenshot...")
            page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
            print(f"[OK] Screenshot saved: {SCREENSHOT_PATH}")
            
            # Save HTML source
            print("[5/5] Saving HTML source...")
            html_content = page.content()
            with open(HTML_PATH, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"[OK] HTML saved: {HTML_PATH}")
            
            # Extract and print selectors
            print()
            print("=" * 70)
            print("  DETECTING SELECTORS")
            print("=" * 70)
            print()
            
            # Find "Start a post" button
            print("Searching for 'Start a post' button...")
            
            selectors_to_try = [
                'button[aria-label*="Create a post"]',
                'button[aria-label*="start a post"]',
                '.share-box-feed-entry__trigger',
                '[data-testid="share-box-feed-entry"]',
                'div.ember-view > button',
                'button.artdeco-button',
                '[class*="share-box"]',
                '[class*="feed-entry"]'
            ]
            
            for selector in selectors_to_try:
                try:
                    element = page.query_selector(selector)
                    if element:
                        print(f"✅ FOUND: {selector}")
                        # Get element text
                        text = element.inner_text()[:50]
                        print(f"   Text: {text}")
                        # Get element attributes
                        attrs = element.get_properties()
                        print(f"   Class: {element.get_attribute('class')[:100] if element.get_attribute('class') else 'N/A'}")
                    else:
                        print(f"❌ Not found: {selector}")
                except Exception as e:
                    print(f"❌ Error with {selector}: {str(e)[:50]}")
            
            print()
            print("=" * 70)
            print("  ANALYSIS COMPLETE")
            print("=" * 70)
            print()
            print("Next Steps:")
            print("  1. Open the screenshot: LinkedIn_ui_screenshot.png")
            print("  2. Inspect the HTML: linkedin_ui_source.html")
            print("  3. Find the correct selectors")
            print("  4. Update linkedin_poster.py")
            print()
            print("Browser will stay open for manual inspection.")
            print("Close it when done.")
            
            # Keep browser open for manual inspection
            time.sleep(60)
            
            browser.close()
            
    except Exception as e:
        print()
        print("=" * 70)
        print(f"  ❌ ERROR: {str(e)}")
        print("=" * 70)

if __name__ == "__main__":
    main()
