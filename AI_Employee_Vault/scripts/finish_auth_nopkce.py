"""
Complete authentication WITHOUT PKCE
"""
import sys
import requests
import pickle
import json
from pathlib import Path

if len(sys.argv) < 3:
    print('Usage: python finish_auth_nopkce.py <credentials.json> <auth_code>')
    sys.exit(1)

credentials_path = Path(sys.argv[1])
auth_code = sys.argv[2]

with open(credentials_path, 'r') as f:
    client_config = json.load(f)

client_id = client_config['installed']['client_id']
client_secret = client_config['installed']['client_secret']

print("Exchanging code for token...")

# Token exchange WITHOUT PKCE
token_url = 'https://oauth2.googleapis.com/token'
data = {
    'code': auth_code,
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
    'grant_type': 'authorization_code'
}

response = requests.post(token_url, data=data)

if response.status_code == 200:
    token_data = response.json()
    print("SUCCESS! Token obtained")
    print(f"Has access_token: {'access_token' in token_data}")
    print(f"Has refresh_token: {'refresh_token' in token_data}")
    
    # Create credentials object
    from google.oauth2.credentials import Credentials
    creds = Credentials(
        token=token_data['access_token'],
        refresh_token=token_data.get('refresh_token'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_id,
        client_secret=client_secret,
        scopes=['https://www.googleapis.com/auth/gmail.readonly']
    )
    
    # Save token
    vault_logs = credentials_path.parent.parent / 'AI_Employee_Vault' / 'Logs'
    token_path = vault_logs / 'gmail_token.pickle'
    token_path.parent.mkdir(parents=True, exist_ok=True)
    with open(token_path, 'wb') as f:
        pickle.dump(creds, f)
    
    print(f"\nToken saved to: {token_path}")
    print("\n=== GMAIL AUTHENTICATION COMPLETE ===")
    print("\nYou can now run Gmail Watcher:")
    print(f'  python gmail_watcher.py "../AI_Employee_Vault" "{credentials_path}"')
    print()
else:
    print(f"FAILED: {response.status_code}")
    print(response.text)
