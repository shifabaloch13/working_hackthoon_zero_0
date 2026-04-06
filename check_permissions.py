"""Check what permissions your token actually has"""
import requests

# Your Page Access Token
token = "EAANxrrU9WAEBQ844NbDZB3bcBECIV8txFhzpRMmWYw3pr2NKOsdI7CZAdJ38DMerZCe1RILZCDWKd5UjdnjZBjTjsEaZAjrfybfZC7TlOVKXFPqdnQo6FBtgDwynEkBgtLPsBDHbl8pN8aySsCvpsRdwEmCwwUuvXJxdBlS3mFUFZA8Eh5LVrDbtQQAj14pdikOyBYy1KK6Wtenfszs1nbgKiNVZCEjNZAGci270BZBUIZALjrE9oAQZD"

# Check token info
url = f"https://graph.facebook.com/v18.0/me/permissions?access_token={token}"

response = requests.get(url)
data = response.json()

print("=" * 60)
print("YOUR TOKEN PERMISSIONS")
print("=" * 60)
print()

if 'data' in data:
    for perm in data['data']:
        status = "✅" if perm.get('status') == 'granted' else "❌"
        print(f"{status} {perm.get('permission')}: {perm.get('status')}")
else:
    print(f"Error: {data}")

print()
print("=" * 60)
