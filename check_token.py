"""Check token validity"""
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')

print(f"Token length: {len(token)}")
print(f"First 30 chars: {token[:30]}")
print(f"Last 30 chars: {token[-30:]}")

# Facebook tokens are typically 150-250 characters
if len(token) < 100:
    print("⚠️  Token seems too short - might be incomplete")
else:
    print("✅ Token length looks OK")
