#!/usr/bin/env python3
"""Test .env loading"""
from dotenv import load_dotenv
import os

# Try loading without path (like facebook_poster does)
print("=== Testing load_dotenv() without path ===")
load_dotenv()
print(f"Page ID: {os.getenv('FACEBOOK_PAGE_ID')}")
print(f"Token starts with: {os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')[:20] if os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN') else 'None'}")

# Clear and try with explicit path
print("\n=== Testing load_dotenv() WITH path ===")
for key in ['FACEBOOK_PAGE_ID', 'FACEBOOK_PAGE_ACCESS_TOKEN']:
    if key in os.environ:
        del os.environ[key]

load_dotenv('D:/Download/working_hackthoon_zero_0/.env')
print(f"Page ID: {os.getenv('FACEBOOK_PAGE_ID')}")
print(f"Token starts with: {os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')[:20] if os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN') else 'None'}")
