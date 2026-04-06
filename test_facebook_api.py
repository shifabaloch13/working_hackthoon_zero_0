#!/usr/bin/env python3
"""Test Facebook API Auto-Post with new credentials"""
import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Clear old env vars
for key in list(os.environ.keys()):
    if 'FACEBOOK' in key:
        del os.environ[key]

# Load from .env
from dotenv import load_dotenv
load_dotenv('D:/Download/working_hackthoon_zero_0/.env')

print("=" * 70)
print("  TESTING FACEBOOK API AUTO-POST")
print("=" * 70)
print()
print(f"App ID: {os.getenv('FACEBOOK_APP_ID')}")
print(f"Page ID: {os.getenv('FACEBOOK_PAGE_ID')}")
print(f"Token: {os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')[:30]}...")
print()

# Try to import facebook SDK
try:
    import facebook
    print("✅ Facebook SDK available")
except ImportError:
    print("❌ Facebook SDK not installed. Install with: pip install facebook-sdk")
    sys.exit(1)

# Create graph API client
try:
    graph = facebook.GraphAPI(
        access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
    )
    print("✅ Graph API client created")
except Exception as e:
    print(f"❌ Failed to create Graph API: {e}")
    sys.exit(1)

# Test connection
try:
    page_id = os.getenv('FACEBOOK_PAGE_ID')
    page_info = graph.get_object(page_id, fields='id,name')
    print(f"✅ Connected to Page: {page_info.get('name')} ({page_id})")
except Exception as e:
    print(f"❌ Failed to connect to page: {e}")
    sys.exit(1)

# Create test post
test_message = f"🎉 AI Employee Gold Tier - Facebook API Test! {datetime.now().strftime('%Y-%m-%d %H:%M')} #AI #Automation #GoldTier"

print()
print("📝 Creating test post...")
print(f"Message: {test_message[:80]}...")
print()

try:
    response = graph.put_object(
        parent_object=page_id,
        connection_name='feed',
        message=test_message
    )
    print("=" * 70)
    print("  🎉🎉🎉 SUCCESS! FACEBOOK API AUTO-POST IS WORKING! 🎉🎉🎉")
    print("=" * 70)
    print()
    print(f"  ✅ Post ID: {response.get('id')}")
    print()
    print(f"  📱 View your post:")
    print(f"  https://www.facebook.com/{response.get('id')}")
    print()
    print("  ✅ Gold Tier: Facebook MCP - COMPLETE!")
    print("  ✅ All permissions working correctly!")
    print()
except Exception as e:
    print("=" * 70)
    print("  ❌ FAILED TO POST")
    print("=" * 70)
    print()
    print(f"  Error: {e}")
    print()
    print("  This might be due to:")
    print("  1. App not reviewed by Facebook")
    print("  2. Missing permissions")
    print("  3. Token expired")
    print()
