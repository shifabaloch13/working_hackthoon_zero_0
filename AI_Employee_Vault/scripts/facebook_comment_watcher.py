"""
Facebook Comment Watcher - Gold Tier Implementation

Monitors Facebook posts for new comments and creates action files.
Includes classification, priority detection, and AI response suggestions.

Prerequisites:
    - Facebook Page Access Token with pages_read_user_content permission
    - facebook-sdk library: pip install facebook-sdk
    - python-dotenv for environment variables: pip install python-dotenv
    - AI Employee vault setup

Usage:
    python facebook_comment_watcher.py "../AI_Employee_Vault"
    python facebook_comment_watcher.py "../AI_Employee_Vault" --check-interval 300
"""

import sys
import json
import os
import facebook
from pathlib import Path
from datetime import datetime, timedelta
import time
from typing import Dict, List, Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print('[WARN] python-dotenv not installed. Install with: pip install python-dotenv')


class FacebookCommentWatcher:
    """Monitor Facebook comments and create action files for AI Employee."""

    def __init__(self, vault_path: str, config_path: str = None):
        self.vault = Path(vault_path).resolve()
        self.needs_action = self.vault / 'Needs_Action'
        self.logs_folder = self.vault / 'Logs'
        
        # Ensure folders exist
        for folder in [self.needs_action, self.logs_folder]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Load config from environment variables
        self.config = self._load_config()
        self.graph = self._create_graph_api()
        
        # Track processed comments (in-memory for now)
        self.processed_comments = set()
        
        # Classification keywords
        self.keywords = {
            'urgent': ['urgent', 'asap', 'emergency', 'immediately', 'right now'],
            'inquiry': ['price', 'cost', 'how much', 'quote', 'invoice', 'pricing', 'buy', 'purchase'],
            'complaint': ['problem', 'issue', 'wrong', 'broken', 'complaint', 'not working', 'disappointed'],
            'positive': ['great', 'awesome', 'love', 'thank', 'excellent', 'amazing', 'wonderful', 'fantastic'],
            'negative': ['bad', 'terrible', 'worst', 'hate', 'awful', 'poor']
        }

    def _load_config(self) -> dict:
        """Load Facebook API config from environment variables."""
        config = {
            'facebook': {
                'app_id': os.getenv('FACEBOOK_APP_ID'),
                'app_secret': os.getenv('FACEBOOK_APP_SECRET'),
                'page_access_token': os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN'),
                'page_id': os.getenv('FACEBOOK_PAGE_ID'),
                'graph_api_version': os.getenv('FACEBOOK_GRAPH_API_VERSION', '18.0')
            },
            'instagram': {
                'business_account_id': os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID'),
                'enabled': True
            }
        }
        
        # Check if we have credentials
        has_credentials = all([
            config['facebook']['page_access_token'],
            config['facebook']['page_id']
        ])
        
        if not has_credentials:
            print('[INFO] No Facebook credentials found in .env file')
            print('[INFO] Add FACEBOOK_PAGE_ACCESS_TOKEN and FACEBOOK_PAGE_ID to .env')
        
        return config

    def _create_graph_api(self) -> Optional[facebook.GraphAPI]:
        """Create Facebook Graph API client."""
        try:
            access_token = self.config.get('facebook', {}).get('page_access_token')
            
            if not access_token:
                print('[INFO] No page_access_token in config - running in simulation mode')
                print('[INFO] Add FACEBOOK_PAGE_ACCESS_TOKEN to .env file')
                return None
            
            # Get API version (ensure format is #.#)
            version = self.config.get('facebook', {}).get('graph_api_version', '18.0')
            
            # Ensure version is a string
            version = str(version)
            
            if version.startswith('v'):
                version = version[1:]
            
            # Ensure version has decimal point (e.g., "18" -> "18.0")
            if '.' not in version:
                version = f"{version}.0"
            
            try:
                graph = facebook.GraphAPI(access_token=access_token, version=version)
                print(f'[OK] Facebook Graph API client created (v{version})')
                return graph
            except Exception as ve:
                if 'Version number' in str(ve):
                    # Try without specifying version
                    graph = facebook.GraphAPI(access_token=access_token)
                    print(f'[OK] Facebook Graph API client created (default version)')
                    return graph
                else:
                    raise
            
        except Exception as e:
            print(f'[WARN] Could not create Graph API client: {e}')
            print('[INFO] Running in simulation mode')
            return None

    def get_recent_comments(self, hours: int = 1) -> List[dict]:
        """Fetch comments from last N hours."""
        
        if not self.graph:
            print('[ERROR] Graph API not initialized')
            return []
        
        try:
            page_id = self.config.get('facebook', {}).get('page_id')
            
            if not page_id:
                print('[ERROR] No page_id in config')
                return []
            
            # Get recent posts with comments
            posts = self.graph.get_connections(
                id=page_id,
                connection_name='feed',
                fields='comments,message,created_time,permalink_url',
                limit=10  # Last 10 posts
            )
            
            all_comments = []
            
            if 'data' not in posts:
                return []
            
            for post in posts['data']:
                post_id = post.get('id')
                post_message = post.get('message', '')[:100]
                permalink = post.get('permalink_url', '')
                
                if 'comments' in post:
                    comments_data = post['comments']
                    
                    for comment in comments_data.get('data', []):
                        # Parse comment time
                        created_time = comment.get('created_time', '')
                        try:
                            comment_time = datetime.fromisoformat(
                                created_time.replace('Z', '+00:00')
                            )
                        except:
                            comment_time = datetime.now()
                        
                        # Only get recent comments
                        if datetime.now() - comment_time < timedelta(hours=hours):
                            comment['post_id'] = post_id
                            comment['post_message'] = post_message
                            comment['permalink'] = permalink
                            all_comments.append(comment)
            
            print(f'[INFO] Found {len(all_comments)} comments in last {hours} hour(s)')
            return all_comments
            
        except Exception as e:
            print(f'[ERROR] Failed to fetch comments: {e}')
            return []

    def filter_unprocessed(self, comments: List[dict]) -> List[dict]:
        """Return only comments we haven't processed."""
        return [c for c in comments if c['id'] not in self.processed_comments]

    def classify_comment(self, comment: dict) -> dict:
        """Classify comment type and priority."""
        
        text = comment.get('message', '').lower()
        
        # Count keyword matches
        scores = {
            'urgent': sum(1 for kw in self.keywords['urgent'] if kw in text),
            'inquiry': sum(1 for kw in self.keywords['inquiry'] if kw in text),
            'complaint': sum(1 for kw in self.keywords['complaint'] if kw in text),
            'positive': sum(1 for kw in self.keywords['positive'] if kw in text),
            'negative': sum(1 for kw in self.keywords['negative'] if kw in text)
        }
        
        # Determine primary type
        primary_type = max(scores, key=scores.get)
        
        # If no matches, it's general
        if scores[primary_type] == 0:
            primary_type = 'general'
        
        # Determine priority
        if scores['urgent'] > 0 or scores['complaint'] > 0:
            priority = 'high'
        elif scores['inquiry'] > 0:
            priority = 'medium'
        elif scores['positive'] > 0:
            priority = 'low'
        else:
            priority = 'normal'
        
        # Determine if response needed
        requires_response = priority in ['high', 'medium']
        
        return {
            'priority': priority,
            'type': primary_type,
            'requires_response': requires_response,
            'scores': scores
        }

    def create_action_file(self, comment: dict, classification: dict) -> Path:
        """Create action file in Needs_Action folder."""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"COMMENT_{comment['id']}_{timestamp}.md"
        filepath = self.needs_action / filename
        
        from_name = comment.get('from', {}).get('name', 'Unknown')
        comment_text = comment.get('message', 'No text')
        created_time = comment.get('created_time', 'Unknown')
        permalink = comment.get('permalink', '')
        
        content = f"""---
type: facebook_comment
post_id: {comment['post_id']}
comment_id: {comment['id']}
from_name: {from_name}
message: {comment_text.replace(chr(10), ' ')}
created_time: {created_time}
priority: {classification['priority']}
comment_type: {classification['type']}
requires_response: {str(classification['requires_response']).lower()}
status: pending
---

# Facebook Comment Alert

## Comment Details
- **From**: {from_name}
- **Time**: {created_time}
- **Priority**: {classification['priority'].upper()}
- **Type**: {classification['type']}
- **Permalink**: {permalink}

## Comment Text
> {comment_text}

## Context
**Original Post**: {comment.get('post_message', 'Unknown')[:100]}

## Suggested Actions
"""
        
        # Add suggested actions based on type
        if classification['type'] == 'inquiry':
            content += """
- [ ] Respond with pricing information
- [ ] Send DM for detailed discussion
- [ ] Create lead in CRM
- [ ] Follow up within 24 hours
"""
        elif classification['type'] == 'complaint':
            content += """
- [ ] Respond immediately (high priority)
- [ ] Apologize and acknowledge issue
- [ ] Escalate to support team
- [ ] Offer resolution or refund
- [ ] Follow up to ensure satisfaction
"""
        elif classification['type'] == 'positive':
            content += """
- [ ] Thank the user
- [ ] Share with team as win
- [ ] Consider as testimonial
- [ ] Ask for review/referral
"""
        elif classification['type'] == 'urgent':
            content += """
- [ ] RESPOND IMMEDIATELY
- [ ] Assess situation
- [ ] Escalate to management
- [ ] Document incident
"""
        else:
            content += """
- [ ] Review and respond if needed
- [ ] Monitor for follow-up
"""
        
        content += f"""
## AI Suggested Response

"""
        
        # Generate suggested response
        suggested_response = self._generate_suggested_response(comment, classification)
        content += f"> {suggested_response}\n\n"
        
        content += f"""
## Quick Links
- [View on Facebook]({permalink})
- [Reply via Facebook]({permalink})

---
*Detected by AI Employee Facebook Comment Watcher*
*Created: {datetime.now().isoformat()}*
"""
        
        filepath.write_text(content, encoding='utf-8')
        self.processed_comments.add(comment['id'])
        
        return filepath

    def _generate_suggested_response(self, comment: dict, classification: dict) -> str:
        """Generate AI-suggested response based on comment type."""
        
        from_name = comment.get('from', {}).get('name', 'there')
        comment_text = comment.get('message', '')
        
        if classification['type'] == 'inquiry':
            return f"Hi {from_name}! Thanks for your interest. I'd be happy to provide pricing information. I'll send you a DM with details. Looking forward to helping you!"
        
        elif classification['type'] == 'complaint':
            return f"Hi {from_name}, I'm sorry to hear about this issue. This isn't the experience we want for our customers. Please check your DMs - I'm reaching out to resolve this immediately."
        
        elif classification['type'] == 'positive':
            return f"Thank you so much, {from_name}! We're thrilled you're happy with our service. Your support means the world to us! 🙏"
        
        elif classification['type'] == 'urgent':
            return f"Hi {from_name}, we understand this is urgent. A team member is looking into this right now and will respond within 15 minutes."
        
        else:
            return f"Thanks for your comment, {from_name}! We appreciate you reaching out."

    def _log_comment(self, comment: dict, classification: dict, filepath: Path):
        """Log comment detection."""
        log_file = self.logs_folder / f'facebook_comments_{datetime.now().strftime("%Y-%m-%d")}.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'comment_id': comment['id'],
            'from': comment.get('from', {}).get('name', 'Unknown'),
            'type': classification['type'],
            'priority': classification['priority'],
            'action_file': filepath.name
        }
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f'[WARN] Failed to log comment: {e}')

    def run(self, check_interval: int = 300):
        """Run continuous monitoring."""
        
        print('=' * 70)
        print('  FACEBOOK COMMENT WATCHER')
        print('=' * 70)
        print()
        print(f'[INFO] Vault: {self.vault}')
        print(f'[INFO] Config: {self.config_path}')
        print(f'[INFO] Check interval: {check_interval} seconds')
        print()
        
        if not self.graph:
            print('[ERROR] Cannot start - Graph API not initialized')
            print('[INFO] Check facebook_config.json has valid credentials')
            return
        
        print(f'[INFO] Starting Facebook Comment Watcher...')
        print(f'[INFO] Monitoring for new comments')
        print()
        
        while True:
            try:
                # Get recent comments (last hour)
                comments = self.get_recent_comments(hours=1)
                
                # Filter unprocessed
                new_comments = self.filter_unprocessed(comments)
                
                if new_comments:
                    print(f'[INFO] Found {len(new_comments)} new comment(s)')
                    print()
                
                # Process each comment
                for comment in new_comments:
                    # Classify
                    classification = self.classify_comment(comment)
                    
                    # Create action file
                    filepath = self.create_action_file(comment, classification)
                    
                    # Log
                    self._log_comment(comment, classification, filepath)
                    
                    # Alert
                    print(f'[OK] Created: {filepath.name}')
                    print(f'     From: {comment.get("from", {}).get("name", "Unknown")}')
                    print(f'     Priority: {classification["priority"]}')
                    print(f'     Type: {classification["type"]}')
                    print()
                
                if not new_comments:
                    print(f'[INFO] No new comments')
                
            except Exception as e:
                print(f'[ERROR] Error in watcher loop: {e}')
            
            # Wait before next check
            print(f'[INFO] Next check in {check_interval} seconds...')
            print()
            time.sleep(check_interval)


def main():
    if len(sys.argv) < 2:
        print('Usage: python facebook_comment_watcher.py <vault_path> [config_path] [OPTIONS]')
        print()
        print('Arguments:')
        print('  vault_path       Path to AI Employee vault')
        print('  config_path      Path to facebook_config.json (default: ../facebook_config.json)')
        print()
        print('Options:')
        print('  --check-interval N  Check every N seconds (default: 300)')
        print('  --once              Run once and exit (for testing)')
        print()
        print('Examples:')
        print('  python facebook_comment_watcher.py "../AI_Employee_Vault"')
        print('  python facebook_comment_watcher.py "../AI_Employee_Vault" --check-interval 60')
        print('  python facebook_comment_watcher.py "../AI_Employee_Vault" --once')
        sys.exit(1)

    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)

    config_path = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
    
    # Parse options
    check_interval = 300
    run_once = False
    
    if '--check-interval' in sys.argv:
        idx = sys.argv.index('--check-interval') + 1
        if idx < len(sys.argv):
            check_interval = int(sys.argv[idx])
    
    if '--once' in sys.argv:
        run_once = True

    watcher = FacebookCommentWatcher(vault_path, config_path)
    
    if run_once:
        # Run once for testing
        print('[INFO] Running in --once mode')
        comments = watcher.get_recent_comments(hours=1)
        new_comments = watcher.filter_unprocessed(comments)
        
        print(f'[INFO] Found {len(comments)} total comments')
        print(f'[INFO] Found {len(new_comments)} new comments')
        
        for comment in new_comments:
            classification = watcher.classify_comment(comment)
            filepath = watcher.create_action_file(comment, classification)
            print(f'[OK] Created: {filepath.name}')
        
        print()
        print('[OK] Done (run without --once for continuous monitoring)')
    else:
        # Run continuous monitoring
        watcher.run(check_interval)


if __name__ == '__main__':
    main()
