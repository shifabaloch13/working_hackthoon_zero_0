# Facebook Auto-Posting & Comment Detection Guide

**Complete guide to automated Facebook posting and comment monitoring for AI Employee**

---

## Table of Contents

1. [Auto-Posting Workflow](#1-auto-posting-workflow)
2. [Comment Detection](#2-comment-detection)
3. [Complete Implementation](#3-complete-implementation)
4. [Testing](#4-testing)
5. [Troubleshooting](#5-troubleshooting)

---

## 1. Auto-Posting Workflow

### Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: Trigger Event                                           │
│                                                                 │
│ Sources:                                                        │
│ - Gmail Watcher (client request)                               │
│ - WhatsApp Watcher (lead inquiry)                              │
│ - Scheduled (daily/weekly posts)                               │
│ - CEO Briefing (business updates)                              │
│ - Manual trigger                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: AI Creates Post Content                                 │
│                                                                 │
│ AI Employee analyzes:                                           │
│ - Business goals                                                │
│ - Recent achievements                                           │
│ - Industry trends                                               │
│ - Optimal posting time                                          │
│ - Hashtag strategy                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: Create Draft File                                       │
│                                                                 │
│ File: Pending_Approval/FB_POST_YYYYMMDD_HHMMSS.md              │
│                                                                 │
│ Contains:                                                       │
│ - Post content                                                  │
│ - Platform (Facebook/Instagram)                                 │
│ - Hashtags                                                      │
│ - Links/Images                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: Human Approval                                          │
│                                                                 │
│ User reviews draft and:                                         │
│ - Moves to Approved/ (approve)                                  │
│ - Moves to Rejected/ (reject)                                   │
│ - Edits content (modify)                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: Automated Posting                                       │
│                                                                 │
│ Command: python facebook_poster.py --post-approved             │
│                                                                 │
│ Process:                                                        │
│ 1. Read all files in Approved/                                  │
│ 2. Post to Facebook via Graph API                               │
│ 3. Post to Instagram (if applicable)                            │
│ 4. Log results                                                  │
│ 5. Move to Done/                                                │
└─────────────────────────────────────────────────────────────────┘
```

### Detailed Step-by-Step

#### Step 1: Trigger Event

**Example 1: Gmail Watcher Trigger**

```python
# gmail_watcher.py detects email
email = {
    'from': 'client@example.com',
    'subject': 'Can you send me the invoice?',
    'body': 'Hi, I need the invoice for January services.'
}

# Creates action file
# Needs_Action/EMAIL_invoice_request.md
```

**Example 2: Scheduled Post**

```bash
# Windows Task Scheduler - Daily at 9 AM
schtasks /create /tn "Facebook_Daily_Post" ^
  /tr "python orchestrator.py ../AI_Employee_Vault --daily-post" ^
  /sc daily /st 09:00
```

**Example 3: CEO Briefing Trigger**

```python
# ceo_briefing.py generates weekly update
briefing = {
    'revenue': 'up 45%',
    'milestone': '100 clients reached'
}

# Creates post draft automatically
```

#### Step 2: AI Creates Post Content

```python
# orchestrator.py triggers AI
prompt = """
Based on this business update, create a Facebook post:

Revenue: Up 45% this quarter
New clients: 25
Milestone: 100 clients reached

Requirements:
- Professional tone
- Include 3-5 hashtags
- Keep under 280 characters
- Add emoji for engagement
"""

# AI generates:
post_content = """
🎉 Exciting news! We've reached 100 clients this quarter! 

Thank you for trusting us with your business. Here's to continued growth together! 🚀

#milestone #business #growth #grateful #100clients
"""
```

#### Step 3: Create Draft File

```python
# facebook_poster.py
draft_file = facebook.create_post_draft(
    message=post_content,
    platform='facebook',
    link='https://yourcompany.com/blog/100-clients'
)

# Creates: Pending_Approval/FB_POST_20260308_093000.md
```

**Draft File Content:**

```markdown
---
type: facebook_post_request
message: 🎉 Exciting news! We've reached 100 clients...
platform: facebook
created: 2026-03-08T09:30:00
character_count: 156
status: pending
---

# Facebook Post Draft

## Content
🎉 Exciting news! We've reached 100 clients this quarter! 

Thank you for trusting us with your business. Here's to continued growth together! 🚀

#milestone #business #growth #grateful #100clients

## Details
- **Platform**: Facebook
- **Character Count**: 156
- **Link**: https://yourcompany.com/blog/100-clients

## To Approve
Move this file to `/Approved` folder to post.
```

#### Step 4: Human Approval

**User Actions:**

```bash
# Option 1: Approve
move Pending_Approval\FB_POST_20260308_093000.md Approved\

# Option 2: Reject (with reason)
move Pending_Approval\FB_POST_20260308_093000.md Rejected\
echo "Too promotional, reduce hashtags" >> Rejected\FB_POST_20260308_093000.md

# Option 3: Edit
notepad Pending_Approval\FB_POST_20260308_093000.md
# Modify content, then move to Approved/
```

#### Step 5: Automated Posting

```bash
# Post all approved content
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" --post-approved
```

**What happens internally:**

```python
# facebook_poster.py - process_approved_posts()

# 1. Find all approved posts
approved_files = [
    'Approved/FB_POST_20260308_093000.md',
    'Approved/IG_POST_20260308_094500.md'
]

# 2. Post each one
for post_file in approved_files:
    post_data = extract_post_data(post_file)
    
    if post_data['platform'] == 'facebook':
        result = post_to_facebook(
            message=post_data['message'],
            link=post_data.get('link')
        )
    elif post_data['platform'] == 'instagram':
        result = post_to_instagram(
            message=post_data['message'],
            photo_path=post_data.get('photo')
        )
    
    # 3. Log result
    log_action(post_file, result)
    
    # 4. Move to Done
    move_to_done(post_file)
```

**Graph API Call:**

```python
import facebook

# Initialize
graph = facebook.GraphAPI(
    access_token="YOUR_PAGE_ACCESS_TOKEN",
    version="18.0"
)

# Post to Facebook
result = graph.put_object(
    parent_object="PAGE_ID",
    connection_name="feed",
    message="🎉 Exciting news! We've reached 100 clients...",
    link="https://yourcompany.com/blog/100-clients"
)

# Returns: {'id': '1234567890_9876543210'}
```

---

## 2. Comment Detection

### Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ COMMENT MONITORING WORKFLOW                                     │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Facebook    │────▶│  Comment     │────▶│  AI          │
│  Graph API   │     │  Fetching    │     │  Analysis    │
└──────────────┘     └──────────────┘     └──────────────┘
                            │                    │
                            │                    ▼
                            │           ┌──────────────┐
                            │           │  Action      │
                            │           │  Creation    │
                            │           └──────────────┘
                            │                    │
                            ▼                    ▼
                     ┌──────────────────────────────┐
                     │   Needs_Action/              │
                     │   COMMENT_post123_*.md       │
                     └──────────────────────────────┘
```

### Implementation

#### Step 1: Create Comment Watcher

```python
# facebook_comment_watcher.py

import facebook
import requests
from pathlib import Path
from datetime import datetime, timedelta
import time

class FacebookCommentWatcher:
    def __init__(self, vault_path: str, config_path: str):
        self.vault = Path(vault_path)
        self.needs_action = self.vault / 'Needs_Action'
        self.config = self._load_config(config_path)
        self.graph = facebook.GraphAPI(
            access_token=self.config['page_access_token'],
            version='18.0'
        )
        self.processed_comments = set()
        
    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def get_recent_comments(self, hours: int = 1) -> list:
        """Fetch comments from last N hours"""
        
        since_time = datetime.now() - timedelta(hours=hours)
        since_timestamp = int(since_time.timestamp())
        
        # Get all posts from page
        posts = self.graph.get_connections(
            id=self.config['page_id'],
            connection_name='feed',
            fields='comments,message,created_time'
        )
        
        comments = []
        for post in posts['data']:
            if 'comments' in post:
                for comment in post['comments']['data']:
                    comment_time = datetime.fromisoformat(
                        comment['created_time'].replace('Z', '+00:00')
                    )
                    
                    # Only get recent comments
                    if comment_time.timestamp() > since_timestamp:
                        comment['post_id'] = post['id']
                        comments.append(comment)
        
        return comments
    
    def filter_unprocessed(self, comments: list) -> list:
        """Return only comments we haven't processed"""
        return [
            c for c in comments 
            if c['id'] not in self.processed_comments
        ]
    
    def classify_comment(self, comment: dict) -> dict:
        """Classify comment type and priority"""
        
        text = comment.get('message', '').lower()
        
        # Keywords for classification
        urgent_keywords = ['urgent', 'asap', 'emergency', 'immediately']
        inquiry_keywords = ['price', 'cost', 'how much', 'quote', 'invoice']
        complaint_keywords = ['problem', 'issue', 'wrong', 'broken', 'complaint']
        positive_keywords = ['great', 'awesome', 'love', 'thank', 'excellent']
        
        # Determine priority
        if any(kw in text for kw in urgent_keywords):
            priority = 'high'
        elif any(kw in text for kw in inquiry_keywords):
            priority = 'medium'
        elif any(kw in text for kw in complaint_keywords):
            priority = 'high'
        elif any(kw in text for kw in positive_keywords):
            priority = 'low'
        else:
            priority = 'normal'
        
        # Determine type
        if any(kw in text for kw in inquiry_keywords):
            comment_type = 'inquiry'
        elif any(kw in text for kw in complaint_keywords):
            comment_type = 'complaint'
        elif any(kw in text for kw in positive_keywords):
            comment_type = 'positive'
        else:
            comment_type = 'general'
        
        return {
            'priority': priority,
            'type': comment_type,
            'requires_response': priority in ['high', 'medium']
        }
    
    def create_action_file(self, comment: dict, classification: dict):
        """Create action file in Needs_Action folder"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"COMMENT_{comment['id']}_{timestamp}.md"
        filepath = self.needs_action / filename
        
        content = f"""---
type: facebook_comment
post_id: {comment['post_id']}
comment_id: {comment['id']}
from_name: {comment.get('from', {}).get('name', 'Unknown')}
from_id: {comment.get('from', {}).get('id', 'Unknown')}
message: {comment.get('message', 'No text')}
created_time: {comment.get('created_time')}
priority: {classification['priority']}
comment_type: {classification['type']}
requires_response: {classification['requires_response']}
status: pending
---

# Facebook Comment Alert

## Comment Details
- **From**: {comment.get('from', {}).get('name', 'Unknown')}
- **Time**: {comment.get('created_time')}
- **Priority**: {classification['priority'].upper()}
- **Type**: {classification['type']}

## Comment Text
> {comment.get('message', 'No text')}

## Suggested Actions
"""
        
        # Add suggested actions based on type
        if classification['type'] == 'inquiry':
            content += """
- [ ] Respond with pricing information
- [ ] Send DM for detailed discussion
- [ ] Create lead in CRM
"""
        elif classification['type'] == 'complaint':
            content += """
- [ ] Respond immediately (high priority)
- [ ] Escalate to support team
- [ ] Offer resolution
"""
        elif classification['type'] == 'positive':
            content += """
- [ ] Thank the user
- [ ] Share with team
- [ ] Consider as testimonial
"""
        else:
            content += """
- [ ] Review and respond if needed
"""
        
        content += f"""
## Quick Reply
[Respond via Facebook](https://facebook.com/{comment['post_id']})

---
*Detected by AI Employee Facebook Comment Watcher*
"""
        
        filepath.write_text(content, encoding='utf-8')
        self.processed_comments.add(comment['id'])
        
        return filepath
    
    def run(self, check_interval: int = 300):
        """Run continuous monitoring"""
        
        print(f"[INFO] Starting Facebook Comment Watcher")
        print(f"[INFO] Checking every {check_interval} seconds")
        
        while True:
            try:
                # Get recent comments
                comments = self.get_recent_comments(hours=1)
                
                # Filter unprocessed
                new_comments = self.filter_unprocessed(comments)
                
                # Process each comment
                for comment in new_comments:
                    # Classify
                    classification = self.classify_comment(comment)
                    
                    # Create action file
                    filepath = self.create_action_file(comment, classification)
                    
                    print(f"[OK] Created action file: {filepath.name}")
                    print(f"     Priority: {classification['priority']}")
                    print(f"     Type: {classification['type']}")
                
                if not new_comments:
                    print(f"[INFO] No new comments")
                
            except Exception as e:
                print(f"[ERROR] Error checking comments: {e}")
            
            # Wait before next check
            time.sleep(check_interval)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python facebook_comment_watcher.py <vault_path> <config_path>")
        sys.exit(1)
    
    vault_path = sys.argv[1]
    config_path = sys.argv[2] if len(sys.argv) > 2 else "facebook_config.json"
    
    watcher = FacebookCommentWatcher(vault_path, config_path)
    watcher.run()
```

#### Step 2: Run Comment Watcher

```bash
# Start comment monitoring
python facebook_comment_watcher.py "../AI_Employee_Vault" "facebook_config.json"

# Or run as background service (Windows)
nssm install FacebookCommentWatcher "python" "facebook_comment_watcher.py" "../AI_Employee_Vault"
nssm start FacebookCommentWatcher
```

#### Step 3: AI Processes Comment

When a comment action file is created, the AI Employee:

1. **Reads the file** from `Needs_Action/`
2. **Analyzes the comment** using AI
3. **Suggests response** based on classification
4. **Creates approval request** for response

**Example AI Response Generation:**

```python
# AI analyzes comment and generates response

comment = """
From: John Smith
Type: inquiry
Priority: medium
Message: "How much does your service cost? I need a quote for 50 users."
"""

# AI generates:
response_draft = """
Hi John! Thanks for your interest. 

Our pricing starts at $10/user/month for the basic plan. 
For 50 users, we offer volume discounts. 

I'll send you a detailed quote via DM. 

Best regards,
AI Employee Team
"""
```

#### Step 4: Human Reviews Response

```markdown
---
type: facebook_reply_request
comment_id: 1234567890
original_message: "How much does your service cost?"
suggested_reply: "Hi John! Thanks for your interest..."
status: pending
---

# Facebook Reply Approval

## Original Comment
> How much does your service cost? I need a quote for 50 users.

## Suggested Reply
Hi John! Thanks for your interest. 

Our pricing starts at $10/user/month...

## To Approve
Move to Approved/ to send reply
```

#### Step 5: Send Reply

```bash
# Send approved replies
python facebook_poster.py "../AI_Employee_Vault" --send-approved-replies
```

---

## 3. Complete Implementation

### File Structure

```
AI_Employee_Vault/
├── scripts/
│   ├── facebook_poster.py           # Main MCP server
│   ├── facebook_comment_watcher.py  # Comment monitoring
│   └── facebook_auto_post.py        # Scheduled posting
├── Pending_Approval/
│   ├── FB_POST_*.md                 # Post drafts
│   └── FB_REPLY_*.md                # Reply drafts
├── Approved/
├── Done/
└── Logs/
    └── facebook_YYYY-MM-DD.json     # Activity logs
```

### Scheduled Auto-Posting

```python
# facebook_auto_post.py

from pathlib import Path
from datetime import datetime
import json

class FacebookAutoPoster:
    def __init__(self, vault_path: str, config_path: str):
        self.vault = Path(vault_path)
        self.config_path = Path(config_path)
        self.facebook_mcp = FacebookMCP(vault_path, config_path)
    
    def generate_daily_post(self) -> str:
        """Generate daily post based on business context"""
        
        # Read business goals
        goals_file = self.vault / 'Business_Goals.md'
        if goals_file.exists():
            goals = goals_file.read_text()
        
        # Read recent achievements from Done folder
        done_folder = self.vault / 'Done'
        recent_tasks = list(done_folder.glob('*.md'))[-10:]
        
        # Generate post using AI
        prompt = f"""
Based on these business goals and recent achievements, create an engaging Facebook post:

Goals:
{goals}

Recent Achievements:
{[f.name for f in recent_tasks]}

Requirements:
- Professional but friendly tone
- 1-2 emojis
- 3-5 relevant hashtags
- Under 280 characters
"""
        
        # Call AI to generate content
        post_content = call_ai(prompt)
        
        return post_content
    
    def schedule_posts(self, posts: list):
        """Schedule posts for the week"""
        
        for post in posts:
            self.facebook_mcp.create_post_draft(
                message=post['content'],
                platform='facebook',
                link=post.get('link')
            )
            
            print(f"[OK] Created draft: {post['content'][:50]}...")


if __name__ == '__main__':
    auto_poster = FacebookAutoPoster("../AI_Employee_Vault", "facebook_config.json")
    
    # Generate and create drafts for the week
    posts = auto_poster.generate_daily_post()
    auto_poster.schedule_posts([posts])
```

### Windows Task Scheduler Setup

```bash
# Daily post at 9 AM
schtasks /create /tn "Facebook_Daily_Post" ^
  /tr "python AI_Employee_Vault/scripts/facebook_auto_post.py" ^
  /sc daily /st 09:00

# Comment check every 5 minutes
schtasks /create /tn "Facebook_Comment_Check" ^
  /tr "python AI_Employee_Vault/scripts/facebook_comment_watcher.py" ^
  /sc minute /mo 5

# Post approved content at 9 AM, 12 PM, 5 PM
schtasks /create /tn "Facebook_Post_Approved" ^
  /tr "python AI_Employee_Vault/scripts/facebook_poster.py ..\AI_Employee_Vault --post-approved" ^
  /sc daily /st 09:00,12:00,17:00
```

---

## 4. Testing

### Test Auto-Posting

```bash
# 1. Create test post draft
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" ^
  --post "Test post from AI Employee #automation"

# 2. Review draft
notepad Pending_Approval\FB_POST_*.md

# 3. Approve
move Pending_Approval\FB_POST_*.md Approved\

# 4. Post
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" --post-approved
```

### Test Comment Detection

```bash
# 1. Start comment watcher
python AI_Employee_Vault/scripts/facebook_comment_watcher.py ^
  "../AI_Employee_Vault" "facebook_config.json"

# 2. Add a test comment to your Facebook post

# 3. Watcher should detect and create action file
# Needs_Action/COMMENT_*.md
```

---

## 5. Troubleshooting

### Issue: Posts Not Appearing on Facebook

**Check:**
1. Access token is valid
2. Token has `pages_manage_posts` permission
3. Page ID is correct

```bash
# Test token
curl -X GET "https://graph.facebook.com/v18.0/me/accounts?access_token=YOUR_TOKEN"
```

### Issue: Comments Not Detected

**Check:**
1. Token has `pages_read_user_content` permission
2. Comment watcher is running
3. Check logs for errors

```python
# Debug: manually fetch comments
import facebook

graph = facebook.GraphAPI(access_token="YOUR_TOKEN")
comments = graph.get_connections(id="PAGE_ID", connection_name="comments")
print(comments)
```

### Issue: Permission Errors

```
facebook.GraphAPIError: Missing permissions
```

**Solution:**
1. Go to App Dashboard → App Review
2. Submit for permission review
3. Use test users during development

---

## Quick Reference

### Commands

```bash
# Create post draft
python facebook_poster.py "../AI_Employee_Vault" --post "Your message"

# Post approved content
python facebook_poster.py "../AI_Employee_Vault" --post-approved

# Start comment monitoring
python facebook_comment_watcher.py "../AI_Employee_Vault" "facebook_config.json"

# Generate daily post
python facebook_auto_post.py "../AI_Employee_Vault"
```

### Permissions Required

| Permission | Purpose |
|------------|---------|
| `pages_manage_posts` | Create posts |
| `pages_read_engagement` | Read comments |
| `pages_read_user_content` | Read user comments |
| `instagram_basic` | Instagram posting |
| `instagram_content_publish` | Publish Instagram |

### API Rate Limits

| Action | Limit |
|--------|-------|
| Posts per day | 25 per Page |
| API calls per hour | 200 per user |
| Comments per post | 1000 |

---

**Next Step:** Test the workflow with a real Facebook post! 🚀
