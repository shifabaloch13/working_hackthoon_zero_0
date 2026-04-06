"""
Vault Sync System for Platinum Tier

Handles Git-based synchronization between Cloud and Local vaults.
Implements claim-by-move rule to prevent double-work.

Usage:
    python vault_sync.py --mode cloud  # or local
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List


class VaultSync:
    """Git-based vault synchronization."""

    def __init__(self, vault_path: str, mode: str = 'local'):
        self.vault = Path(vault_path).resolve()
        self.mode = mode  # 'cloud' or 'local'
        self.git_dir = self.vault.parent
        
        # Sync-safe folders (these sync between cloud and local)
        self.sync_folders = [
            'Needs_Action',
            'Plans',
            'Updates',
            'Done',
            'Logs',
            'Briefings'
        ]
        
        # Local-only folders (never sync)
        self.local_only = [
            '.env',
            '*.pem',
            '*.key',
            'credentials.json',
            'facebook_config.json',
            'odoo_config.json',
            'whatsapp_session'
        ]

    def pull(self) -> bool:
        """Pull latest changes from remote."""
        print(f"[{self.mode}] Pulling from Git...")
        try:
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                cwd=self.git_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"[{self.mode}] Pull successful")
                return True
            else:
                print(f"[{self.mode}] Pull failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"[{self.mode}] Pull error: {e}")
            return False

    def push(self) -> bool:
        """Push changes to remote."""
        print(f"[{self.mode}] Pushing to Git...")
        try:
            # Check for changes
            result = subprocess.run(
                ['git', 'diff-index', '--quiet', 'HEAD'],
                cwd=self.git_dir
            )
            
            if result.returncode != 0:
                # There are changes
                subprocess.run(
                    ['git', 'add', '-A'],
                    cwd=self.git_dir,
                    timeout=30
                )
                
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                subprocess.run(
                    ['git', 'commit', '-m', f'{self.mode} sync: {timestamp}'],
                    cwd=self.git_dir,
                    timeout=30
                )
                
                subprocess.run(
                    ['git', 'push', 'origin', 'main'],
                    cwd=self.git_dir,
                    timeout=60
                )
                
                print(f"[{self.mode}] Push successful")
                return True
            else:
                print(f"[{self.mode}] No changes to push")
                return True
        except Exception as e:
            print(f"[{self.mode}] Push error: {e}")
            return False

    def merge_updates(self) -> List[str]:
        """Merge Cloud updates into Local dashboard."""
        print(f"[{self.mode}] Merging updates...")
        
        updates_folder = self.vault / 'Updates'
        merged = []
        
        if not updates_folder.exists():
            return merged
        
        for update_file in updates_folder.glob('*.md'):
            content = update_file.read_text(encoding='utf-8')
            
            # Process update based on type
            if 'email_reply_draft' in content:
                # Move to Pending_Approval for human review
                dest = self.vault / 'Pending_Approval' / update_file.name
                update_file.rename(dest)
                merged.append(update_file.name)
                print(f"  Merged: {update_file.name}")
            
            elif 'social_post_draft' in content:
                # Move to Pending_Approval for human review
                dest = self.vault / 'Pending_Approval' / update_file.name
                update_file.rename(dest)
                merged.append(update_file.name)
                print(f"  Merged: {update_file.name}")
        
        return merged


class ClaimByMoveRule:
    """Implements claim-by-move rule to prevent double-work."""

    def __init__(self, vault_path: str, agent_name: str):
        self.vault = Path(vault_path).resolve()
        self.agent_name = agent_name
        self.in_progress = self.vault / 'In_Progress' / agent_name
        
        # Ensure in_progress folder exists
        self.in_progress.mkdir(parents=True, exist_ok=True)

    def claim(self, item_path: Path) -> Optional[Path]:
        """
        Claim an item by moving it to agent's in_progress folder.
        
        Returns the new path if claimed successfully, None if already claimed.
        """
        # Check if item is already in some in_progress folder
        for agent_folder in (self.vault / 'In_Progress').iterdir():
            if agent_folder.is_dir():
                claimed_item = agent_folder / item_path.name
                if claimed_item.exists():
                    print(f"[{self.agent_name}] Item already claimed by {agent_folder.name}")
                    return None
        
        # Move to our in_progress folder
        try:
            dest = self.in_progress / item_path.name
            item_path.rename(dest)
            print(f"[{self.agent_name}] Claimed: {item_path.name}")
            return dest
        except Exception as e:
            print(f"[{self.agent_name}] Failed to claim: {e}")
            return None

    def release(self, item_name: str, destination: str):
        """
        Release a claimed item to destination (Done, Approved, etc).
        """
        item_path = self.in_progress / item_name
        
        if not item_path.exists():
            print(f"[{self.agent_name}] Item not found: {item_name}")
            return
        
        try:
            if destination == 'done':
                dest = self.vault / 'Done' / item_name
            elif destination == 'approved':
                dest = self.vault / 'Approved' / item_name
            else:
                dest = Path(destination) / item_name
            
            item_path.rename(dest)
            print(f"[{self.agent_name}] Released {item_name} to {destination}")
        except Exception as e:
            print(f"[{self.agent_name}] Failed to release: {e}")

    def get_claimed_items(self) -> List[Path]:
        """Get all items claimed by this agent."""
        if not self.in_progress.exists():
            return []
        
        return list(self.in_progress.glob('*.md'))


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Vault Sync System')
    parser.add_argument('--mode', choices=['cloud', 'local'], required=True,
                       help='Running mode (cloud or local)')
    parser.add_argument('--vault', default='../AI_Employee_Vault',
                       help='Path to vault')
    parser.add_argument('--action', choices=['pull', 'push', 'merge', 'sync'],
                       default='sync', help='Action to perform')
    
    args = parser.parse_args()
    
    sync = VaultSync(args.vault, args.mode)
    
    if args.action == 'pull':
        sync.pull()
    elif args.action == 'push':
        sync.push()
    elif args.action == 'merge':
        sync.merge_updates()
    elif args.action == 'sync':
        sync.pull()
        if args.mode == 'local':
            sync.merge_updates()
        sync.push()


if __name__ == '__main__':
    main()
