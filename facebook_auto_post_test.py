#!/usr/bin/env python3
"""Facebook Auto-Post Test - Fresh Session"""
import sys
import os

# Clear ALL cached Facebook environment variables
for key in list(os.environ.keys()):
    if 'FACEBOOK' in key:
        del os.environ[key]

# Load from .env file (explicit path)
from dotenv import load_dotenv
load_dotenv('D:/Download/working_hackthoon_zero_0/.env')

print("=" * 70)
print("  FACEBOOK AUTO-POST TEST - FRESH SESSION")
print("=" * 70)
print()
print(f"Page ID: {os.getenv('FACEBOOK_PAGE_ID')}")
print(f"Token: {os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')[:20]}...")
print()

sys.path.insert(0, 'D:/Download/working_hackthoon_zero_0/AI_Employee_Vault/scripts')
from facebook_poster import FacebookMCP

# Initialize Facebook MCP
fb = FacebookMCP('D:/Download/working_hackthoon_zero_0/AI_Employee_Vault')

# Create test post
print("Creating test post...")
draft = fb.create_post_draft("🎉 AI Employee Gold Tier - Facebook Auto-Post is LIVE! All permissions working! #AI #Facebook #Automation #GoldTier")
print()

# Move to Approved
import shutil
approved_path = fb.approved / draft.name
shutil.move(str(draft), str(approved_path))
print(f"✅ Moved to Approved/")
print()

# Post to Facebook
print("Posting to Facebook...")
posted = fb.process_approved_posts()

print()
print("=" * 70)
if posted > 0:
    print("  🎉 SUCCESS! Facebook auto-post is WORKING!")
    print("=" * 70)
    print()
    print(f"  Posts published: {posted}")
    print()
    print("  Check your Facebook Page:")
    print("  https://www.facebook.com/951563341384120")
    print()
    print("  ✅ Gold Tier: Facebook/Instagram MCP - COMPLETE!")
else:
    print("  ❌ Failed to post (see errors above)")
print("=" * 70)
