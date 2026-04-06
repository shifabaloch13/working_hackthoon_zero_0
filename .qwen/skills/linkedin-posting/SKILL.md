---
name: linkedin-posting
description: |
  Automatically post business updates to LinkedIn for lead generation.
  Uses Playwright for browser automation. Requires human approval before posting.
  Use for content marketing, business updates, and sales generation.
---

# LinkedIn Posting Skill

Automate LinkedIn posts for business marketing and lead generation.

## Prerequisites

1. **Python 3.10+**
2. **Playwright**: `pip install playwright`
3. **Playwright browsers**: `playwright install`
4. **LinkedIn account** with business profile

## Installation

```bash
# Install Playwright
pip install playwright

# Install browser (Chromium)
playwright install chromium
```

## Usage

### Post to LinkedIn

```bash
cd AI_Employee_Vault/scripts
python linkedin_poster.py "D:/path/to/AI_Employee_Vault" --post "Your post content here"
```

### With Image

```bash
python linkedin_poster.py "../AI_Employee_Vault" \
  --post "Check out our new service!" \
  --image "D:/path/to/image.jpg"
```

### Command Line Options

```bash
python linkedin_poster.py <vault_path> [OPTIONS]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--post` | (required) | Post content text |
| `--image` | None | Path to image file |
| `--schedule` | None | Schedule for later (ISO datetime) |
| `--headless` | false | Run browser in headless mode |

## How It Works

1. **Create post content** (manually or via AI)
2. **Save to Pending_Approval/** for review
3. **Human approves** by moving to Approved/
4. **Poster script** logs into LinkedIn and posts
5. **Log result** in Done/ folder

## Post Creation Workflow

### Step 1: AI Creates Post Draft

```markdown
---
type: social_post
platform: linkedin
content: |
  Excited to announce our new AI Employee service!
  
  Automate your business workflows with intelligent agents.
  
  #AI #Automation #Business
  
created: 2026-02-26T10:30:00Z
status: pending_approval
---

# LinkedIn Post Draft

## Content
Excited to announce our new AI Employee service!

Automate your business workflows with intelligent agents.

#AI #Automation #Business

## To Approve
Move this file to `/Approved` folder to post.
```

### Step 2: Human Reviews

- Check content for accuracy
- Verify hashtags are relevant
- Ensure professional tone
- Move to `Approved/` or `Rejected/`

### Step 3: Execute Post

```bash
# Process approved posts
python linkedin_poster.py "../AI_Employee_Vault" --execute-approved
```

## Python Implementation

```python
# linkedin_poster.py
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

class LinkedInPoster:
    def __init__(self, vault_path: str, session_path: str = None):
        self.vault = Path(vault_path)
        self.session_path = Path(session_path) if session_path else self.vault / 'linkedin_session'
        self.approved = self.vault / 'Approved'
        self.done = self.vault / 'Done'
    
    def post(self, content: str, image_path: str = None, headless: bool = False):
        """Post content to LinkedIn."""
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                self.session_path,
                headless=headless,
                viewport={'width': 1280, 'height': 720}
            )
            
            page = browser.pages[0]
            
            # Navigate to LinkedIn
            page.goto('https://www.linkedin.com/feed/')
            page.wait_for_timeout(5000)  # Wait for load
            
            # Find and click the post input
            post_input = page.query_selector('[data-testid="update-editor-text-input"]')
            if post_input:
                post_input.click()
                post_input.fill(content)
                
                # Add image if provided
                if image_path:
                    media_button = page.query_selector('[data-testid="media-upload"]')
                    if media_button:
                        media_button.click()
                        page.set_input_files('input[type="file"]', image_path)
                
                # Click post button
                post_button = page.query_selector('[data-testid="share-post-btn"]')
                if post_button:
                    post_button.click()
                    page.wait_for_timeout(3000)
                    
                    print("[OK] Posted to LinkedIn successfully")
                    return True
            
            browser.close()
            return False
    
    def process_approved_posts(self, headless: bool = False):
        """Process all approved post files."""
        for approval_file in self.approved.iterdir():
            if approval_file.suffix == '.md' and 'social_post' in approval_file.read_text():
                content = self._parse_post_content(approval_file)
                
                if content:
                    success = self.post(content, headless=headless)
                    
                    if success:
                        approval_file.rename(self.done / approval_file.name)
                        print(f"[OK] Posted and moved to Done: {approval_file.name}")
                    else:
                        print(f"[ERROR] Failed to post: {approval_file.name}")
    
    def _parse_post_content(self, filepath: Path) -> str:
        """Extract post content from approval file."""
        content = filepath.read_text(encoding='utf-8')
        # Parse frontmatter to extract content
        # Simple extraction (improve with proper YAML parsing)
        lines = content.split('\n')
        in_content = False
        post_lines = []
        
        for line in lines:
            if line.strip() == '## Content':
                in_content = True
                continue
            if in_content and line.startswith('##'):
                break
            if in_content:
                post_lines.append(line)
        
        return '\n'.join(post_lines).strip()
```

## Content Guidelines

### Good Post Examples

```
🚀 Excited to announce our new AI Employee service!

Automate your business workflows with intelligent agents that work 24/7.

✅ Reduce costs by 85%
✅ 168 hours/week availability
✅ Instant scaling

Learn more: [your-link.com]

#AI #Automation #Business #Innovation
```

### Post Types

1. **Business Updates**: New services, milestones
2. **Thought Leadership**: Industry insights
3. **Case Studies**: Client success stories
4. **Educational**: Tips and how-tos
5. **Engagement**: Questions and polls

## Approval Workflow

```
AI generates post draft
        ↓
Saved to Pending_Approval/
        ↓
Human reviews content
        ↓
Move to Approved/ → AI posts automatically
        ↓
Logged in Done/
```

## Scheduling

For scheduled posts, use Task Scheduler:

```bash
# Windows Task Scheduler
schtasks /create /tn "LinkedIn Post" /tr "python linkedin_poster.py ../AI_Employee_Vault --execute-approved" /sc daily /st 09:00
```

## Security Notes

- **Never auto-post** without approval
- **Keep session secure** (contains LinkedIn auth)
- **Review all content** before posting
- **Monitor for errors** (LinkedIn may block automation)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Login failed | Session expired, re-login manually |
| Post button not found | LinkedIn UI changed, update selectors |
| Rate limited | Reduce posting frequency |
| Image upload fails | Check file path and format |

## Best Practices

1. **Review every post** before publishing
2. **Maintain brand voice** in Company_Handbook.md
3. **Track engagement** manually or via API
4. **Post consistently** (3-5 times per week)
5. **Use relevant hashtags** (3-5 per post)
