"""
Simple Gmail Auth with Send Permission - Manual Code Entry

Usage:
    python gmail_simple_auth.py "D:/path/to/credeintals.json"
"""

import sys
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes with SEND permission
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]


def main():
    if len(sys.argv) < 2:
        print('Usage: python gmail_simple_auth.py <credentials.json>')
        sys.exit(1)
    
    credentials_path = Path(sys.argv[1])
    vault_logs = credentials_path.parent.parent / 'AI_Employee_Vault' / 'Logs'
    token_path = vault_logs / 'gmail_token.pickle'
    
    print()
    print('=' * 70)
    print('  GMAIL AUTH - SEND PERMISSION')
    print('=' * 70)
    print()
    
    # Delete old token
    if token_path.exists():
        print('[INFO] Deleting old read-only token...')
        token_path.unlink()
        print('[OK] Old token deleted')
        print()
    
    # Create flow with OOB (out-of-band) for manual code entry
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
    
    print('STEP 1: Open this URL in your browser:')
    print()
    print(auth_url)
    print()
    print('STEP 2: Sign in with your Google account')
    print('STEP 3: Grant ALL permissions (including "Send emails")')
    print('STEP 4: Copy the authorization code shown')
    print()
    
    code = input('Enter the authorization code: ').strip()
    
    if not code:
        print('[ERROR] No code provided')
        return
    
    print()
    print('[INFO] Exchanging code for token...')
    
    try:
        flow.fetch_token(code=code)
        creds = flow.credentials
        
        # Save token
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'wb') as f:
            pickle.dump(creds, f)
        
        print()
        print('=' * 70)
        print('  AUTHENTICATION SUCCESSFUL!')
        print('=' * 70)
        print()
        print(f'[OK] Token saved with SEND permission')
        print()
        print('Now you can send emails:')
        print('  python email_mcp_server.py "../AI_Employee_Vault" "../credeintals.json"')
        print()
        
    except Exception as e:
        print()
        print(f'[ERROR] Authentication failed: {e}')
        print()
        print('The code may have expired. Please try again.')


if __name__ == '__main__':
    main()
