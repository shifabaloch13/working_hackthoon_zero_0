#!/usr/bin/env python3
"""Test Facebook auto-post with fresh environment"""
import sys
import os

# Clear any cached environment variables
for key in list(os.environ.keys()):
    if 'FACEBOOK' in key:
        del os.environ[key]

# Now load from .env file
from dotenv import load_dotenv
load_dotenv('D:/Download/working_hackthoon_zero_0/.env')

print("=" * 70)
print("  TESTING FACEBOOK CREDENTIALS")
print("=" * 70)
print()
print("Loaded from .env file:")
print(f"  Page ID: {os.getenv('FACEBOOK_PAGE_ID')}")
print(f"  Token starts with: {os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')[:20] if os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN') else 'None'}")
print()

# Test facebook_poster
sys.path.insert(0, 'D:/Download/working_hackthoon_zero_0/AI_Employee_Vault/scripts')
from facebook_poster import FacebookMCP

print("Initializing FacebookMCP...")
fb = FacebookMCP('D:/Download/working_hackthoon_zero_0/AI_Employee_Vault')
print()

if fb.page_id == '951563341384120':
    print("✅ SUCCESS! Correct Page ID loaded!")
    print()
    print("Creating test post...")
    draft = fb.create_post_draft("🎉 FACEBOOK AUTO-POST TEST! AI Employee Gold Tier is LIVE! #AI #Facebook #GoldTier")
    print()
    print(f"Draft created: {draft.name}")
    print()
    print("Next: Move to Approved/ and run --post-approved")
else:
    print(f"❌ FAILED! Wrong Page ID: {fb.page_id}")
