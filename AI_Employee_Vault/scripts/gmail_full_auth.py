"""
Complete Gmail Auth with Send Permission - Single Script
Opens browser, gets code, exchanges for token automatically
"""

import sys
import pickle
import json
import webbrowser
import time
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from google.oauth2.credentials import Credentials

# Configuration
CREDENTIALS_FILE = 'D:/Download/working_hackthoon_zero_0/credeintals.json'
TOKEN_FILE = 'D:/Download/working_hackthoon_zero_0/AI_Employee_Vault/Logs/gmail_token.pickle'
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

class AuthHandler(BaseHTTPRequestHandler):
    code = None
    
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        if 'code' in params:
            self.code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Authentication Successful!</h1><p>You can close this window now.</p></body></html>')
        else:
            self.send_response(400)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logging

def main():
    print()
    print('=' * 70)
    print('  GMAIL AUTHENTICATION - SEND PERMISSION')
    print('=' * 70)
    print()
    
    # Load client config
    with open(CREDENTIALS_FILE, 'r') as f:
        client_config = json.load(f)
    
    client_id = client_config['installed']['client_id']
    client_secret = client_config['installed']['client_secret']
    
    # Build auth URL
    auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri=http://localhost:8085&"
        f"scope={'%20'.join(SCOPES)}&"
        f"response_type=code&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    
    print('[INFO] Opening browser for authentication...')
    print('[INFO] Please sign in and grant ALL permissions...')
    print()
    
    # Open browser
    webbrowser.open(auth_url)
    
    # Start local server to receive callback
    print('[INFO] Waiting for authentication callback...')
    print('[INFO] Please complete authentication in your browser...')
    print()
    
    server = HTTPServer(('localhost', 8085), AuthHandler)
    server.handle_request()
    
    code = AuthHandler.code
    
    if not code:
        print('[ERROR] No authorization code received')
        return
    
    print('[OK] Authorization code received!')
    print('[INFO] Exchanging code for token...')
    
    # Exchange code for token
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'http://localhost:8085',
        'grant_type': 'authorization_code'
    }
    
    import requests
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
        print(f'[OK] Token saved to: {token_path}')
        print()
        print('Scopes granted:')
        print('  ✓ gmail.readonly - Read emails')
        print('  ✓ gmail.send - Send emails')
        print()
        print('Now you can send emails!')
        print('  python email_mcp_server.py "../AI_Employee_Vault" "../credeintals.json"')
        print()
    else:
        print()
        print('=' * 70)
        print('  AUTHENTICATION FAILED')
        print('=' * 70)
        print()
        print(f'[ERROR] {resp.status_code}')
        print(resp.text)

if __name__ == '__main__':
    main()
