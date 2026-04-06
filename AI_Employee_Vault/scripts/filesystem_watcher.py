"""
File System Watcher for AI Employee

Monitors a "Drop" folder for new files and creates action files in Needs_Action.
This is the simplest watcher to set up and perfect for Bronze tier.

Usage:
    python filesystem_watcher.py /path/to/vault

Or run continuously:
    python filesystem_watcher.py /path/to/vault --interval 30
"""

import sys
import argparse
import hashlib
from pathlib import Path
from datetime import datetime

from base_watcher import BaseWatcher


class FileSystemWatcher(BaseWatcher):
    """
    Watches a Drop folder for new files and creates action files.
    
    Files dropped into the Drop folder are copied to Needs_Action
    with accompanying metadata.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 30):
        """
        Initialize the file system watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 30)
        """
        super().__init__(vault_path, check_interval)
        self.drop_folder = self.vault_path / 'Drop'
        self.drop_folder.mkdir(parents=True, exist_ok=True)
        
        # Track processed files by hash to avoid duplicates
        self.state_file = self.vault_path / 'Logs' / 'filesystem_watcher_state.txt'
        self.processed_files = self._load_state()
    
    def _load_state(self) -> set:
        """Load the set of processed file hashes."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return set(line.strip() for line in f)
        return set()
    
    def _save_state(self):
        """Save the current state of processed files."""
        with open(self.state_file, 'w') as f:
            f.write('\n'.join(self.processed_files))
    
    def _get_file_hash(self, filepath: Path) -> str:
        """Calculate MD5 hash of a file."""
        hash_md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def check_for_updates(self) -> list:
        """
        Check the Drop folder for new files.
        
        Returns:
            List of tuples: (filepath, file_hash)
        """
        new_files = []
        
        if not self.drop_folder.exists():
            return new_files
        
        for filepath in self.drop_folder.iterdir():
            if filepath.is_file() and not filepath.name.startswith('.'):
                file_hash = self._get_file_hash(filepath)
                
                if file_hash not in self.processed_files:
                    new_files.append((filepath, file_hash))
                    self.processed_files.add(file_hash)
        
        self._save_state()
        return new_files
    
    def create_action_file(self, item) -> Path:
        """
        Create a .md action file for the dropped file.
        
        Args:
            item: Tuple of (filepath, file_hash)
            
        Returns:
            Path to the created action file
        """
        filepath, file_hash = item
        file_size = filepath.stat().st_size
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create action file path
        action_filename = f'FILE_{timestamp}_{filepath.name}.md'
        action_path = self.needs_action / action_filename
        
        # Create the action file content
        content = f'''---
type: file_drop
original_name: {filepath.name}
size: {file_size}
size_human: {self._human_readable_size(file_size)}
dropped_at: {datetime.now().isoformat()}
file_hash: {file_hash}
status: pending
---

# File Dropped for Processing

## File Details

- **Original Name**: {filepath.name}
- **Size**: {self._human_readable_size(file_size)}
- **Dropped At**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Suggested Actions

- [ ] Review file contents
- [ ] Categorize the file
- [ ] Take necessary action
- [ ] Move to appropriate folder
- [ ] Archive or delete after processing

## Notes

*Add your notes here*

---
*Created by FileSystemWatcher (Qwen Code AI Employee)*
'''
        
        action_path.write_text(content, encoding='utf-8')
        self.logger.info(f'Processed file: {filepath.name} ({self._human_readable_size(file_size)})')
        
        return action_path
    
    def _human_readable_size(self, size: int) -> str:
        """Convert bytes to human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f'{size:.2f} {unit}'
            size /= 1024
        return f'{size:.2f} TB'


def main():
    """Main entry point for the file system watcher."""
    parser = argparse.ArgumentParser(
        description='File System Watcher for AI Employee'
    )
    parser.add_argument(
        'vault_path',
        type=str,
        help='Path to the Obsidian vault root'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=30,
        help='Check interval in seconds (default: 30)'
    )
    
    args = parser.parse_args()
    
    # Resolve to absolute path
    vault_path = Path(args.vault_path).resolve()
    
    if not vault_path.exists():
        print(f'Error: Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    print('[INFO] Starting FileSystemWatcher')
    print(f'[INFO] Vault: {vault_path}')
    print(f'[INFO] Drop folder: {vault_path / "Drop"}')
    print(f'[INFO] Check interval: {args.interval}s')
    print(f'\n[TIP] Drop files into the "Drop" folder to create action items')
    print(f'Press Ctrl+C to stop\n')
    
    watcher = FileSystemWatcher(str(vault_path), args.interval)
    watcher.run()


if __name__ == '__main__':
    main()
