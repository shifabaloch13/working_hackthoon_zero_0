"""
Twitter/X MCP Server - Gold Tier Implementation

Posts tweets to Twitter/X via API v2.
Includes approval workflow for sensitive actions.

Prerequisites:
    - Twitter Developer Account
    - Twitter API v2 credentials (Bearer Token, API Key, API Secret)
    - tweepy library: pip install tweepy

Usage:
    python twitter_poster.py "D:/path/to/vault" --tweet "Your tweet text"
    python twitter_poster.py "D:/path/to/vault" --post-approved
"""

import sys
import json
import pickle
from pathlib import Path
from datetime import datetime

# Try to import tweepy (optional - for actual posting)
try:
    import tweepy
    TWEEPY_AVAILABLE = True
except ImportError:
    TWEEPY_AVAILABLE = False
    print('[WARN] tweepy not installed. Twitter posting will be simulated.')


class TwitterMCP:
    """Twitter/X MCP Server for AI Employee."""
    
    def __init__(self, vault_path: str, config_path: str = None):
        self.vault = Path(vault_path).resolve()
        self.config_path = Path(config_path) if config_path else self.vault.parent / 'twitter_config.json'
        self.pending_approval = self.vault / 'Pending_Approval'
        self.approved = self.vault / 'Approved'
        self.done = self.vault / 'Done'
        self.logs_folder = self.vault / 'Logs'
        
        for folder in [self.pending_approval, self.approved, self.done, self.logs_folder]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Load config
        self.config = self._load_config()
        self.client = self._create_client()
    
    def _load_config(self) -> dict:
        """Load Twitter API config."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Return dummy config for simulation
        return {
            'bearer_token': 'dummy_token',
            'api_key': 'dummy_key',
            'api_secret': 'dummy_secret',
            'access_token': 'dummy_token',
            'access_token_secret': 'dummy_secret'
        }
    
    def _create_client(self):
        """Create Twitter API client."""
        if not TWEEPY_AVAILABLE:
            return None
        
        if not self.config_path.exists():
            print('[INFO] Twitter config not found. Running in simulation mode.')
            return None
        
        try:
            client = tweepy.Client(
                bearer_token=self.config.get('bearer_token'),
                consumer_key=self.config.get('api_key'),
                consumer_secret=self.config.get('api_secret'),
                access_token=self.config.get('access_token'),
                access_token_secret=self.config.get('access_token_secret')
            )
            print('[OK] Twitter API client created')
            return client
        except Exception as e:
            print(f'[WARN] Could not create Twitter client: {e}')
            print('[INFO] Running in simulation mode')
            return None
    
    def create_tweet_draft(self, text: str, media_path: str = None) -> Path:
        """Create a tweet draft for approval."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'TWEET_{timestamp}.md'
        draft_file = self.pending_approval / filename
        
        content = f"""---
type: tweet_request
text: {text[:100]}{'...' if len(text) > 100 else ''}
created: {datetime.now().isoformat()}
character_count: {len(text)}
status: pending
---

# Tweet Draft

## Content
{text}

## Details
- **Character Count**: {len(text)}/280
- **Media**: {media_path if media_path else 'None'}

## To Approve
Move this file to `/Approved` folder to post to Twitter.

## To Reject
Move this file to `/Rejected` folder with reason.

---
*Created by AI Employee Twitter MCP*
"""
        draft_file.write_text(content, encoding='utf-8')
        print(f'[OK] Tweet draft created: {draft_file.name}')
        return draft_file
    
    def post_tweet(self, text: str, media_path: str = None) -> dict:
        """Post tweet to Twitter."""
        
        print(f'[INFO] Posting tweet: {text[:50]}...')
        
        # Check character limit
        if len(text) > 280:
            print(f'[ERROR] Tweet too long: {len(text)}/280 characters')
            return {'success': False, 'error': 'Tweet too long'}
        
        # Simulation mode (no Twitter API)
        if not self.client:
            print('[INFO] Simulation mode - tweet not actually posted')
            print('[INFO] To enable real posting, add twitter_config.json with API credentials')
            
            # Simulate successful post
            return {
                'success': True,
                'simulated': True,
                'text': text,
                'timestamp': datetime.now().isoformat()
            }
        
        # Real Twitter API posting
        try:
            response = self.client.create_tweet(text=text)
            tweet_id = response.data['id']
            
            print(f'[OK] Tweet posted! ID: {tweet_id}')
            
            return {
                'success': True,
                'simulated': False,
                'tweet_id': tweet_id,
                'text': text,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f'[ERROR] Failed to post tweet: {e}')
            return {'success': False, 'error': str(e)}
    
    def process_approved_tweets(self) -> int:
        """Process all approved tweets."""
        approved_files = [f for f in self.approved.iterdir() 
                         if f.suffix == '.md' and 'TWEET' in f.name]
        
        if not approved_files:
            print('[INFO] No approved tweets to process')
            return 0
        
        print(f'[INFO] Found {len(approved_files)} approved tweet(s)')
        
        posted = 0
        for tweet_file in approved_files:
            print()
            print(f'Processing: {tweet_file.name}')
            
            # Parse tweet content
            content = tweet_file.read_text(encoding='utf-8')
            tweet_text = self._extract_tweet_text(content)
            
            if tweet_text:
                result = self.post_tweet(tweet_text)
                
                if result.get('success'):
                    # Move to Done
                    tweet_file.rename(self.done / tweet_file.name)
                    print(f'[OK] Moved to Done: {tweet_file.name}')
                    
                    # Log the action
                    self._log_action(tweet_file, result)
                    posted += 1
                else:
                    print(f'[ERROR] Failed to post: {tweet_file.name}')
        
        return posted
    
    def _extract_tweet_text(self, content: str) -> str:
        """Extract tweet text from approval file."""
        lines = content.split('\n')
        in_content = False
        text_lines = []
        
        for line in lines:
            if line.strip() == '## Content':
                in_content = True
                continue
            if in_content:
                if line.startswith('##'):
                    break
                text_lines.append(line)
        
        return '\n'.join(text_lines).strip()
    
    def _log_action(self, filepath: Path, result: dict):
        """Log tweet action."""
        log_file = self.logs_folder / f'twitter_{datetime.now().strftime("%Y-%m-%d")}.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': 'tweet_posted',
            'file': filepath.name,
            'result': result
        }
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')


def main():
    if len(sys.argv) < 2:
        print('Usage: python twitter_poster.py <vault_path> [OPTIONS]')
        print()
        print('Options:')
        print('  --tweet "text"     Create tweet draft')
        print('  --post-approved    Post all approved tweets')
        print()
        print('Examples:')
        print('  python twitter_poster.py "../AI_Employee_Vault" --tweet "Hello Twitter!"')
        print('  python twitter_poster.py "../AI_Employee_Vault" --post-approved')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    twitter = TwitterMCP(vault_path)
    
    if '--tweet' in sys.argv:
        # Create tweet draft
        idx = sys.argv.index('--tweet') + 1
        if idx < len(sys.argv):
            tweet_text = sys.argv[idx]
            twitter.create_tweet_draft(tweet_text)
        else:
            print('[ERROR] No tweet text provided')
    
    elif '--post-approved' in sys.argv:
        # Post approved tweets
        posted = twitter.process_approved_tweets()
        print()
        print('=' * 70)
        print(f'  TWEETS POSTED: {posted}')
        print('=' * 70)
        print()


if __name__ == '__main__':
    main()
