"""
Get Authorization URL for Gmail Send Scope
Run this to get a fresh URL, then use exchange_code.py with the code
"""

from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

flow = InstalledAppFlow.from_client_secrets_file(
    'D:/Download/working_hackthoon_zero_0/credeintals.json',
    SCOPES,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
)

auth_url, _ = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    prompt='consent'
)

print()
print('=' * 70)
print('  GMAIL SEND PERMISSION - AUTHORIZATION URL')
print('=' * 70)
print()
print('STEP 1: Open this URL in your browser:')
print()
print(auth_url)
print()
print('STEP 2: Sign in and GRANT ALL PERMISSIONS (including Send emails)')
print()
print('STEP 3: Copy the authorization code (starts with 4/...)')
print()
print('STEP 4: Run exchange_code.py with your code:')
print('  python exchange_code.py YOUR_CODE_HERE')
print()
print('=' * 70)
print()
print('Keep this window open and run exchange_code.py in another window!')
print()
