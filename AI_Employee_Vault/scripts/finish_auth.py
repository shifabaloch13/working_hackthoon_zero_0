"""
Complete authentication with the provided code - No PKCE required for OOB flow
"""
import requests
import pickle
import json
from pathlib import Path

# Your authorization code
AUTH_CODE = "4/1AfrIepCAb_zGed0D715FS_gPpg18UmK4DMz5vQ_vpgMRATCUU28ZOJKwvI8"

# Load credentials
with open('D:/Download/working_hackthoon_zero_0/credeintals.json', 'r') as f:
    client_config = json.load(f)

client_id = client_config['installed']['client_id']
client_secret = client_config['installed']['client_secret']

print("Exchanging code for token...")
print(f"Client ID: {client_id[:20]}...")

# Token exchange (OOB flow doesn't require code_verifier)
token_url = 'https://oauth2.googleapis.com/token'
data = {
    'code': AUTH_CODE,
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
    token_path = Path('D:/Download/working_hackthoon_zero_0/AI_Employee_Vault/Logs/gmail_token.pickle')
    token_path.parent.mkdir(parents=True, exist_ok=True)
    with open(token_path, 'wb') as f:
        pickle.dump(creds, f)
    
    print(f"\nToken saved to: {token_path}")
    print("\nYou can now run Gmail Watcher!")
else:
    print(f"FAILED: {response.status_code}")
    print(response.text)
