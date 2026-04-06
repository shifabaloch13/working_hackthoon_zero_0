"""
Cloud Orchestrator for Platinum Tier AI Employee

Runs on cloud VM 24/7, handling:
- Email triage and draft creation
- Social media draft creation
- Git sync with local vault
- Health monitoring

Usage:
    python cloud_orchestrator.py
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/ai_employee_cloud.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('cloud_orchestrator')


class CloudOrchestrator:
    """Orchestrator for Cloud AI Employee."""

    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.needs_action = self.vault / 'Needs_Action' / 'cloud'
        self.updates = self.vault / 'Updates'
        self.in_progress = self.vault / 'In_Progress' / 'cloud_agent'
        self.done = self.vault / 'Done'
        self.logs_folder = self.vault / 'Logs'

        # Ensure folders exist
        for folder in [self.needs_action, self.updates, self.in_progress, self.done, self.logs_folder]:
            folder.mkdir(parents=True, exist_ok=True)

        logger.info(f'Cloud Orchestrator initialized')
        logger.info(f'Vault: {self.vault}')

    def sync_from_git(self):
        """Pull latest changes from Git."""
        logger.info('Syncing from Git...')
        try:
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                cwd=self.vault.parent,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                logger.info('Git sync successful')
            else:
                logger.warning(f'Git sync returned: {result.stderr}')
        except Exception as e:
            logger.error(f'Git sync failed: {e}')

    def sync_to_git(self):
        """Push changes to Git."""
        logger.info('Syncing to Git...')
        try:
            # Add changes
            subprocess.run(['git', 'add', '-A'], cwd=self.vault.parent, timeout=30)
            
            # Commit if there are changes
            result = subprocess.run(
                ['git', 'diff-index', '--quiet', 'HEAD'],
                cwd=self.vault.parent
            )
            
            if result.returncode != 0:  # There are changes
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                subprocess.run(
                    ['git', 'commit', '-m', f'Cloud sync: {timestamp}'],
                    cwd=self.vault.parent,
                    timeout=30
                )
                subprocess.run(
                    ['git', 'push', 'origin', 'main'],
                    cwd=self.vault.parent,
                    timeout=60
                )
                logger.info('Git sync successful')
            else:
                logger.info('No changes to sync')
        except Exception as e:
            logger.error(f'Git sync failed: {e}')

    def claim_item(self, item_path: Path) -> bool:
        """Claim an item by moving to in_progress."""
        try:
            dest = self.in_progress / item_path.name
            item_path.rename(dest)
            logger.info(f'Claimed: {item_path.name}')
            return True
        except Exception as e:
            logger.error(f'Failed to claim item: {e}')
            return False

    def complete_item(self, item_path: Path):
        """Complete an item by moving to done."""
        try:
            dest = self.done / item_path.name
            item_path.rename(dest)
            logger.info(f'Completed: {item_path.name}')
        except Exception as e:
            logger.error(f'Failed to complete item: {e}')

    def create_update(self, title: str, content: str) -> Path:
        """Create an update file for Local to review."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'UPDATE_{title}_{timestamp}.md'
        update_file = self.updates / filename

        update_file.write_text(content, encoding='utf-8')
        logger.info(f'Created update: {filename}')
        
        return update_file

    def process_email_triage(self):
        """Process email triage (draft only)."""
        logger.info('Processing email triage...')
        
        # Check for new emails in Needs_Action
        email_files = list(self.needs_action.glob('EMAIL_*.md'))
        
        for email_file in email_files:
            logger.info(f'Processing: {email_file.name}')
            
            # Claim the item
            if not self.claim_item(email_file):
                continue
            
            # Read email content
            content = email_file.read_text(encoding='utf-8')
            
            # Create draft reply (Cloud only drafts, Local sends)
            draft_content = f"""---
type: email_reply_draft
original: {email_file.name}
created: {datetime.now().isoformat()}
status: pending_approval
---

# Email Reply Draft

## Original Email
{content}

## Suggested Reply
[AI to generate reply based on content]

## To Send
Local agent must approve and send via MCP.
"""
            
            # Create update for Local
            self.create_update('EMAIL_REPLY', draft_content)
            
            # Mark as complete (draft created)
            self.complete_item(email_file)

    def process_social_drafts(self):
        """Create social media post drafts."""
        logger.info('Processing social media drafts...')
        
        # Check for social requests
        social_files = list(self.needs_action.glob('SOCIAL_*.md'))
        
        for social_file in social_files:
            logger.info(f'Processing: {social_file.name}')
            
            # Claim the item
            if not self.claim_item(social_file):
                continue
            
            # Read request
            content = social_file.read_text(encoding='utf-8')
            
            # Create draft post
            draft_content = f"""---
type: social_post_draft
original: {social_file.name}
created: {datetime.now().isoformat()}
platform: facebook
status: pending_approval
---

# Social Media Post Draft

## Request
{content}

## Suggested Post
[AI to generate post based on request]

## To Post
Local agent must approve and post via MCP.
"""
            
            # Create update for Local
            self.create_update('SOCIAL_POST', draft_content)
            
            # Mark as complete (draft created)
            self.complete_item(social_file)

    def run(self, sync_interval: int = 300):
        """Run the cloud orchestrator."""
        logger.info('Starting Cloud Orchestrator...')
        logger.info(f'Sync interval: {sync_interval} seconds')
        
        last_sync = 0
        
        while True:
            try:
                current_time = time.time()
                
                # Sync from Git periodically
                if current_time - last_sync > sync_interval:
                    self.sync_from_git()
                    last_sync = current_time
                
                # Process email triage
                self.process_email_triage()
                
                # Process social drafts
                self.process_social_drafts()
                
                # Sync to Git
                self.sync_to_git()
                
                # Wait before next cycle
                time.sleep(60)
                
            except KeyboardInterrupt:
                logger.info('Shutting down...')
                break
            except Exception as e:
                logger.error(f'Error in orchestrator: {e}')
                time.sleep(60)


def main():
    vault_path = os.getenv('VAULT_PATH', '../AI_Employee_Vault')
    
    if not Path(vault_path).exists():
        logger.error(f'Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    orchestrator = CloudOrchestrator(vault_path)
    orchestrator.run(sync_interval=300)


if __name__ == '__main__':
    main()
