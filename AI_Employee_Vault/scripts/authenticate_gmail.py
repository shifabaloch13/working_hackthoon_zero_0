"""
Simple Gmail Authentication Script

Run this ONCE to authenticate with Gmail API.
After successful authentication, the token is saved and you won't need to run this again.

Usage:
    python authenticate_gmail.py "D:/path/to/credeintals.json"
"""

import sys
import pickle
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate(credentials_path: str, token_path: str):
    """Authenticate with Gmail API and save token."""
    
    credentials_path = Path(credentials_path)
    token_path = Path(token_path)
    
    # Check if credentials file exists
    if not credentials_path.exists():
        print(f'[ERROR] Credentials file not found: {credentials_path}')
        sys.exit(1)
    
    print()
    print('=' * 70)
    print('  GMAIL API AUTHENTICATION')
    print('=' * 70)
    print()
    print('This script will authenticate with Gmail API using OAuth 2.0')
    print()
    
    # Create flow with out-of-band redirect URI
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path,
        SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    
    # Generate authorization URL
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    print('STEP 1: Visit this URL in your browser')
    print('-' * 70)
    print()
    print(auth_url)
    print()
    print('-' * 70)
    print()
    print('STEP 2: Sign in with your Google account')
    print('STEP 3: Grant permissions when asked')
    print('STEP 4: Copy the authorization code shown')
    print()
    
    # Get authorization code from user
    code = input('Enter the authorization code: ').strip()
    
    if not code:
        print('[ERROR] No authorization code provided')
        sys.exit(1)
    
    print()
    print('[INFO] Exchanging code for token...')
    
    try:
        # Exchange code for token
        flow.fetch_token(code=code)
        creds = flow.credentials
        
        # Save token
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        
        print()
        print('=' * 70)
        print('  AUTHENTICATION SUCCESSFUL!')
        print('=' * 70)
        print()
        print(f'[OK] Token saved to: {token_path}')
        print()
        print('You can now run the Gmail Watcher:')
        print(f'  python gmail_watcher.py "../AI_Employee_Vault" "{credentials_path}"')
        print()
        print('=' * 70)
        
    except Exception as e:
        print()
        print(f'[ERROR] Authentication failed: {e}')
        print()
        print('Possible causes:')
        print('  - Invalid authorization code (expired or incorrect)')
        print('  - Network error')
        print()
        print('Please try again.')
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print('Usage: python authenticate_gmail.py <credentials.json>')
        print()
        print('Example:')
        print('  python authenticate_gmail.py "D:/Download/working_hackthoon_zero_0/credeintals.json"')
        sys.exit(1)
    
    credentials_path = sys.argv[1]
    
    # Default token path
    vault_logs = Path(credentials_path).parent.parent / 'AI_Employee_Vault' / 'Logs'
    token_path = vault_logs / 'gmail_token.pickle'
    
    # Check if token already exists
    if token_path.exists():
        print(f'[INFO] Token already exists at: {token_path}')
        print('[INFO] Delete the file to re-authenticate')
        response = input('Do you want to re-authenticate? (y/n): ').strip().lower()
        if response != 'y':
            sys.exit(0)
    
    authenticate(credentials_path, str(token_path))


if __name__ == '__main__':
    main()
