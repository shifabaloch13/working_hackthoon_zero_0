"""
WhatsApp Watcher for AI Employee

Monitors WhatsApp Web for messages containing specific keywords.
Uses Playwright for browser automation.

Usage:
    python whatsapp_watcher.py /path/to/vault --keywords urgent,asap,invoice,payment

Dependencies:
    pip install playwright
    playwright install chromium
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

from base_watcher import BaseWatcher

# Playwright imports
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class WhatsAppWatcher(BaseWatcher):
    """
    Watches WhatsApp Web for messages containing keywords.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60, 
                 keywords=None, headless: bool = False):
        """
        Initialize the WhatsApp watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 60)
            keywords: List of keywords to detect (default: urgent, asap, invoice, payment, help)
            headless: Run browser in headless mode (default: False)
        """
        super().__init__(vault_path, check_interval)
        
        self.session_path = self.vault_path / 'whatsapp_session'
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        # Default keywords
        self.keywords = keywords or ['urgent', 'asap', 'invoice', 'payment', 'help', 'asap']
        
        self.headless = headless
        self.processed_chats = set()
        
        self.logger.info(f'WhatsApp Watcher initialized')
        self.logger.info(f'Keywords: {self.keywords}')
        self.logger.info(f'Session path: {self.session_path}')
    
    def check_for_updates(self) -> list:
        """
        Check WhatsApp Web for new messages with keywords.
        
        Returns:
            List of message dicts with chat info and text
        """
        messages = []
        
        try:
            with sync_playwright() as p:
                # Launch browser with persistent context
                browser = p.chromium.launch_persistent_context(
                    self.session_path,
                    headless=self.headless,
                    args=['--disable-blink-features=AutomationControlled'],
                    viewport={'width': 1280, 'height': 720}
                )
                
                page = browser.pages[0]
                
                # Navigate to WhatsApp Web
                self.logger.info('Navigating to WhatsApp Web...')
                page.goto('https://web.whatsapp.com', wait_until='domcontentloaded')
                
                # Wait for chat list (with timeout)
                try:
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                except PlaywrightTimeout:
                    self.logger.warning('WhatsApp Web did not load in time. May need QR scan.')
                    browser.close()
                    return messages
                
                # Give time for messages to load
                page.wait_for_timeout(5000)
                
                # Find all chat items
                chat_items = page.query_selector_all('[data-testid="chat-list"] > div')
                
                for chat in chat_items:
                    try:
                        # Get chat name
                        name_elem = chat.query_selector('[data-testid="chat-info"]')
                        chat_name = name_elem.inner_text() if name_elem else 'Unknown'
                        
                        # Check for unread indicator
                        is_unread = chat.get_attribute('aria-label', '').lower().find('unread') >= 0
                        
                        if is_unread:
                            # Get message text
                            msg_elem = chat.query_selector('[data-testid="message"]')
                            msg_text = msg_elem.inner_text() if msg_elem else ''
                            
                            # Check for keywords
                            msg_lower = msg_text.lower()
                            matched_keywords = [kw for kw in self.keywords if kw.lower() in msg_lower]
                            
                            if matched_keywords:
                                # Get timestamp if available
                                time_elem = chat.query_selector('[data-testid="chat-meta"]')
                                timestamp = time_elem.inner_text() if time_elem else datetime.now().isoformat()
                                
                                messages.append({
                                    'chat_name': chat_name,
                                    'message': msg_text,
                                    'keywords': matched_keywords,
                                    'timestamp': timestamp,
                                    'is_unread': True
                                })
                                
                                self.logger.info(f'Found matching message from {chat_name}: {matched_keywords}')
                        
                    except Exception as e:
                        self.logger.debug(f'Error processing chat: {e}')
                        continue
                
                browser.close()
                
        except Exception as e:
            self.logger.error(f'Error checking WhatsApp: {e}')
        
        return messages
    
    def create_action_file(self, message) -> Path:
        """
        Create a .md action file for the WhatsApp message.
        
        Args:
            message: Message dict with chat_name, message, keywords, timestamp
            
        Returns:
            Path to the created action file
        """
        chat_name = message['chat_name']
        msg_text = message['message']
        keywords = message['keywords']
        timestamp = message['timestamp']
        
        # Create filename
        safe_name = ''.join(c for c in chat_name[:20] if c.isalnum() or c in ' -_').strip()
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'WHATSAPP_{ts}_{safe_name}.md'
        filepath = self.needs_action / filename
        
        content = f'''---
type: whatsapp
from: {chat_name}
received: {timestamp}
keywords: {','.join(keywords)}
status: pending
---

# WhatsApp Message

## From
{chat_name}

## Received
{timestamp}

## Message
{msg_text}

## Keywords Detected
{chr(10).join('- ' + kw for kw in keywords)}

## Suggested Actions

- [ ] Reply to sender
- [ ] Take necessary action
- [ ] Mark as read in WhatsApp
- [ ] Archive after processing

## Notes

*Add your notes here*

---
*Created by WhatsAppWatcher (Qwen Code AI Employee)*

**Warning:** Be aware of WhatsApp's terms of service when using automation.
'''
        
        filepath.write_text(content, encoding='utf-8')
        self.logger.info(f'Created action file for WhatsApp message from {chat_name}')
        
        return filepath


def main():
    """Main entry point for the WhatsApp watcher."""
    parser = argparse.ArgumentParser(
        description='WhatsApp Watcher for AI Employee'
    )
    parser.add_argument(
        'vault_path',
        type=str,
        help='Path to the Obsidian vault root'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Check interval in seconds (default: 60)'
    )
    parser.add_argument(
        '--keywords',
        type=str,
        default='urgent,asap,invoice,payment,help',
        help='Comma-separated keywords to detect'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )
    
    args = parser.parse_args()
    
    # Resolve to absolute path
    vault_path = Path(args.vault_path).resolve()
    
    if not vault_path.exists():
        print(f'Error: Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    # Parse keywords
    keywords = [k.strip() for k in args.keywords.split(',')]
    
    print('[INFO] Starting WhatsAppWatcher')
    print(f'[INFO] Vault: {vault_path}')
    print(f'[INFO] Check interval: {args.interval}s')
    print(f'[INFO] Keywords: {", ".join(keywords)}')
    print(f'[INFO] Headless: {args.headless}')
    print(f'\n[TIP] First run will open browser for QR code scan')
    print(f'[TIP] Keep browser window visible to scan QR code')
    print(f'Press Ctrl+C to stop\n')
    
    try:
        watcher = WhatsAppWatcher(
            str(vault_path),
            check_interval=args.interval,
            keywords=keywords,
            headless=args.headless
        )
        watcher.run()
    except KeyboardInterrupt:
        print('\n[INFO] WhatsAppWatcher stopped by user')
    except Exception as e:
        print(f'[ERROR] Fatal error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
