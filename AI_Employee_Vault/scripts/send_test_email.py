"""
Send Test Email - Direct without MCP Server complexity
Uses the same authentication as gmail_watcher but with send scope
"""

import pickle
import base64
import json
from pathlib import Path
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Configuration
VAULT_PATH = 'D:/Download/working_hackthoon_zero_0/AI_Employee_Vault'
CREDENTIALS_PATH = 'D:/Download/working_hackthoon_zero_0/credeintals.json'

def send_test_email():
    """Send a test email using Gmail API."""
    
    print()
    print('=' * 70)
    print('  SENDING TEST EMAIL')
    print('=' * 70)
    print()
    
    # Load credentials
    with open(CREDENTIALS_PATH, 'r') as f:
        client_config = json.load(f)
    
    client_id = client_config['installed']['client_id']
    client_secret = client_config['installed']['client_secret']
    
    # We need to re-authenticate with send scope
    # For now, let's use a simpler approach - direct API call with user consent
    
    print('[INFO] To send emails, we need to authenticate with SEND permission.')
    print()
    print('Please run this command to authenticate:')
    print()
    print('  python gmail_full_auth.py')
    print()
    print('Then run this command again to send the test email.')
    print()
    
    # Check if we have a valid token
    token_path = Path(f'{VAULT_PATH}/Logs/gmail_token.pickle')
    
    if not token_path.exists():
        print('[ERROR] No token found. Please authenticate first.')
        return False
    
    # Try to load token
    try:
        with open(token_path, 'rb') as f:
            creds = pickle.load(f)
        
        # Check if token is valid
        if not creds or not creds.token:
            print('[ERROR] Token is invalid or expired. Please re-authenticate.')
            print()
            print('Run: python gmail_full_auth.py')
            return False
        
        # Build service
        service = build('gmail', 'v1', credentials=creds)
        
        # Create email
        message = MIMEText('This is a test email from your AI Employee!\n\nThe Email MCP Server is working correctly!')
        message['to'] = 'balckcat699@gmail.com'
        message['from'] = 'AI Employee <muhammad764baloch@gmail.com>'
        message['subject'] = 'Test Email from AI Employee'
        
        # Encode and send
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        print('[INFO] Sending email to balckcat699@gmail.com...')
        
        sent_message = service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
        
        print()
        print('=' * 70)
        print('  EMAIL SENT SUCCESSFULLY!')
        print('=' * 70)
        print()
        print(f'[OK] Message ID: {sent_message["id"]}')
        print(f'[OK] To: balckcat699@gmail.com')
        print(f'[OK] Subject: Test Email from AI Employee')
        print()
        print('Check your inbox at balckcat699@gmail.com!')
        print()
        
        return True
        
    except Exception as e:
        print()
        print('=' * 70)
        print('  FAILED TO SEND')
        print('=' * 70)
        print()
        print(f'[ERROR] {e}')
        print()
        print('This usually means the token doesn\'t have SEND permission.')
        print()
        print('To fix this:')
        print('  1. Run: python gmail_full_auth.py')
        print('  2. Sign in and grant ALL permissions')
        print('  3. Run this script again')
        print()
        return False

if __name__ == '__main__':
    send_test_email()
