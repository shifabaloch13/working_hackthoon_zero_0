"""
Gmail Authentication - Combined Script

This script generates URL and accepts code in the same flow.

Usage:
    python auth_gmail.py "D:/path/to/credeintals.json"
"""

import sys
import pickle
import hashlib
import base64
import urllib.parse
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def generate_code_verifier():
    """Generate a code verifier for PKCE."""
    import secrets
    return secrets.token_urlsafe(64)


def generate_code_challenge(verifier):
    """Generate code challenge from verifier."""
    sha256 = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(sha256).rstrip(b'=').decode()


def authenticate(credentials_path: str, token_path: str):
    """Complete authentication flow."""
    
    credentials_path = Path(credentials_path)
    token_path = Path(token_path)
    
    if not credentials_path.exists():
        print(f'[ERROR] Credentials not found: {credentials_path}')
        return False
    
    print()
    print('=' * 70)
    print('  GMAIL AUTHENTICATION')
    print('=' * 70)
    print()
    
    # Load credentials
    with open(credentials_path, 'r') as f:
        import json
        client_config = json.load(f)
    
    # Generate PKCE values
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    
    # Build authorization URL
    client_id = client_config['installed']['client_id']
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
    
    print('STEP 1: Open this URL in your browser')
    print('-' * 70)
    print()
    print(auth_url)
    print()
    print('-' * 70)
    print()
    print('STEP 2: Sign in and grant permissions')
    print()
    print('STEP 3: Copy the authorization code')
    print()
    
    code = input('Enter authorization code: ').strip()
    
    if not code:
        print('[ERROR] No code provided')
        return False
    
    print()
    print('[INFO] Exchanging code for token...')
    
    try:
        # Exchange code for credentials
        import requests
        
        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_config['installed']['client_secret'],
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
            'grant_type': 'authorization_code',
            'code_verifier': code_verifier
        }
        
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        
        # Create credentials object
        creds = Credentials(
            token=token_data['access_token'],
            refresh_token=token_data.get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_config['installed']['client_secret'],
            scopes=SCOPES
        )
        
        # Save token
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'wb') as f:
            pickle.dump(creds, f)
        
        print()
        print('=' * 70)
        print('  AUTHENTICATION SUCCESSFUL!')
        print('=' * 70)
        print()
        print(f'[OK] Token saved to: {token_path}')
        print()
        print('Now run Gmail Watcher:')
        print()
        print(f'  python gmail_watcher.py "../AI_Employee_Vault" "{credentials_path}"')
        print()
        
        return True
        
    except Exception as e:
        print()
        print('=' * 70)
        print('  AUTHENTICATION FAILED')
        print('=' * 70)
        print()
        print(f'[ERROR] {e}')
        print()
        print('The code may have expired. Please try again.')
        print()
        
        return False


def main():
    if len(sys.argv) < 2:
        print('Usage: python auth_gmail.py <credentials.json>')
        sys.exit(1)
    
    credentials_path = sys.argv[1]
    
    # Token path
    vault_logs = Path(credentials_path).parent.parent / 'AI_Employee_Vault' / 'Logs'
    token_path = vault_logs / 'gmail_token.pickle'
    
    # Check existing token
    if token_path.exists():
        print(f'[INFO] Token already exists: {token_path}')
        response = input('Re-authenticate? (y/n): ').strip().lower()
        if response != 'y':
            print('[INFO] Using existing token')
            return
        token_path.unlink()
        print('[INFO] Deleted old token')
    
    success = authenticate(credentials_path, str(token_path))
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
