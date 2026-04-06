"""
Simple Gmail Auth for blackcat@gmail.com - Manual Code Entry
No redirect URI issues - just copy/paste the code
"""

import sys
import pickle
import json
import hashlib
import base64
import secrets
from pathlib import Path
import requests
from google.oauth2.credentials import Credentials

# Configuration
CREDENTIALS_FILE = 'D:/Download/working_hackthoon_zero_0/credeintals.json'
TOKEN_FILE = 'D:/Download/working_hackthoon_zero_0/AI_Employee_Vault/Logs/gmail_token.pickle'
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def generate_pkce():
    """Generate PKCE code verifier and challenge."""
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b'=').decode()
    return code_verifier, code_challenge

def main():
    print()
    print('=' * 70)
    print('  GMAIL AUTH - blackcat@gmail.com')
    print('=' * 70)
    print()
    
    # Load credentials
    with open(CREDENTIALS_FILE, 'r') as f:
        client_config = json.load(f)
    
    # Handle both 'installed' and 'web' formats
    if 'installed' in client_config:
        auth_info = client_config['installed']
    elif 'web' in client_config:
        auth_info = client_config['web']
    else:
        print('[ERROR] Unknown credentials format')
        return
    
    client_id = auth_info['client_id']
    client_secret = auth_info['client_secret']
    
    # Generate PKCE
    code_verifier, code_challenge = generate_pkce()
    
    # Build auth URL
    auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri=urn:ietf:wg:oauth:2.0:oob&"
        f"scope={'%20'.join(SCOPES)}&"
        f"response_type=code&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    
    print('STEP 1: Open this URL in your browser:')
    print()
    print(auth_url)
    print()
    print('STEP 2: Sign in with blackcat@gmail.com')
    print('STEP 3: Click "Allow" to grant ALL permissions')
    print('STEP 4: Copy the authorization code (starts with 4/...)')
    print()
    
    code = input('Enter the authorization code: ').strip()
    
    if not code:
        print('[ERROR] No code provided')
        return
    
    print()
    print('[INFO] Exchanging code for token...')
    
    # Exchange code for token
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        'grant_type': 'authorization_code',
        'code_verifier': code_verifier
    }
    
    resp = requests.post(token_url, data=data)
    
    if resp.status_code == 200:
        token_data = resp.json()
        print('[OK] Token received!')
        
        # Create credentials
        creds = Credentials(
            token=token_data.get('access_token'),
            refresh_token=token_data.get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES
        )
        
        # Save token
        token_path = Path(TOKEN_FILE)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        pickle.dump(creds, open(token_path, 'wb'))
        
        print()
        print('=' * 70)
        print('  AUTHENTICATION SUCCESSFUL!')
        print('=' * 70)
        print()
        print(f'[OK] Token saved for: blackcat@gmail.com')
        print()
        print('Scopes granted:')
        print('  ✓ gmail.readonly - Read emails')
        print('  ✓ gmail.send - Send emails')
        print()
        print('Now you can use Gmail with blackcat@gmail.com!')
        print()
        print('Commands:')
        print('  # Watch Gmail')
        print('  python gmail_watcher.py "../AI_Employee_Vault" "../credeintals.json"')
        print()
        print('  # Send test email')
        print('  python send_test_email.py')
        print()
    else:
        print()
        print('=' * 70)
        print('  AUTHENTICATION FAILED')
        print('=' * 70)
        print()
        print(f'[ERROR] {resp.status_code}')
        print(resp.text)
        print()
        print('The code may have expired. Please try again.')

if __name__ == '__main__':
    main()
