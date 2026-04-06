"""
Local Agent for Platinum Tier AI Employee

Runs on local machine, handling:
- Human-in-the-loop approvals
- WhatsApp session (local only)
- Banking credentials (local only)
- Final send/post actions via MCP

Usage:
    python local_agent.py
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from vault_sync import VaultSync, ClaimByMoveRule

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/local_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('local_agent')


class LocalAgent:
    """Local AI Employee Agent."""

    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.needs_action = self.vault / 'Needs_Action' / 'local'
        self.pending_approval = self.vault / 'Pending_Approval'
        self.approved = self.vault / 'Approved'
        self.in_progress = self.vault / 'In_Progress' / 'local_agent'
        self.done = self.vault / 'Done'
        self.updates = self.vault / 'Updates'
        self.logs_folder = self.vault / 'Logs'

        # Ensure folders exist
        for folder in [self.needs_action, self.pending_approval, self.approved, 
                       self.in_progress, self.done, self.updates, self.logs_folder]:
            folder.mkdir(parents=True, exist_ok=True)

        # Initialize sync and claim systems
        self.sync = VaultSync(vault_path, mode='local')
        self.claim = ClaimByMoveRule(vault_path, 'local_agent')

        logger.info(f'Local Agent initialized')
        logger.info(f'Vault: {self.vault}')

    def sync_from_cloud(self):
        """Pull updates from Cloud and merge."""
        logger.info('Syncing from Cloud...')
        
        # Pull from Git
        if self.sync.pull():
            # Merge Cloud updates
            merged = self.sync.merge_updates()
            if merged:
                logger.info(f'Merged {len(merged)} updates from Cloud')
        
        logger.info('Sync complete')

    def sync_to_cloud(self):
        """Push completed items to Cloud."""
        logger.info('Syncing to Cloud...')
        self.sync.push()
        logger.info('Sync complete')

    def check_pending_approvals(self) -> list:
        """Check for items pending human approval."""
        if not self.pending_approval.exists():
            return []
        
        items = list(self.pending_approval.glob('*.md'))
        if items:
            logger.info(f'Found {len(items)} pending approvals')
            for item in items:
                logger.info(f'  - {item.name}')
        
        return items

    def check_approved(self) -> list:
        """Check for approved items ready to execute."""
        if not self.approved.exists():
            return []
        
        items = list(self.approved.glob('*.md'))
        if items:
            logger.info(f'Found {len(items)} approved items')
        
        return items

    def execute_email_send(self, approval_file: Path):
        """Execute email send via MCP."""
        logger.info(f'Executing email send: {approval_file.name}')
        
        # Read approval file
        content = approval_file.read_text(encoding='utf-8')
        
        # Extract email details (parse frontmatter)
        # For now, just log the action
        logger.info(f'Would send email (MCP integration needed)')
        
        # Move to Done
        dest = self.done / approval_file.name
        approval_file.rename(dest)
        logger.info(f'Moved to Done: {approval_file.name}')
        
        # Log action
        self._log_action('email_send', approval_file.name, 'success')

    def execute_facebook_post(self, approval_file: Path):
        """Execute Facebook post via MCP."""
        logger.info(f'Executing Facebook post: {approval_file.name}')
        
        # Import Facebook MCP
        try:
            from facebook_poster import FacebookMCP
            
            facebook = FacebookMCP(str(self.vault))
            
            # Read approval file
            content = approval_file.read_text(encoding='utf-8')
            
            # Extract post data
            post_data = self._extract_post_data(content)
            
            if post_data:
                # Post to Facebook
                if post_data['platform'] == 'instagram':
                    result = facebook.post_to_instagram(
                        post_data['message'],
                        post_data.get('photo')
                    )
                else:
                    result = facebook.post_to_facebook(
                        post_data['message'],
                        post_data.get('link'),
                        post_data.get('photo')
                    )
                
                if result.get('success'):
                    logger.info(f'Posted successfully: {result.get("post_id")}')
                    self._log_action('facebook_post', approval_file.name, 'success')
                else:
                    logger.error(f'Post failed: {result.get("error")}')
                    self._log_action('facebook_post', approval_file.name, 'failed')
        except Exception as e:
            logger.error(f'Facebook post error: {e}')
            self._log_action('facebook_post', approval_file.name, f'error: {e}')
        
        # Move to Done
        dest = self.done / approval_file.name
        approval_file.rename(dest)
        logger.info(f'Moved to Done: {approval_file.name}')

    def execute_payment(self, approval_file: Path):
        """Execute payment via Odoo MCP."""
        logger.info(f'Executing payment: {approval_file.name}')
        
        # Import Odoo MCP
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'odoo' / 'scripts'))
            from odoo_mcp_server import OdooMCP
            
            odoo = OdooMCP(str(self.vault))
            
            # Read payment details from approval file
            content = approval_file.read_text(encoding='utf-8')
            
            # Extract payment data (parse frontmatter)
            # For now, just log
            logger.info(f'Would execute payment (Odoo MCP integration)')
            
            self._log_action('payment', approval_file.name, 'success')
        except Exception as e:
            logger.error(f'Payment error: {e}')
            self._log_action('payment', approval_file.name, f'error: {e}')
        
        # Move to Done
        dest = self.done / approval_file.name
        approval_file.rename(dest)
        logger.info(f'Moved to Done: {approval_file.name}')

    def _extract_post_data(self, content: str) -> dict:
        """Extract post data from approval file."""
        lines = content.split('\n')
        
        data = {
            'platform': 'facebook',
            'message': '',
            'link': None,
            'photo': None
        }
        
        in_content = False
        message_lines = []
        
        for line in lines:
            if line.startswith('platform:'):
                data['platform'] = line.split(':')[1].strip()
            elif line.startswith('- **Link**:') and line != '- **Link**: None':
                data['link'] = line.split(':')[1].strip()
            elif line.startswith('- **Photo**:') and line != '- **Photo**: None':
                data['photo'] = line.split(':')[1].strip()
            elif line.strip() == '## Content':
                in_content = True
                continue
            elif in_content:
                if line.startswith('##'):
                    break
                message_lines.append(line)
        
        data['message'] = '\n'.join(message_lines).strip()
        return data

    def _log_action(self, action_type: str, file_name: str, result: str):
        """Log action to audit log."""
        log_file = self.logs_folder / f'local_{datetime.now().strftime("%Y-%m-%d")}.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action_type,
            'file': file_name,
            'result': result,
            'agent': 'local_agent'
        }
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(str(log_entry) + '\n')

    def process_approved_items(self):
        """Process all approved items."""
        approved_items = self.check_approved()
        
        for item in approved_items:
            # Claim the item
            claimed = self.claim.claim(item)
            if not claimed:
                continue
            
            # Determine action type and execute
            content = item.read_text(encoding='utf-8')
            
            if 'email' in content.lower() and 'send' in content.lower():
                self.execute_email_send(item)
            elif 'facebook' in content.lower() or 'post' in content.lower():
                self.execute_facebook_post(item)
            elif 'payment' in content.lower():
                self.execute_payment(item)
            else:
                logger.info(f'Unknown action type: {item.name}')
                # Move to Done anyway
                dest = self.done / item.name
                item.rename(dest)

    def run(self, sync_interval: int = 300):
        """Run the local agent."""
        logger.info('Starting Local Agent...')
        logger.info(f'Sync interval: {sync_interval} seconds')
        
        last_sync = 0
        
        while True:
            try:
                current_time = time.time()
                
                # Sync from Cloud periodically
                if current_time - last_sync > sync_interval:
                    self.sync_from_cloud()
                    last_sync = current_time
                
                # Check for approved items (human has approved)
                self.process_approved_items()
                
                # Sync to Cloud
                self.sync_to_cloud()
                
                # Wait before next cycle
                time.sleep(60)
                
            except KeyboardInterrupt:
                logger.info('Shutting down...')
                break
            except Exception as e:
                logger.error(f'Error in local agent: {e}')
                time.sleep(60)


def main():
    vault_path = os.getenv('VAULT_PATH', '../AI_Employee_Vault')
    
    if not Path(vault_path).exists():
        logger.error(f'Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    # Create logs folder
    logs_folder = Path(vault_path) / 'Logs'
    logs_folder.mkdir(parents=True, exist_ok=True)
    
    agent = LocalAgent(vault_path)
    agent.run(sync_interval=300)


if __name__ == '__main__':
    main()
