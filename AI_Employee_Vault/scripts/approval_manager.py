"""
Approval Workflow Manager for AI Employee (Silver Tier)

Human-in-the-Loop approval system for sensitive AI actions.
Files move through: Pending_Approval -> Approved -> Done or Rejected

Usage:
    python approval_manager.py "D:/path/to/vault" --check
    python approval_manager.py "D:/path/to/vault" --create --action send_email --to test@example.com
"""

import sys
import argparse
import shutil
import yaml
from pathlib import Path
from datetime import datetime, timedelta


class ApprovalManager:
    """
    Manages approval workflow for sensitive actions.
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize the approval manager.
        
        Args:
            vault_path: Path to the Obsidian vault root
        """
        self.vault = Path(vault_path).resolve()
        self.pending = self.vault / 'Pending_Approval'
        self.approved = self.vault / 'Approved'
        self.rejected = self.vault / 'Rejected'
        self.done = self.vault / 'Done'
        
        for folder in [self.pending, self.approved, self.rejected, self.done]:
            folder.mkdir(parents=True, exist_ok=True)
        
        self.logs_folder = self.vault / 'Logs'
        self.logs_folder.mkdir(parents=True, exist_ok=True)
    
    def create_approval_request(self, request_data: dict) -> Path:
        """
        Create an approval request file.
        
        Args:
            request_data: Dict with action details
                - action: Type of action (send_email, payment, social_post, etc.)
                - to/recipient: Target of action
                - amount: If payment
                - description: What this action does
                - priority: normal, high, urgent
                - expires_hours: When approval expires (default: 24)
        
        Returns:
            Path to the created approval file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        action_type = request_data.get('action', 'unknown')
        priority = request_data.get('priority', 'normal')
        
        # Create filename
        filename = f"APPROVAL_{timestamp}_{priority}_{action_type}.md"
        filepath = self.pending / filename
        
        # Calculate expiration
        expires_hours = request_data.get('expires_hours', 24)
        expires = (datetime.now() + timedelta(hours=expires_hours)).isoformat()
        
        content = self._format_request(request_data, expires)
        filepath.write_text(content, encoding='utf-8')
        
        self._log_action('create', filepath, request_data)
        
        return filepath
    
    def check_approvals(self) -> list:
        """
        Check for approved files ready for execution.
        
        Returns:
            List of approved file paths
        """
        approved_files = []
        
        for f in self.approved.iterdir():
            if f.suffix == '.md':
                # Check if expired
                content = f.read_text(encoding='utf-8')
                data = self._parse_frontmatter(content)
                
                expires = data.get('expires')
                if expires:
                    try:
                        expires_dt = datetime.fromisoformat(expires)
                        if datetime.now() > expires_dt:
                            # Expired - move back to pending or reject
                            self._log_action('expired', f, data)
                            continue
                    except:
                        pass
                
                approved_files.append(f)
        
        return approved_files
    
    def process_approved(self, approved_file: Path, executor) -> bool:
        """
        Process an approved file.
        
        Args:
            approved_file: Path to approved file
            executor: Object with execute(data) method
        
        Returns:
            True if successful
        """
        content = approved_file.read_text(encoding='utf-8')
        data = self._parse_frontmatter(content)
        
        try:
            # Execute the approved action
            result = executor.execute(data)
            
            # Move to Done
            shutil.move(str(approved_file), str(self.done / approved_file.name))
            
            self._log_action('executed', approved_file, data)
            
            return True
            
        except Exception as e:
            self._log_action('error', approved_file, {'error': str(e)})
            return False
    
    def reject_approval(self, approval_file: Path, reason: str = '') -> None:
        """
        Reject an approval request.
        
        Args:
            approval_file: Path to approval file
            reason: Reason for rejection
        """
        # Add rejection reason to file
        content = approval_file.read_text(encoding='utf-8')
        content += f'\n\n## Rejected\n\nReason: {reason}\nDate: {datetime.now().isoformat()}'
        
        # Move to Rejected folder
        approval_file.write_text(content, encoding='utf-8')
        shutil.move(str(approval_file), str(self.rejected / approval_file.name))
        
        self._log_action('rejected', approval_file, {'reason': reason})
    
    def list_pending(self) -> list:
        """
        List all pending approval requests.
        
        Returns:
            List of pending file info dicts
        """
        pending = []
        
        for f in self.pending.iterdir():
            if f.suffix == '.md':
                content = f.read_text(encoding='utf-8')
                data = self._parse_frontmatter(content)
                
                pending.append({
                    'file': f,
                    'action': data.get('action', 'unknown'),
                    'created': data.get('created', ''),
                    'expires': data.get('expires', ''),
                    'priority': data.get('priority', 'normal')
                })
        
        return pending
    
    def _format_request(self, data: dict, expires: str) -> str:
        """Format approval request as markdown."""
        action = data.get('action', 'unknown')
        priority = data.get('priority', 'normal')
        
        # Build details section
        details_lines = []
        for key, value in data.items():
            if key not in ['action', 'priority', 'expires_hours', 'description']:
                details_lines.append(f'- **{key.title()}**: {value}')
        
        details = '\n'.join(details_lines)
        description = data.get('description', 'No description provided')
        
        return f'''---
type: approval_request
action: {action}
created: {datetime.now().isoformat()}
expires: {expires}
priority: {priority}
status: pending
---

# Approval Request: {action.replace('_', ' ').title()}

## Description
{description}

## Details
{details}

## Instructions

### To Approve
1. Review the details above carefully
2. Move this file to `/Approved` folder

### To Reject
1. Add your reason for rejection
2. Move this file to `/Rejected` folder

---
*Created by AI Employee Approval System*
*Requires human approval before execution*
'''
    
    def _parse_frontmatter(self, content: str) -> dict:
        """Parse YAML frontmatter."""
        lines = content.split('\n')
        if lines[0].strip() != '---':
            return {}
        
        try:
            end = lines.index('---', 1)
            yaml_content = '\n'.join(lines[1:end])
            return yaml.safe_load(yaml_content) or {}
        except:
            return {}
    
    def _log_action(self, action: str, filepath: Path, data: dict):
        """Log approval action."""
        log_file = self.logs_folder / f'approval_{datetime.now().strftime("%Y-%m-%d")}.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'file': filepath.name,
            'data': data
        }
        
        import json
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')


def main():
    """Main entry point for the approval manager."""
    parser = argparse.ArgumentParser(
        description='Approval Workflow Manager for AI Employee',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    # Check for approved files
    python approval_manager.py "../AI_Employee_Vault" --check
    
    # List pending approvals
    python approval_manager.py "../AI_Employee_Vault" --list
    
    # Create approval request
    python approval_manager.py "../AI_Employee_Vault" --create \\
        --action send_email \\
        --to client@example.com \\
        --subject "Invoice #1234"
        '''
    )
    parser.add_argument(
        'vault_path',
        type=str,
        help='Path to the Obsidian vault root'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check for approved files'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List pending approvals'
    )
    parser.add_argument(
        '--create',
        action='store_true',
        help='Create approval request'
    )
    parser.add_argument(
        '--action',
        type=str,
        help='Action type (send_email, payment, social_post, etc.)'
    )
    parser.add_argument(
        '--to',
        type=str,
        help='Target (email recipient, payment recipient, etc.)'
    )
    parser.add_argument(
        '--amount',
        type=float,
        help='Amount (for payments)'
    )
    parser.add_argument(
        '--description',
        type=str,
        help='Description of the action'
    )
    parser.add_argument(
        '--priority',
        type=str,
        choices=['normal', 'high', 'urgent'],
        default='normal',
        help='Priority level'
    )
    
    args = parser.parse_args()
    
    manager = ApprovalManager(args.vault_path)
    
    if args.check:
        approved = manager.check_approvals()
        print(f'[INFO] Found {len(approved)} approved file(s):')
        for f in approved:
            print(f'  - {f.name}')
    
    elif args.list:
        pending = manager.list_pending()
        print(f'[INFO] Found {len(pending)} pending approval(s):')
        for p in pending:
            print(f'  [{p["priority"]}] {p["action"]} - {p["file"].name}')
    
    elif args.create:
        if not args.action:
            print('[ERROR] --action is required for --create')
            sys.exit(1)
        
        request_data = {
            'action': args.action,
            'priority': args.priority,
            'description': args.description or f'{args.action} action'
        }
        
        if args.to:
            request_data['to'] = args.to
        if args.amount:
            request_data['amount'] = args.amount
        
        filepath = manager.create_approval_request(request_data)
        print(f'[OK] Approval request created: {filepath.name}')
        print('[INFO] Move file to /Approved to execute')
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
