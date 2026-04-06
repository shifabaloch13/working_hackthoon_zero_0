"""
Gmail Debug Script - Check what emails are in your inbox

Usage:
    python gmail_debug.py "D:/path/to/credeintals.json"
"""

import sys
import pickle
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def debug_gmail(credentials_path: str):
    """Check Gmail for emails."""
    
    credentials_path = Path(credentials_path)
    vault_logs = credentials_path.parent.parent / 'AI_Employee_Vault' / 'Logs'
    token_path = vault_logs / 'gmail_token.pickle'
    
    # Load token
    if not token_path.exists():
        print('[ERROR] Gmail token not found. Run gmail_watcher.py first.')
        return
    
    with open(token_path, 'rb') as f:
        creds = pickle.load(f)
    
    # Build Gmail service
    service = build('gmail', 'v1', credentials=creds)
    
    print()
    print('=' * 70)
    print('  GMAIL DEBUG - Checking Your Inbox')
    print('=' * 70)
    print()
    
    # Check ALL recent emails (not just unread)
    print('[INFO] Checking ALL recent emails in inbox...')
    results = service.users().messages().list(
        userId='me',
        maxResults=20
    ).execute()
    
    messages = results.get('messages', [])
    
    print(f'\n[OK] Found {len(messages)} recent emails\n')
    
    print('Recent Email IDs:')
    print('-' * 70)
    for i, msg in enumerate(messages[:10], 1):
        print(f'  {i}. {msg["id"]}')
    print('-' * 70)
    print()
    
    # Check unread emails
    print('[INFO] Checking UNREAD emails...')
    results = service.users().messages().list(
        userId='me',
        q='is:unread',
        maxResults=20
    ).execute()
    
    messages = results.get('messages', [])
    
    print(f'\n[OK] Found {len(messages)} unread emails\n')
    
    if messages:
        print('Unread Email Details:')
        print('-' * 70)
        
        for msg in messages[:10]:
            # Get full message details
            full_msg = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            
            headers = {h['name']: h['value'] for h in full_msg['payload']['headers']}
            
            # Remove ALL non-ASCII characters for Windows console
            from_safe = headers.get("From", "Unknown").encode('ascii', errors='ignore').decode('ascii', errors='ignore')
            subject_safe = headers.get("Subject", "No Subject").encode('ascii', errors='ignore').decode('ascii', errors='ignore')
            
            print(f'\nEmail ID: {msg["id"]}')
            print(f'  From: {from_safe}')
            print(f'  Subject: {subject_safe}')
            print(f'  Date: {headers.get("Date", "Unknown")}')
        
        print('-' * 70)
    else:
        print('[WARN] No unread emails found!')
        print()
        print('Possible reasons:')
        print('  1. Email was already marked as read')
        print('  2. Email is in a different folder (Spam, Promotions, etc.)')
        print('  3. Gmail API sync delay (wait 1-2 minutes)')
        print('  4. Email address mismatch (check recipient)')
    
    print()
    
    # Check state file
    state_file = vault_logs / 'gmail_watcher_state.txt'
    if state_file.exists():
        with open(state_file, 'r') as f:
            processed_ids = set(line.strip() for line in f if line.strip())
        
        print(f'[INFO] Processed email IDs in state file: {len(processed_ids)}')
        
        # Check if any unread emails are already processed
        if messages:
            already_processed = 0
            new_emails = 0
            
            for msg in messages:
                if msg['id'] in processed_ids:
                    already_processed += 1
                else:
                    new_emails += 1
            
            print(f'  - Already processed: {already_processed}')
            print(f'  - New (not processed): {new_emails}')
    
    print()
    print('=' * 70)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python gmail_debug.py <credentials.json>')
        sys.exit(1)
    
    debug_gmail(sys.argv[1])
