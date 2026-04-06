"""
Email MCP Server for AI Employee

Sends emails via Gmail API after human approval.

Usage:
    python email_mcp_server.py "D:/path/to/credeintals.json"

This server listens for approval files and sends emails automatically.
"""

import sys
import pickle
import json
import base64
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class EmailMCPServer:
    def __init__(self, vault_path: str, credentials_path: str):
        self.vault = Path(vault_path).resolve()
        self.credentials_path = Path(credentials_path)
        # Try multiple token locations
        self.token_path = self.vault / 'Logs' / 'gmail_token.pickle'
        if not self.token_path.exists():
            self.token_path = Path('D:/Download/working_hackthoon_zero_0/AI_Employee_Vault/Logs/gmail_token.pickle')
        
        self.approved = self.vault / 'Approved'
        self.done = self.vault / 'Done'
        self.logs_folder = self.vault / 'Logs'
        
        for folder in [self.approved, self.done, self.logs_folder]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Authenticate
        self.service = self._authenticate()
        
        print()
        print('=' * 70)
        print('  EMAIL MCP SERVER - Ready to Send')
        print('=' * 70)
        print()
        print(f'[OK] Connected to Gmail API')
        print(f'[OK] Monitoring: {self.approved}')
        print()
    
    def _authenticate(self):
        """Authenticate with Gmail API."""
        creds = None
        
        if self.token_path.exists():
            with open(self.token_path, 'rb') as f:
                creds = pickle.load(f)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                from google.auth.transport.requests import Request
                creds.refresh(Request())
            else:
                raise Exception('Gmail token not found or expired. Run gmail_watcher.py first.')
        
        return build('gmail', 'v1', credentials=creds)
    
    def send_email(self, to: str, subject: str, body: str, html: bool = False) -> bool:
        """Send email via Gmail API."""
        
        print(f'[INFO] Sending email to: {to}')
        print(f'[INFO] Subject: {subject}')
        
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['to'] = to
            message['subject'] = subject
            
            # Add body
            if html:
                message.attach(MIMEText(body, 'html'))
            else:
                message.attach(MIMEText(body, 'plain'))
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send
            sent_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            print(f'[OK] Email sent! Message ID: {sent_message["id"]}')
            return True
            
        except Exception as e:
            print(f'[ERROR] Failed to send: {e}')
            return False
    
    def check_approved_emails(self) -> int:
        """Check for approved email actions and send them."""
        
        approved_files = [f for f in self.approved.iterdir() 
                         if f.suffix == '.md' and 'APPROVAL' in f.name and 'email' in f.name.lower()]
        
        if not approved_files:
            print('[INFO] No approved emails to send')
            return 0
        
        print(f'[INFO] Found {len(approved_files)} approved email(s) to send')
        
        sent = 0
        for approval_file in approved_files:
            print()
            print(f'Processing: {approval_file.name}')
            
            # Parse approval file
            data = self._parse_approval_file(approval_file)
            
            if data and data.get('action') == 'send_email':
                success = self.send_email(
                    to=data.get('to', ''),
                    subject=data.get('subject', ''),
                    body=data.get('body', ''),
                    html=data.get('html', False)
                )
                
                if success:
                    # Move to Done
                    approval_file.rename(self.done / approval_file.name)
                    print(f'[OK] Moved to Done: {approval_file.name}')
                    sent += 1
                    
                    # Log the action
                    self._log_action(approval_file, data, 'sent')
                else:
                    print(f'[ERROR] Failed to send: {approval_file.name}')
        
        return sent
    
    def _parse_approval_file(self, filepath: Path) -> dict:
        """Parse approval request file."""
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Parse frontmatter
        in_frontmatter = False
        frontmatter_lines = []
        
        for line in lines:
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break
            
            if in_frontmatter:
                frontmatter_lines.append(line)
        
        # Parse YAML manually (simple version)
        data = {}
        for line in frontmatter_lines:
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
        
        # Extract email body from content
        in_body = False
        body_lines = []
        
        for line in lines:
            if line.strip() == '## Email Body' or line.strip() == '## Body':
                in_body = True
                continue
            if in_body:
                if line.startswith('##') and line.strip() != '## Email Body':
                    break
                body_lines.append(line)
        
        data['body'] = '\n'.join(body_lines).strip()
        
        return data
    
    def _log_action(self, filepath: Path, data: dict, status: str):
        """Log email action."""
        log_file = self.logs_folder / f'email_mcp_{datetime.now().strftime("%Y-%m-%d")}.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': 'send_email',
            'to': data.get('to', ''),
            'subject': data.get('subject', ''),
            'status': status,
            'file': filepath.name
        }
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')


def main():
    if len(sys.argv) < 3:
        print('Usage: python email_mcp_server.py <vault_path> <credentials_path>')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    credentials_path = sys.argv[2]
    
    try:
        server = EmailMCPServer(vault_path, credentials_path)
        
        # Check for approved emails
        sent = server.check_approved_emails()
        
        print()
        print('=' * 70)
        print(f'  COMPLETED: {sent} email(s) sent')
        print('=' * 70)
        print()
        
    except Exception as e:
        print(f'[ERROR] {e}')
        print()
        print('Make sure:')
        print('  1. Gmail token exists (run gmail_watcher.py first)')
        print('  2. Credentials file is valid')
        sys.exit(1)


if __name__ == '__main__':
    main()
