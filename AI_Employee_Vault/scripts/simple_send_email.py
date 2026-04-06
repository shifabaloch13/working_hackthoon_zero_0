"""
Simple Email Sender

Uses the token from simple_gmail_auth.py
"""

import sys
import pickle
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def send_email(to, subject, body):
    """Send email using Gmail API"""
    
    # Load token
    token_path = Path('gmail_token.pickle')
    
    if not token_path.exists():
        print("❌ No token found!")
        print("Run: python simple_gmail_auth.py")
        return False
    
    with open(token_path, 'rb') as token:
        creds = pickle.load(token)
    
    # Build Gmail service
    service = build('gmail', 'v1', credentials=creds)
    
    # Create message
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    message['from'] = 'AI Employee'
    
    # Add body
    message.attach(MIMEText(body, 'plain'))
    
    # Encode message to base64
    import base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    
    try:
        # Send email
        sent_message = service.users().messages().send(
            userId='me',
            body={
                'raw': raw_message
            }
        ).execute()
        
        print()
        print("=" * 70)
        print("  ✅ EMAIL SENT SUCCESSFULLY!")
        print("=" * 70)
        print()
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Message ID: {sent_message['id']}")
        print()
        return True
        
    except Exception as e:
        print()
        print("=" * 70)
        print("  ❌ FAILED TO SEND")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        print("Try re-authenticating:")
        print("  python simple_gmail_auth.py")
        print()
        return False

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python simple_send_email.py <to> <subject> <body>")
        print()
        print("Example:")
        print('  python simple_send_email.py "test@example.com" "Test" "Hello!"')
        sys.exit(1)
    
    to = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    
    print()
    print("=" * 70)
    print("  SENDING EMAIL")
    print("=" * 70)
    print()
    
    success = send_email(to, subject, body)
    sys.exit(0 if success else 1)
