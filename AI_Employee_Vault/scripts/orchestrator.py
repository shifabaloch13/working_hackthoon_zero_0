"""
Orchestrator for AI Employee (Silver Tier)

Processes files in the Needs_Action folder and coordinates with Qwen Code.
Creates Plan.md files, manages approvals, and updates Dashboard.

Usage:
    python orchestrator.py /path/to/vault
    python orchestrator.py /path/to/vault --once
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Optional


class Orchestrator:
    """
    Main orchestrator for the AI Employee system.
    
    Responsibilities:
    - Monitor Needs_Action folder for new items
    - Create Plan.md files for complex tasks
    - Move completed items to Done folder
    - Update Dashboard.md with recent activity
    - Coordinate with approval workflow
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault root
        """
        self.vault_path = Path(vault_path).resolve()
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done_folder = self.vault_path / 'Done'
        self.plans_folder = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved_folder = self.vault_path / 'Approved'
        self.rejected_folder = self.vault_path / 'Rejected'
        self.dashboard = self.vault_path / 'Dashboard.md'
        self.logs_folder = self.vault_path / 'Logs'
        self.handbook = self.vault_path / 'Company_Handbook.md'
        
        # Ensure directories exist
        for folder in [self.done_folder, self.plans_folder, self.pending_approval, 
                       self.approved_folder, self.rejected_folder, self.logs_folder]:
            folder.mkdir(parents=True, exist_ok=True)
    
    def process_needs_action(self) -> int:
        """
        Process all files in the Needs_Action folder.
        
        Returns:
            Number of files processed
        """
        processed = 0
        
        if not self.needs_action.exists():
            return 0
        
        for filepath in self.needs_action.iterdir():
            if filepath.is_file() and filepath.suffix == '.md':
                self._process_file(filepath)
                processed += 1
        
        return processed
    
    def _process_file(self, filepath: Path):
        """
        Process a single action file with Qwen Code reasoning loop.
        
        Args:
            filepath: Path to the action file
        """
        content = filepath.read_text(encoding='utf-8')
        
        # Extract type from frontmatter
        file_type = self._extract_type(content)
        
        # Apply Qwen Code reasoning: analyze and create plan
        plan_path = self._create_plan_with_reasoning(filepath, file_type, content)
        
        # Check if approval is needed based on Company Handbook rules
        if self._requires_approval(file_type, content):
            self._create_approval_request(filepath, file_type, content)
        
        # Log the action
        self._log_action(filepath, file_type, 'processed')
        
        # Update dashboard
        self._update_dashboard(filepath, file_type)
        
        print(f'[OK] Processed: {filepath.name}')
        print(f'[OK] Plan created: {plan_path.name}')
    
    def _extract_type(self, content: str) -> str:
        """Extract the type from frontmatter."""
        for line in content.split('\n'):
            if line.startswith('type:'):
                return line.split(':')[1].strip()
        return 'unknown'
    
    def _create_plan_with_reasoning(self, action_file: Path, file_type: str, content: str) -> Path:
        """
        Create a Plan.md file using Qwen Code reasoning pattern.
        
        This implements the reasoning loop:
        1. Read and understand the action
        2. Determine required steps
        3. Check for approval requirements
        4. Create structured plan
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plan_filename = f'PLAN_{timestamp}_{action_file.stem}.md'
        plan_path = self.plans_folder / plan_filename
        
        # Extract key info for reasoning
        frontmatter = self._parse_frontmatter(content)
        priority = frontmatter.get('priority', 'normal')
        from_field = frontmatter.get('from', frontmatter.get('sender', 'Unknown'))
        subject = frontmatter.get('subject', 'No subject')
        
        # Determine steps based on type (Qwen Code reasoning pattern)
        steps = self._determine_steps(file_type, frontmatter)
        
        # Determine if approval needed
        approval_needed = self._check_approval_needed(file_type, frontmatter)
        
        plan_content = f'''---
created: {datetime.now().isoformat()}
status: pending
action_type: {file_type}
source_file: {action_file.name}
priority: {priority}
---

# Action Plan: {subject[:50]}

## Objective
Process the {file_type} action item from: `{action_file.name}`

## Context
- **Type**: {file_type}
- **From**: {from_field}
- **Priority**: {priority}
- **Subject**: {subject}

## Steps

{chr(10).join(f'- [ ] {step}' for step in steps)}

## Approval Required
{"Yes - " + approval_needed if approval_needed else "No"}

## Decisions Made

*Decisions will be documented here during execution*

## Notes

*Add notes during processing*

---
*Created by Orchestrator (Qwen Code AI Employee - Silver Tier)*
'''
        
        plan_path.write_text(plan_content, encoding='utf-8')
        return plan_path
    
    def _determine_steps(self, file_type: str, frontmatter: dict) -> list:
        """Determine processing steps based on file type (Qwen reasoning)."""
        
        steps_map = {
            'email': [
                'Read and understand the email content',
                'Identify sender intent and required response',
                'Check Company Handbook for response rules',
                'Draft response or take action',
                'Request approval if needed (new contacts, sensitive topics)',
                'Execute action after approval',
                'Log action and update Dashboard',
                'Move to Done folder'
            ],
            'whatsapp': [
                'Read WhatsApp message content',
                'Identify keywords and urgency',
                'Check Company Handbook for response rules',
                'Draft appropriate response',
                'Request approval if payment/invoice related',
                'Send response after approval',
                'Mark as read in WhatsApp',
                'Move to Done folder'
            ],
            'file_drop': [
                'Review file contents',
                'Categorize the file type',
                'Determine required action',
                'Execute action or create follow-up task',
                'Move to appropriate folder',
                'Archive or delete after processing'
            ],
            'social_post': [
                'Review post content for brand alignment',
                'Check for appropriate hashtags',
                'Verify image attachment if specified',
                'Request human approval (always required)',
                'Post to LinkedIn after approval',
                'Log engagement metrics',
                'Move to Done folder'
            ]
        }
        
        return steps_map.get(file_type, [
            'Read and understand the action item',
            'Determine required actions',
            'Check approval requirements',
            'Execute actions',
            'Update Dashboard',
            'Move to Done folder'
        ])
    
    def _check_approval_needed(self, file_type: str, frontmatter: dict) -> str:
        """Check if approval is needed based on rules."""
        
        # Email rules
        if file_type == 'email':
            # Check if new contact
            from_field = frontmatter.get('from', '')
            if 'new' in frontmatter.get('status', '') or '@' in from_field:
                return 'New contact requires approval'
        
        # Payment rules
        amount = frontmatter.get('amount', 0)
        if isinstance(amount, (int, float)) and amount > 500:
            return f'Payment over $500 (${amount})'
        
        # Social post rules
        if file_type == 'social_post':
            return 'Social posts always require approval'
        
        return ''
    
    def _requires_approval(self, file_type: str, content: str) -> bool:
        """Check if this item requires approval."""
        frontmatter = self._parse_frontmatter(content)
        
        # Social posts always need approval
        if file_type == 'social_post':
            return True
        
        # Check amount threshold
        amount = frontmatter.get('amount', 0)
        if isinstance(amount, (int, float)) and amount > 500:
            return True
        
        return False
    
    def _create_approval_request(self, filepath: Path, file_type: str, content: str):
        """Create approval request file for sensitive actions."""
        frontmatter = self._parse_frontmatter(content)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'APPROVAL_{timestamp}_{file_type}_{filepath.stem}.md'
        approval_path = self.pending_approval / filename
        
        amount = frontmatter.get('amount', 0)
        to_field = frontmatter.get('to', frontmatter.get('from', 'Unknown'))
        subject = frontmatter.get('subject', 'No subject')
        
        approval_content = f'''---
type: approval_request
action: {file_type}
created: {datetime.now().isoformat()}
expires: {(datetime.now() + timedelta(hours=24)).isoformat()}
priority: {frontmatter.get('priority', 'normal')}
status: pending
source_file: {filepath.name}
---

# Approval Request: {file_type.replace('_', ' ').title()}

## Details
- **Action Type**: {file_type}
- **From/To**: {to_field}
- **Subject**: {subject}
{f"- **Amount**: ${amount}" if amount else ""}

## Context
This action requires human approval before execution.
Source file: `{filepath.name}`

## To Approve
Move this file to `/Approved` folder.

## To Reject
Move this file to `/Rejected` folder with reason.

---
*Created by AI Employee Approval System*
*Requires human approval before execution*
'''
        
        # Import timedelta
        from datetime import timedelta
        
        approval_path.write_text(approval_content, encoding='utf-8')
        print(f'[INFO] Approval request created: {filename}')
    
    def _parse_frontmatter(self, content: str) -> dict:
        """Parse YAML frontmatter."""
        import yaml
        lines = content.split('\n')
        if lines[0].strip() != '---':
            return {}
        
        try:
            end = lines.index('---', 1)
            yaml_content = '\n'.join(lines[1:end])
            return yaml.safe_load(yaml_content) or {}
        except:
            return {}
    
    def _log_action(self, filepath: Path, action_type: str, status: str):
        """Log the action to the logs folder."""
        log_file = self.logs_folder / f'{datetime.now().strftime("%Y-%m-%d")}.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'actor': 'orchestrator',
            'source': filepath.name,
            'result': status
        }
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def _update_dashboard(self, filepath: Path, file_type: str):
        """Update the Dashboard.md with recent activity."""
        if not self.dashboard.exists():
            return
        
        content = self.dashboard.read_text(encoding='utf-8')
        
        # Add to recent activity section
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        activity_line = f'- [{timestamp}] Processed {file_type} item: {filepath.name}'
        
        # Find the Recent Activity section
        lines = content.split('\n')
        new_lines = []
        in_recent_activity = False
        added = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            if '## 📝 Recent Activity' in line or '## Recent Activity' in line:
                in_recent_activity = True
            elif in_recent_activity and not added:
                if line.strip() == '*No recent activity*':
                    new_lines[-1] = activity_line
                    added = True
                elif line.startswith('##'):
                    new_lines.insert(-1, activity_line)
                    new_lines.insert(-1, '')
                    added = True
        
        if not added:
            new_lines.append(activity_line)
        
        self.dashboard.write_text('\n'.join(new_lines), encoding='utf-8')
    
    def check_approvals(self) -> int:
        """
        Check for approved items ready for action.
        
        Returns:
            Number of approved items
        """
        if not self.approved_folder.exists():
            return 0
        
        approved = list(self.approved_folder.iterdir())
        print(f'[INFO] {len(approved)} approved item(s) ready for action')
        return len(approved)
    
    def run_once(self):
        """Run a single processing cycle."""
        print()
        print('=' * 60)
        print('  AI Employee Orchestrator - Silver Tier')
        print('=' * 60)
        print(f'[INFO] Running orchestration cycle...')
        print(f'[INFO] Vault: {self.vault_path}')
        
        # Check for approvals first
        self.check_approvals()
        
        # Process needs action
        processed = self.process_needs_action()
        
        if processed == 0:
            print('[INFO] No items to process')
        else:
            print(f'[OK] Processed {processed} item(s)')
        
        print(f'[OK] Dashboard updated: {self.dashboard.exists()}')
        print('=' * 60)


def main():
    """Main entry point for the orchestrator."""
    parser = argparse.ArgumentParser(
        description='Orchestrator for AI Employee (Silver Tier)'
    )
    parser.add_argument(
        'vault_path',
        type=str,
        help='Path to the Obsidian vault root'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit (default: run continuously)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Check interval in seconds (default: 60)'
    )
    
    args = parser.parse_args()
    
    vault_path = Path(args.vault_path).resolve()
    
    if not vault_path.exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    orchestrator = Orchestrator(str(vault_path))
    
    if args.once:
        orchestrator.run_once()
    else:
        import time
        print()
        print('=' * 60)
        print('  AI Employee Orchestrator - Silver Tier')
        print('=' * 60)
        print(f'[INFO] Starting Orchestrator')
        print(f'[INFO] Vault: {vault_path}')
        print(f'[INFO] Check interval: {args.interval}s')
        print()
        print('Press Ctrl+C to stop')
        print('=' * 60)
        print()
        
        try:
            while True:
                orchestrator.run_once()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print()
            print('[INFO] Orchestrator stopped by user')


if __name__ == '__main__':
    main()
