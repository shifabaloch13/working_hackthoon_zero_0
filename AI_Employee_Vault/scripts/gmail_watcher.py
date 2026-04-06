"""
Gmail Watcher for AI Employee (Silver Tier)

Monitors Gmail for new unread emails and creates action files in Obsidian vault.
Uses Gmail API with OAuth 2.0 authentication.

Usage:
    python gmail_watcher.py "D:/path/to/AI_Employee_Vault" "D:/path/to/credentials.json"

Dependencies:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
"""

import os
import sys
import pickle
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add scripts folder to path
sys.path.insert(0, str(Path(__file__).parent))

from base_watcher import BaseWatcher

# Gmail API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GmailWatcher(BaseWatcher):
    """
    Watches Gmail for new unread emails and creates action files.
    """
    
    # Gmail API scopes
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, vault_path: str, credentials_path: str, check_interval: int = 120):
        """
        Initialize the Gmail watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            credentials_path: Path to Gmail API credentials.json
            check_interval: Seconds between checks (default: 120)
        """
        super().__init__(vault_path, check_interval)
        
        self.credentials_path = Path(credentials_path)
        self.token_path = self.vault_path / 'Logs' / 'gmail_token.pickle'
        self.state_file = self.vault_path / 'Logs' / 'gmail_watcher_state.txt'
        
        # Track processed email IDs
        self.processed_ids = self._load_state()
        
        # Authenticate and build service
        self.service = self._authenticate()
        
        self.logger.info('Gmail Watcher initialized')
        self.logger.info(f'Credentials: {self.credentials_path}')
        self.logger.info(f'Vault: {self.vault_path}')
    
    def _authenticate(self):
        """Authenticate with Gmail API and return service object."""
        creds = None
        
        # Load token from file if exists
        if self.token_path.exists():
            try:
                with open(self.token_path, 'rb') as token:
                    creds = pickle.load(token)
                self.logger.info('Loaded existing Gmail token')
            except Exception as e:
                self.logger.warning(f'Could not load token: {e}')
                creds = None
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    self.logger.info('Refreshed Gmail credentials')
                except Exception as e:
                    self.logger.warning(f'Could not refresh credentials: {e}')
                    creds = None
            
            if not creds:
                if not self.credentials_path.exists():
                    raise FileNotFoundError(
                        f'Gmail credentials not found at: {self.credentials_path}\n'
                        f'Download credentials.json from Google Cloud Console'
                    )
                
                self.logger.info('Starting OAuth flow...')
                print()
                print('=' * 70)
                print('  GMAIL AUTHENTICATION REQUIRED')
                print('=' * 70)
                print()
                print('Since automatic browser opening may not work, please:')
                print()
                print('1. Run this command to get authorization URL:')
                print('   python get_auth_url.py "..\\..\\credeintals.json"')
                print()
                print('2. Open the URL in your browser')
                print()
                print('3. After granting access, copy the authorization code')
                print()
                print('4. Run this command with your code:')
                print('   python complete_auth.py "..\\..\\credeintals.json" "YOUR_CODE"')
                print()
                print('=' * 70)
                print()
                print('Alternatively, run the simple authentication:')
                print('   python simple_auth.py "..\\..\\credeintals.json"')
                print('   (This will open browser automatically)')
                print()
                sys.exit(0)
            
            # Save token for future use
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
                self.logger.info('Saved Gmail token')
        
        return build('gmail', 'v1', credentials=creds)
    
    def _load_state(self) -> set:
        """Load the set of processed email IDs."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return set(line.strip() for line in f if line.strip())
        return set()
    
    def _save_state(self):
        """Save the current state of processed email IDs."""
        with open(self.state_file, 'w') as f:
            f.write('\n'.join(self.processed_ids))
    
    def check_for_updates(self) -> list:
        """
        Check Gmail for new unread emails.
        
        Returns:
            List of email message dicts
        """
        try:
            # List unread messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=50
            ).execute()
            
            messages = results.get('messages', [])
            new_messages = []
            
            for msg in messages:
                if msg['id'] not in self.processed_ids:
                    # Get full message details
                    full_msg = self.service.users().messages().get(
                        userId='me',
                        id=msg['id'],
                        format='metadata',
                        metadataHeaders=['From', 'To', 'Subject', 'Date']
                    ).execute()
                    
                    new_messages.append(full_msg)
                    self.processed_ids.add(msg['id'])
            
            self._save_state()
            
            if new_messages:
                self.logger.info(f'Found {len(new_messages)} new emails')
            
            return new_messages
            
        except HttpError as error:
            self.logger.error(f'Gmail API error: {error}')
            return []
        except Exception as e:
            self.logger.error(f'Error checking Gmail: {e}')
            return []
    
    def create_action_file(self, message) -> Path:
        """
        Create a .md action file for the email.
        
        Args:
            message: Gmail message dict
            
        Returns:
            Path to the created action file
        """
        # Extract headers
        headers = {h['name']: h['value'] for h in message['payload']['headers']}
        
        from_email = headers.get('From', 'Unknown')
        subject = headers.get('Subject', 'No Subject')
        date = headers.get('Date', '')
        email_id = message['id']
        
        # Parse date
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(date)
            received = dt.isoformat()
        except:
            received = datetime.now().isoformat()
        
        # Create action file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_subject = ''.join(c for c in subject[:30] if c.isalnum() or c in ' -_').strip()
        filename = f'EMAIL_{timestamp}_{safe_subject}.md'
        filepath = self.needs_action / filename
        
        content = f'''---
type: email
from: {from_email}
subject: {subject}
received: {received}
email_id: {email_id}
priority: normal
status: pending
---

# Email: {subject}

## Sender
{from_email}

## Received
{received}

## Body
*Full email content available in Gmail*
Email ID: {email_id}

## Suggested Actions

- [ ] Read full email in Gmail
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
- [ ] Create follow-up task if needed

## Notes

*Add your notes here*

---
*Created by GmailWatcher (Qwen Code AI Employee)*
'''
        
        filepath.write_text(content, encoding='utf-8')
        # Remove emojis from log message to avoid Windows console encoding issues
        safe_from = from_email.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        safe_subject = subject.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        self.logger.info(f'Created action file for email from {safe_from}: {safe_subject}')
        
        return filepath


def main():
    """Main entry point for the Gmail watcher."""
    parser = argparse.ArgumentParser(
        description='Gmail Watcher for AI Employee',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    python gmail_watcher.py "../AI_Employee_Vault" "D:/credentials.json"
    python gmail_watcher.py "../AI_Employee_Vault" "D:/credentials.json" --interval 60
        '''
    )
    parser.add_argument(
        'vault_path',
        type=str,
        help='Path to the Obsidian vault root'
    )
    parser.add_argument(
        'credentials_path',
        type=str,
        help='Path to Gmail API credentials.json'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=120,
        help='Check interval in seconds (default: 120)'
    )
    parser.add_argument(
        '--query',
        type=str,
        default='is:unread',
        help='Gmail search query (default: is:unread)'
    )
    
    args = parser.parse_args()
    
    # Resolve to absolute path
    vault_path = Path(args.vault_path).resolve()
    credentials_path = Path(args.credentials_path).resolve()
    
    if not vault_path.exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    if not credentials_path.exists():
        print(f'[ERROR] Credentials file not found: {credentials_path}')
        print('Download credentials.json from Google Cloud Console')
        sys.exit(1)
    
    print('=' * 60)
    print('  Gmail Watcher - AI Employee (Silver Tier)')
    print('=' * 60)
    print(f'[INFO] Vault: {vault_path}')
    print(f'[INFO] Credentials: {credentials_path}')
    print(f'[INFO] Check interval: {args.interval}s')
    print(f'[INFO] Query: {args.query}')
    print()
    print('[INFO] First run will require OAuth authentication:')
    print('  1. Visit the URL shown in browser')
    print('  2. Sign in with your Google account')
    print('  3. Grant permissions')
    print('  4. Copy the code and paste in terminal')
    print()
    print('Press Ctrl+C to stop')
    print('=' * 60)
    print()
    
    try:
        watcher = GmailWatcher(str(vault_path), str(credentials_path), args.interval)
        print('[OK] Gmail Watcher started successfully!')
        print('[INFO] Monitoring Gmail for new emails...')
        print()
        watcher.run()
    except FileNotFoundError as e:
        print(f'[ERROR] {e}')
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print('[INFO] GmailWatcher stopped by user')
    except Exception as e:
        print(f'[ERROR] Fatal error: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
