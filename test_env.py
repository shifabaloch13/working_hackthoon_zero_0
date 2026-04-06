"""Test .env file loading"""
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

print("=" * 60)
print("Testing .env File Loading")
print("=" * 60)
print()

# Test Facebook credentials
print("Facebook Credentials:")
print(f"  FACEBOOK_APP_ID: {os.getenv('FACEBOOK_APP_ID', 'NOT FOUND')}")
print(f"  FACEBOOK_APP_SECRET: {'***' + os.getenv('FACEBOOK_APP_SECRET', 'NOT FOUND')[-4:] if os.getenv('FACEBOOK_APP_SECRET') else 'NOT FOUND'}")
print(f"  FACEBOOK_PAGE_ACCESS_TOKEN: {'***' + os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', 'NOT FOUND')[-10:] if os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN') else 'NOT FOUND'}")
print(f"  FACEBOOK_PAGE_ID: {os.getenv('FACEBOOK_PAGE_ID', 'NOT FOUND')}")
print(f"  FACEBOOK_GRAPH_API_VERSION: {os.getenv('FACEBOOK_GRAPH_API_VERSION', 'NOT FOUND')}")
print()
print("Instagram Credentials:")
print(f"  INSTAGRAM_BUSINESS_ACCOUNT_ID: {os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', 'NOT FOUND')}")
print()

# Check if all required credentials are present
required = [
    'FACEBOOK_APP_ID',
    'FACEBOOK_APP_SECRET', 
    'FACEBOOK_PAGE_ACCESS_TOKEN',
    'FACEBOOK_PAGE_ID'
]

missing = [key for key in required if not os.getenv(key)]

if missing:
    print(f"[WARN] Missing credentials: {missing}")
    print("[INFO] Please update .env file with your Facebook credentials")
else:
    print("[OK] All required Facebook credentials found!")
    print()
    print("Ready to use Facebook_auto-posting and comment detection!")

print()
print("=" * 60)
