"""
Re-authenticate Gmail with SEND permissions

The current token only has READ permission. This will get a token with SEND permission.

Usage:
    python gmail_auth_send.py "D:/path/to/credeintals.json"
"""

import sys
import pickle
import webbrowser
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API scopes - now with SEND permission
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]


def authenticate_with_send_scope(credentials_path: str, token_path: str):
    """Authenticate with Gmail API including send permission."""
    
    credentials_path = Path(credentials_path)
    token_path = Path(token_path)
    
    print()
    print('=' * 70)
    print('  GMAIL AUTHENTICATION - WITH SEND PERMISSION')
    print('=' * 70)
    print()
    print('This will authenticate with BOTH read AND send permissions.')
    print()
    
    # Delete old token
    if token_path.exists():
        print('[INFO] Deleting old token (read-only)...')
        token_path.unlink()
        print('[OK] Old token deleted')
        print()
    
    # Create flow
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path,
        SCOPES
    )
    
    # Run local server flow (opens browser automatically)
    print('[INFO] Opening browser for authentication...')
    print('[INFO] Please sign in and grant permissions...')
    print()
    
    try:
        creds = flow.run_local_server(
            port=0,
            host='localhost',
            open_browser=True,
            authorization_prompt_message='Opening browser... ',
            success_message='Authentication successful! Closing browser...'
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
        print('Scopes granted:')
        print('  ✓ gmail.readonly - Read emails')
        print('  ✓ gmail.send - Send emails')
        print()
        print('You can now send emails with:')
        print('  python email_mcp_server.py "../AI_Employee_Vault" "../credeintals.json"')
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
        print('Please try again.')
        return False


def main():
    if len(sys.argv) < 2:
        print('Usage: python gmail_auth_send.py <credentials.json>')
        sys.exit(1)
    
    credentials_path = sys.argv[1]
    vault_logs = Path(credentials_path).parent.parent / 'AI_Employee_Vault' / 'Logs'
    token_path = vault_logs / 'gmail_token.pickle'
    
    success = authenticate_with_send_scope(credentials_path, str(token_path))
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
