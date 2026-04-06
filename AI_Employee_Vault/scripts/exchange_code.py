"""
Exchange authorization code for token with Gmail Send scope
Usage: python exchange_code.py YOUR_AUTH_CODE
"""

import sys
import requests
import pickle
import json
from pathlib import Path

if len(sys.argv) < 2:
    print('Usage: python exchange_code.py <authorization_code>')
    print()
    print('First run: python get_url.py')
    print('Then run this with the code you get')
    sys.exit(1)

code = sys.argv[1]

# Load client config
client_config = json.load(open('D:/Download/working_hackthoon_zero_0/credeintals.json'))

# Exchange code for token
token_url = 'https://oauth2.googleapis.com/token'
data = {
    'code': code,
    'client_id': client_config['installed']['client_id'],
    'client_secret': client_config['installed']['client_secret'],
    'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
    'grant_type': 'authorization_code'
}

print('[INFO] Exchanging code for token...')
resp = requests.post(token_url, data=data)

if resp.status_code == 200:
    token_data = resp.json()
    print('[OK] Token received!')
    
    # Create credentials
    from google.oauth2.credentials import Credentials
    creds = Credentials(
        token=token_data.get('access_token'),
        refresh_token=token_data.get('refresh_token'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_config['installed']['client_id'],
        client_secret=client_config['installed']['client_secret'],
        scopes=['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
    )
    
    # Save token
    token_path = Path('D:/Download/working_hackthoon_zero_0/AI_Employee_Vault/Logs/gmail_token.pickle')
    token_path.parent.mkdir(parents=True, exist_ok=True)
    pickle.dump(creds, open(token_path, 'wb'))
    
    print()
    print('=' * 70)
    print('  SUCCESS! Token saved with SEND permission')
    print('=' * 70)
    print()
    print('Now you can send emails:')
    print('  python email_mcp_server.py "../AI_Employee_Vault" "../credeintals.json"')
    print()
else:
    print(f'[ERROR] Failed: {resp.status_code}')
    print(resp.text)
