"""
Complete Gmail Authentication with Existing Code

Usage:
    python complete_auth.py "D:/path/to/credeintals.json" "YOUR_AUTH_CODE"
"""

import sys
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def complete_authentication(credentials_path: str, auth_code: str, token_path: str):
    """Complete authentication using existing authorization code."""
    
    credentials_path = Path(credentials_path)
    token_path = Path(token_path)
    
    print()
    print('=' * 70)
    print('  COMPLETING GMAIL AUTHENTICATION')
    print('=' * 70)
    print()
    print(f'[INFO] Using credentials: {credentials_path}')
    print(f'[INFO] Token will be saved to: {token_path}')
    print()
    
    # Create flow
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path,
        SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    
    try:
        print('[INFO] Exchanging authorization code for token...')
        flow.fetch_token(code=auth_code)
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
        print()
        print(f'  python gmail_watcher.py "../AI_Employee_Vault" "{credentials_path}"')
        print()
        print('The watcher will now:')
        print('  - Check Gmail every 2 minutes')
        print('  - Create action files for new emails')
        print('  - Update Dashboard.md')
        print()
        print('=' * 70)
        
        return True
        
    except Exception as e:
        print()
        print('=' * 70)
        print('  AUTHENTICATION FAILED')
        print('=' * 70)
        print()
        print(f'[ERROR] {e}')
        print()
        print('Possible causes:')
        print('  - Authorization code expired (codes expire quickly)')
        print('  - Code already used')
        print('  - Incorrect code')
        print()
        print('Solution:')
        print('  1. Run: python get_auth_url.py "D:/path/to/credeintals.json"')
        print('  2. Get a NEW authorization code')
        print('  3. Run this command immediately with the new code')
        print()
        
        return False


def main():
    if len(sys.argv) < 3:
        print('Usage: python complete_auth.py <credentials.json> <authorization_code>')
        print()
        print('Example:')
        print('  python complete_auth.py "D:/credeintals.json" "4/1AfrIep..."')
        print()
        print('OR: Just run with the code:')
        print('  python complete_auth.py "D:/Download/working_hackthoon_zero_0/credeintals.json" "YOUR_CODE"')
        sys.exit(1)
    
    credentials_path = sys.argv[1]
    auth_code = sys.argv[2]
    
    # Token path
    vault_logs = Path(credentials_path).parent.parent / 'AI_Employee_Vault' / 'Logs'
    token_path = vault_logs / 'gmail_token.pickle'
    
    success = complete_authentication(credentials_path, auth_code, str(token_path))
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
