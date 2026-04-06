"""
Base Watcher Class for AI Employee

All watcher scripts should inherit from this base class.
Watchers monitor external sources and create action files in the Needs_Action folder.
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime


class BaseWatcher(ABC):
    """
    Abstract base class for all AI Employee watchers.
    
    Watchers are long-running processes that monitor external sources
    (Gmail, WhatsApp, file systems, etc.) and create actionable .md files
    when new items are detected.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        
        # Setup logging
        self.log_dir = self.vault_path / 'Logs'
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = self.log_dir / f'watcher_{datetime.now().strftime("%Y-%m-%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Ensure required directories exist
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Create required directories if they don't exist."""
        dirs = ['Inbox', 'Needs_Action', 'Done', 'Pending_Approval', 'Approved', 'Logs']
        for dir_name in dirs:
            (self.vault_path / dir_name).mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check the external source for new items.
        
        Returns:
            List of new items to process
        """
        pass
    
    @abstractmethod
    def create_action_file(self, item) -> Path:
        """
        Create a .md action file in the Needs_Action folder.
        
        Args:
            item: The item to create an action file for
            
        Returns:
            Path to the created file
        """
        pass
    
    def run(self):
        """
        Main run loop. Continuously checks for updates and creates action files.
        This method runs indefinitely until interrupted (Ctrl+C).
        """
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')
        
        try:
            while True:
                try:
                    items = self.check_for_updates()
                    for item in items:
                        filepath = self.create_action_file(item)
                        self.logger.info(f'Created action file: {filepath.name}')
                except Exception as e:
                    self.logger.error(f'Error checking for updates: {e}', exc_info=True)
                
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}', exc_info=True)
            raise
