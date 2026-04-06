#!/usr/bin/env python3
"""Auto-post approved Facebook posts"""
import sys
import os

# Clear cached environment variables
for key in list(os.environ.keys()):
    if 'FACEBOOK' in key:
        del os.environ[key]

# Load from .env
from dotenv import load_dotenv
load_dotenv('D:/Download/working_hackthoon_zero_0/.env')

sys.path.insert(0, 'D:/Download/working_hackthoon_zero_0/AI_Employee_Vault/scripts')
from facebook_poster import FacebookMCP

print("=" * 70)
print("  FACEBOOK AUTO-POST")
print("=" * 70)
print()

fb = FacebookMCP('D:/Download/working_hackthoon_zero_0/AI_Employee_Vault')
posted = fb.process_approved_posts()

print()
print("=" * 70)
print(f"  POSTS PUBLISHED: {posted}")
print("=" * 70)
if posted > 0:
    print("  ✅ REAL Facebook posts published!")
    print()
    print("  Check your Facebook Page: https://facebook.com/951563341384120")
else:
    print("  ⚠️ No posts published (check errors above)")
