"""
Get Gmail Authorization URL WITHOUT PKCE (for manual code exchange)
"""
import sys
import urllib.parse
import json
from pathlib import Path

if len(sys.argv) < 2:
    print('Usage: python get_auth_url_nopkce.py <credentials.json>')
    sys.exit(1)

credentials_path = Path(sys.argv[1])

with open(credentials_path, 'r') as f:
    client_config = json.load(f)

client_id = client_config['installed']['client_id']
scopes = ['https://www.googleapis.com/auth/gmail.readonly']

# Build URL WITHOUT PKCE
auth_url = (
    f"https://accounts.google.com/o/oauth2/auth?"
    f"client_id={client_id}&"
    f"redirect_uri=urn:ietf:wg:oauth:2.0:oob&"
    f"scope={'%20'.join(scopes)}&"
    f"response_type=code&"
    f"access_type=offline&"
    f"prompt=consent"
)

print()
print('=' * 70)
print('  GMAIL AUTHORIZATION URL (No PKCE)')
print('=' * 70)
print()
print('STEP 1: Copy this URL and open in browser:')
print()
print(auth_url)
print()
print('-' * 70)
print()
print('STEP 2: After granting access, copy the authorization code')
print()
print('STEP 3: Run this command with your code:')
print()
print(f'  python finish_auth_nopkce.py "{credentials_path}" "YOUR_CODE"')
print()
print('=' * 70)
print()
