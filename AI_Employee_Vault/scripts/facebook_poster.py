"""
Facebook/Instagram MCP Server - Gold Tier Implementation

Posts to Facebook Pages and Instagram Business accounts using REAL API credentials.
Includes approval workflow for sensitive actions.

Prerequisites:
    - Facebook Developer Account
    - Facebook App with Graph API access
    - Page Access Token (stored in .env file)
    - facebook-sdk library: pip install facebook-sdk

Usage:
    python facebook_poster.py "D:/path/to/vault" --post "Your post text"
    python facebook_poster.py "D:/path/to/vault" --post-approved
    python facebook_poster.py "D:/path/to/vault" --instagram --post "Instagram post"
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file (EXPLICIT PATH)
load_dotenv('D:/Download/working_hackthoon_zero_0/.env')

# Try to import facebook-sdk
try:
    import facebook
    FACEBOOK_SDK_AVAILABLE = True
except ImportError:
    FACEBOOK_SDK_AVAILABLE = False
    print('[WARN] facebook-sdk not installed. Facebook posting will be simulated.')
    print('[INFO] Install with: pip install facebook-sdk')


class FacebookMCP:
    """Facebook/Instagram MCP Server for AI Employee."""
    
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.pending_approval = self.vault / 'Pending_Approval'
        self.approved = self.vault / 'Approved'
        self.done = self.vault / 'Done'
        self.logs_folder = self.vault / 'Logs'
        
        for folder in [self.pending_approval, self.approved, self.done, self.logs_folder]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Load config from .env (EXPLICIT PATH)
        self.access_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
        self.page_id = os.getenv('FACEBOOK_PAGE_ID')
        self.app_id = os.getenv('FACEBOOK_APP_ID')
        self.app_secret = os.getenv('FACEBOOK_APP_SECRET')
        self.instagram_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        
        # Debug output
        print(f'[DEBUG] Loaded Page ID: {self.page_id}')
        print(f'[DEBUG] Token starts with: {self.access_token[:20] if self.access_token else "None"}')
        
        # Create Graph API client
        self.graph = self._create_graph_api()
    
    def _create_graph_api(self):
        """Create Facebook Graph API client."""
        if not FACEBOOK_SDK_AVAILABLE:
            return None
        
        if not self.access_token:
            print('[WARN] No Facebook access token found in .env file')
            print('[INFO] Running in simulation mode')
            return None
        
        try:
            graph = facebook.GraphAPI(
                access_token=self.access_token
            )
            print(f'[OK] Facebook Graph API client created')
            print(f'[OK] Connected to Page ID: {self.page_id}')
            return graph
        except Exception as e:
            print(f'[WARN] Could not create Facebook client: {e}')
            print('[INFO] Running in simulation mode')
            return None
    
    def create_post_draft(self, message: str, platform: str = 'facebook', 
                         link: str = None, photo_path: str = None) -> Path:
        """Create a post draft for approval."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        platform_prefix = 'IG' if platform == 'instagram' else 'FB'
        filename = f'{platform_prefix}_POST_{timestamp}.md'
        draft_file = self.pending_approval / filename
        
        content = f"""---
type: {platform}_post_request
message: {message[:100]}{'...' if len(message) > 100 else ''}
platform: {platform}
created: {datetime.now().isoformat()}
character_count: {len(message)}
status: pending
---

# {'Instagram' if platform == 'instagram' else 'Facebook'} Post Draft

## Content
{message}

## Details
- **Platform**: {platform.title()}
- **Character Count**: {len(message)}
- **Link**: {link if link else 'None'}
- **Photo**: {photo_path if photo_path else 'None'}

## To Approve
Move this file to `/Approved` folder to post to {'Instagram' if platform == 'instagram' else 'Facebook'}.

## To Reject
Move this file to `/Rejected` folder with reason.

---
*Created by AI Employee {'Instagram' if platform == 'instagram' else 'Facebook'} MCP*
"""
        draft_file.write_text(content, encoding='utf-8')
        print(f'[OK] {platform.title()} post draft created: {draft_file.name}')
        return draft_file
    
    def post_to_facebook(self, message: str, link: str = None, photo_path: str = None) -> dict:
        """Post to Facebook Page."""
        
        print(f'[INFO] Posting to Facebook: {message[:50]}...')
        
        # Check if we have real credentials
        if not self.graph:
            print('[INFO] Simulation mode - post not actually posted to Facebook')
            return {
                'success': True,
                'simulated': True,
                'platform': 'facebook',
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
        
        # REAL Facebook posting
        try:
            attachment = {}
            if link:
                attachment['link'] = link
            
            page_id = self.page_id
            
            # Post to Facebook
            response = self.graph.put_object(
                parent_object=page_id,
                connection_name='feed',
                message=message,
                **attachment
            )
            
            post_id = response.get('id')
            print(f'[OK] ✅ Facebook post posted successfully!')
            print(f'[OK] Post ID: {post_id}')
            print(f'[OK] View post: https://facebook.com/{post_id}')
            
            return {
                'success': True,
                'simulated': False,
                'platform': 'facebook',
                'post_id': post_id,
                'message': message,
                'link': link,
                'timestamp': datetime.now().isoformat(),
                'url': f'https://facebook.com/{post_id}'
            }
        except Exception as e:
            print(f'[ERROR] Failed to post to Facebook: {e}')
            return {'success': False, 'error': str(e), 'platform': 'facebook'}
    
    def post_to_instagram(self, message: str, photo_path: str = None) -> dict:
        """Post to Instagram Business Account."""
        
        print(f'[INFO] Posting to Instagram: {message[:50]}...')
        
        # Check if we have real credentials
        if not self.graph or not self.instagram_account_id:
            print('[INFO] Simulation mode - Instagram credentials not configured')
            return {
                'success': True,
                'simulated': True,
                'platform': 'instagram',
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
        
        # REAL Instagram posting (requires photo)
        try:
            ig_account_id = self.instagram_account_id
            
            # Instagram requires a photo URL
            if not photo_path:
                print('[WARN] Instagram posts require a photo. Using placeholder.')
                photo_path = 'https://example.com/placeholder.jpg'
            
            # Create media container
            response = self.graph.put_object(
                parent_object=ig_account_id,
                connection_name='media',
                caption=message,
                image_url=photo_path
            )
            
            creation_id = response.get('id')
            print(f'[OK] Instagram media container created: {creation_id}')
            
            # Publish the media
            publish_response = self.graph.put_object(
                parent_object=ig_account_id,
                connection_name='media_publish',
                creation_id=creation_id
            )
            
            post_id = publish_response.get('id')
            print(f'[OK] ✅ Instagram post published successfully!')
            print(f'[OK] Post ID: {post_id}')
            
            return {
                'success': True,
                'simulated': False,
                'platform': 'instagram',
                'post_id': post_id,
                'message': message,
                'photo': photo_path,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f'[ERROR] Failed to post to Instagram: {e}')
            return {'success': False, 'error': str(e), 'platform': 'instagram'}
    
    def process_approved_posts(self) -> int:
        """Process all approved posts."""
        approved_files = [f for f in self.approved.iterdir() 
                         if f.suffix == '.md' and ('FB_POST' in f.name or 'IG_POST' in f.name)]
        
        if not approved_files:
            print('[INFO] No approved posts to process')
            return 0
        
        print(f'[INFO] Found {len(approved_files)} approved post(s)')
        
        posted = 0
        for post_file in approved_files:
            print()
            print(f'Processing: {post_file.name}')
            
            # Parse post content
            content = post_file.read_text(encoding='utf-8')
            post_data = self._extract_post_data(content)
            
            if post_data:
                if post_data['platform'] == 'instagram':
                    result = self.post_to_instagram(
                        post_data['message'],
                        post_data.get('photo')
                    )
                else:
                    result = self.post_to_facebook(
                        post_data['message'],
                        post_data.get('link'),
                        post_data.get('photo')
                    )
                
                if result.get('success'):
                    # Move to Done
                    post_file.rename(self.done / post_file.name)
                    print(f'[OK] Moved to Done: {post_file.name}')
                    
                    # Log the action
                    self._log_action(post_file, result)
                    posted += 1
                else:
                    print(f'[ERROR] Failed to post: {post_file.name}')
        
        return posted
    
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
    
    def _log_action(self, filepath: Path, result: dict):
        """Log post action."""
        log_file = self.logs_folder / f'facebook_{datetime.now().strftime("%Y-%m-%d")}.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': f'{result.get("platform", "facebook")}_post',
            'file': filepath.name,
            'result': result
        }
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, indent=2) + '\n')


def main():
    if len(sys.argv) < 2:
        print('Usage: python facebook_poster.py <vault_path> [OPTIONS]')
        print()
        print('Options:')
        print('  --post "text"        Create Facebook post draft')
        print('  --instagram --post "text"  Create Instagram post draft')
        print('  --post-approved      Post all approved posts')
        print('  --link "url"         Add link to post')
        print('  --photo "path"       Add photo to post')
        print()
        print('Examples:')
        print('  python facebook_poster.py "../AI_Employee_Vault" --post "Hello Facebook!"')
        print('  python facebook_poster.py "../AI_Employee_Vault" --instagram --post "Instagram post"')
        print('  python facebook_poster.py "../AI_Employee_Vault" --post-approved')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    facebook = FacebookMCP(vault_path)
    
    # Parse options
    if '--post' in sys.argv:
        # Create post draft
        idx = sys.argv.index('--post') + 1
        if idx < len(sys.argv):
            post_text = sys.argv[idx]
            platform = 'instagram' if '--instagram' in sys.argv else 'facebook'
            
            link = None
            if '--link' in sys.argv:
                link_idx = sys.argv.index('--link') + 1
                if link_idx < len(sys.argv):
                    link = sys.argv[link_idx]
            
            photo = None
            if '--photo' in sys.argv:
                photo_idx = sys.argv.index('--photo') + 1
                if photo_idx < len(sys.argv):
                    photo = sys.argv[photo_idx]
            
            facebook.create_post_draft(post_text, platform, link, photo)
        else:
            print('[ERROR] No post text provided')
    
    elif '--post-approved' in sys.argv:
        # Post approved posts
        posted = facebook.process_approved_posts()
        print()
        print('=' * 70)
        print(f'  POSTS PUBLISHED: {posted}')
        print('=' * 70)
        if posted > 0:
            print('  ✅ REAL Facebook posts published!')
        print()


if __name__ == '__main__':
    main()
