"""
Simple Gmail Authentication - All in One

This script handles the complete flow properly with PKCE.

Usage:
    python simple_auth.py "D:/path/to/credeintals.json"
"""

import sys
import pickle
import webbrowser
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate(credentials_path: str, token_path: str):
    """Authenticate with Gmail API."""
    
    credentials_path = Path(credentials_path)
    token_path = Path(token_path)
    
    if not credentials_path.exists():
        print(f'[ERROR] Credentials file not found: {credentials_path}')
        return False
    
    print()
    print('=' * 70)
    print('  GMAIL AUTHENTICATION')
    print('=' * 70)
    print()
    print('Opening browser for authentication...')
    print()
    
    try:
        # Create flow - this handles PKCE automatically
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path,
            SCOPES
        )
        
        # Run local server flow (opens browser automatically)
        # This uses localhost redirect which works better than OOB
        creds = flow.run_local_server(
            port=0,
            host='localhost',
            authorization_prompt_message='Opening browser... ',
            success_message='Authentication successful! You can close this window.',
            open_browser=True
        )
        
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
        print('Now you can run Gmail Watcher:')
        print()
        print(f'  python gmail_watcher.py "../AI_Employee_Vault" "{credentials_path}"')
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
        print('Troubleshooting:')
        print('  1. Make sure your browser is the default browser')
        print('  2. Try running as Administrator')
        print('  3. Check if port 8080 is available')
        print()
        
        return False


def main():
    if len(sys.argv) < 2:
        print('Usage: python simple_auth.py <credentials.json>')
        sys.exit(1)
    
    credentials_path = sys.argv[1]
    
    # Token path - save in same folder as credentials for simplicity
    token_path = Path(credentials_path).parent / 'gmail_token.pickle'
    
    # Check if token already exists
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
