"""Debug token to see permissions"""
import requests

# Your Page Access Token
token = "EAANxrrU9WAEBQ844NbDZB3bcBECIV8txFhzpRMmWYw3pr2NKOsdI7CZAdJ38DMerZCe1RILZCDWKd5UjdnjZBjTjsEaZAjrfybfZC7TlOVKXFPqdnQo6FBtgDwynEkBgtLPsBDHbl8pN8aySsCvpsRdwEmCwwUuvXJxdBlS3mFUFZA8Eh5LVrDbtQQAj14pdikOyBYy1KK6Wtenfszs1nbgKiNVZCEjNZAGci270BZBUIZALjrE9oAQZD"

# Debug token
url = f"https://graph.facebook.com/debug_token?input_token={token}&access_token={token}"

response = requests.get(url)
data = response.json()

print("=" * 60)
print("TOKEN DEBUG INFO")
print("=" * 60)
print()

if 'data' in data:
    token_data = data['data']
    print(f"App ID: {token_data.get('app_id')}")
    print(f"Type: {token_data.get('type')}")
    print(f"Is Valid: {token_data.get('is_valid')}")
    print(f"Expires At: {token_data.get('expires_at')}")
    print()
    print("Scopes (Permissions):")
    scopes = token_data.get('scopes', [])
    for scope in scopes:
        print(f"  - {scope}")
else:
    print(f"Error: {data}")

print()
print("=" * 60)
