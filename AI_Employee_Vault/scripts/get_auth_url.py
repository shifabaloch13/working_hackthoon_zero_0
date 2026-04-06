"""
Get Gmail Authorization URL

Run this to get a fresh authorization URL.
Then use complete_auth.py with the code.

Usage:
    python get_auth_url.py "D:/path/to/credeintals.json"
"""

import sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_auth_url(credentials_path: str):
    """Generate authorization URL."""
    
    credentials_path = Path(credentials_path)
    
    if not credentials_path.exists():
        print(f'[ERROR] Credentials file not found: {credentials_path}')
        sys.exit(1)
    
    # Create flow
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path,
        SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    
    # Generate URL
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    print()
    print('=' * 70)
    print('  GMAIL AUTHORIZATION URL')
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
    print(f'  python complete_auth.py "{credentials_path}" "YOUR_CODE_HERE"')
    print()
    print('=' * 70)
    print()
    print('[INFO] Keep this terminal open while you authenticate')
    print('[INFO] Authorization codes expire quickly!')
    print()


def main():
    if len(sys.argv) < 2:
        print('Usage: python get_auth_url.py <credentials.json>')
        sys.exit(1)
    
    get_auth_url(sys.argv[1])


if __name__ == '__main__':
    main()
