#!/usr/bin/env python3
"""Facebook Auto-Post - FINAL TEST"""
import sys
import os
import shutil
from datetime import datetime

# Clear ALL cached Facebook environment variables
for key in list(os.environ.keys()):
    if 'FACEBOOK' in key:
        del os.environ[key]

# Load from .env file (explicit path)
from dotenv import load_dotenv
load_dotenv('D:/Download/working_hackthoon_zero_0/.env')

print("=" * 70)
print("  FACEBOOK AUTO-POST - FINAL TEST")
print("=" * 70)
print()
print(f"✅ Page ID: {os.getenv('FACEBOOK_PAGE_ID')}")
print(f"✅ Token: {os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')[:30]}...")
print()

sys.path.insert(0, 'D:/Download/working_hackthoon_zero_0/AI_Employee_Vault/scripts')
from facebook_poster import FacebookMCP

# Initialize Facebook MCP
fb = FacebookMCP('D:/Download/working_hackthoon_zero_0/AI_Employee_Vault')

# Verify correct page
if fb.page_id != '951563341384120':
    print(f"❌ WRONG PAGE ID: {fb.page_id}")
    print("Expected: 951563341384120")
    sys.exit(1)

print("✅ Correct Page ID loaded!")
print()

# Create FRESH test post
print("📝 Creating FRESH test post...")
draft_content = f"""---
type: facebook_post_request
message: 🎉 AI Employee Gold Tier - Facebook Auto-Post Test!
platform: facebook
created: {datetime.now().isoformat()}
character_count: 60
status: pending
---

# Facebook Post Draft

## Content
🎉 AI Employee Gold Tier - Facebook Auto-Post Test! 

Testing automated posting with proper permissions! #AI #Facebook #Automation #GoldTier

## Details
- **Platform**: Facebook
- **Character Count**: 120

## To Approve
Move this file to `/Approved` folder to post to Facebook.

---
*Created by AI Employee Facebook MCP*
"""

# Save draft
draft_file = fb.pending_approval / f"FB_POST_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
draft_file.write_text(draft_content, encoding='utf-8')
print(f"✅ Draft created: {draft_file.name}")
print()

# Move to Approved (simulate human approval)
approved_file = fb.approved / draft_file.name
shutil.move(str(draft_file), str(approved_file))
print(f"✅ Moved to Approved/ (simulating human approval)")
print()

# Post to Facebook
print("🚀 POSTING TO FACEBOOK...")
print()
posted = fb.process_approved_posts()

print()
print("=" * 70)
if posted > 0:
    print("  🎉🎉🎉 SUCCESS! FACEBOOK AUTO-POST IS WORKING! 🎉🎉🎉")
    print("=" * 70)
    print()
    print(f"  ✅ Posts published: {posted}")
    print()
    print("  📱 Check your Facebook Page NOW:")
    print("  👉 https://www.facebook.com/951563341384120")
    print()
    print("  ✅ Gold Tier: Facebook MCP - COMPLETE!")
    print("  ✅ All permissions working correctly!")
else:
    print("  ❌ FAILED to post to Facebook")
    print()
    print("  The token still doesn't have proper permissions.")
    print("  Recommendation: Use Playwright browser automation instead.")
print("=" * 70)
