---
name: facebook-instagram-mcp
description: |
  MCP server for Facebook and Instagram integration using official Graph API.
  Posts updates, monitors engagement, and generates summaries.
  Pure API integration - no browser automation.
---

# Facebook & Instagram MCP Server

**Official Facebook Graph API integration** for AI Employee social media automation.

## Overview

Integrates Facebook Pages and Instagram Business accounts using the **official Graph API** (via `facebook-sdk`):

- ✅ Automated posting (with approval workflow)
- ✅ Engagement monitoring
- ✅ Analytics and summaries
- ✅ Lead generation tracking
- ✅ **No Playwright** - Pure API integration

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  AI Employee    │────▶│  Facebook MCP    │────▶│  Facebook Graph │
│  (Obsidian)     │     │  (facebook-sdk)  │     │  API v18.0      │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │                          │
                              │                          ▼
                              │                   ┌─────────────────┐
                              └──────────────────▶│  Instagram API  │
                                                  └─────────────────┘
```

## Prerequisites

1. **Facebook Developer Account** - https://developers.facebook.com
2. **Facebook App** with Graph API access
3. **Facebook Page** (for posting)
4. **Instagram Business Account** (connected to Facebook Page)
5. **Python Libraries**:
   ```bash
   pip install facebook-sdk requests
   ```

## Installation

### Step 1: Install Dependencies

```bash
pip install facebook-sdk requests
```

### Step 2: Create Facebook App

See detailed guide: [FACEBOOK_GRAPH_API_SETUP.md](../FACEBOOK_GRAPH_API_SETUP.md)

Quick steps:
1. Go to https://developers.facebook.com
2. Create App → Select **Business**
3. Add **Facebook Login for Business** product
4. Request permissions: `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`

### Step 3: Get Access Tokens

**Get Page Access Token** (never expires):

```bash
# Using Graph API Explorer
https://developers.facebook.com/tools/explorer

# Select your app → Generate Token
# Select permissions → Generate
```

**Get Instagram Business Account ID**:

```bash
curl -X GET "https://graph.facebook.com/v18.0/YOUR_PAGE_ID?fields=instagram_business_account&access_token=YOUR_PAGE_TOKEN"
```

### Step 4: Create Configuration File

Create `facebook_config.json` in project root:

```json
{
  "facebook": {
    "app_id": "123456789012345",
    "app_secret": "your_app_secret_here",
    "page_access_token": "EAAG...your_long_lived_page_token",
    "page_id": "1234567890",
    "graph_api_version": "v18.0"
  },
  "instagram": {
    "business_account_id": "17841400000000000",
    "enabled": true
  }
}
```

**⚠️ Security:** Never commit this file! Add to `.gitignore`:
```
facebook_config.json
```

## Usage

### Create Facebook Post Draft

```bash
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" --post "Hello Facebook! #business #automation"
```

Creates approval file in `Pending_Approval/`:
```markdown
---
type: facebook_post_request
message: Hello Facebook! #business #automation
platform: facebook
created: 2026-03-07T10:30:00
character_count: 42
status: pending
---

# Facebook Post Draft

## Content
Hello Facebook! #business #automation

## To Approve
Move this file to `/Approved` folder to post.
```

### Create Instagram Post Draft

```bash
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" ^
  --instagram --post "New product launch! #innovation" --photo "path/to/image.jpg"
```

### Post with Link

```bash
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" ^
  --post "Check out our latest offer!" --link "https://example.com/offer"
```

### Post Approved Posts

```bash
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" --post-approved
```

### Generate Social Media Summary

```bash
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" --summary --period week
```

## Integration with AI Employee

### Approval Workflow

```
1. AI Creates Draft
   ↓
   Pending_Approval/FB_POST_*.md

2. Human Review
   ↓
   Review content, timing, hashtags

3. Human Approval
   ↓
   Move to Approved/

4. MCP Posts via Graph API
   ↓
   facebook-sdk → Graph API v18.0

5. Logging
   ↓
   Logs/facebook_YYYY-MM-DD.json
```

### Automated Posting Schedule

```bash
# Windows Task Scheduler - Post daily at 9 AM
schtasks /create /tn "Facebook_Daily_Post" ^
  /tr "python AI_Employee_Vault/scripts/facebook_poster.py \"../AI_Employee_Vault\" --post-approved" ^
  /sc daily /st 09:00
```

### CEO Briefing Integration

```markdown
## Social Media Performance (This Week)

### Facebook
- **Posts Published**: 5
- **Total Reach**: 12,500
- **Engagement Rate**: 3.2%
- **New Followers**: 45

### Instagram
- **Posts Published**: 3
- **Total Likes**: 890
- **Comments**: 67
- **New Followers**: 120

### Leads Generated
- **Facebook Leads**: 8
- **Instagram Leads**: 7
```

## API Reference

### FacebookMCP Class

```python
class FacebookMCP:
    """Facebook/Instagram MCP using official Graph API."""
    
    def __init__(self, vault_path: str, config_path: str = None)
    
    def create_post_draft(
        message: str, 
        platform: str = 'facebook',
        link: str = None, 
        photo_path: str = None
    ) -> Path
    
    def post_to_facebook(
        message: str, 
        link: str = None, 
        photo_path: str = None
    ) -> dict
    
    def post_to_instagram(
        message: str, 
        photo_path: str = None
    ) -> dict
    
    def process_approved_posts() -> int
    
    def get_page_insights(period: str = 'week') -> dict
    
    def get_instagram_insights(period: str = 'week') -> dict
```

### Graph API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/{page-id}/feed` | POST | Create Facebook post |
| `/{ig-account-id}/media` | POST | Create Instagram media container |
| `/{ig-account-id}/media_publish` | POST | Publish Instagram post |
| `/{page-id}?fields=insights` | GET | Get Page insights |
| `/{ig-account-id}?fields=insights` | GET | Get Instagram insights |

## Example: Graph API Call

### Post to Facebook

```python
import facebook

# Initialize Graph API
graph = facebook.GraphAPI(
    access_token="YOUR_PAGE_ACCESS_TOKEN",
    version="v18.0"
)

# Post to Page feed
result = graph.put_object(
    parent_object="YOUR_PAGE_ID",
    connection_name="feed",
    message="Hello from AI Employee! 🚀 #automation",
    link="https://example.com"
)

print(f"Post created! ID: {result['id']}")
```

### Post to Instagram

```python
import requests

access_token = "YOUR_PAGE_ACCESS_TOKEN"
ig_account_id = "YOUR_INSTAGRAM_ACCOUNT_ID"

# Step 1: Create media container
container_url = f"https://graph.facebook.com/v18.0/{ig_account_id}/media"
params = {
    "image_url": "https://example.com/image.jpg",
    "caption": "Hello Instagram! #automation",
    "access_token": access_token
}

response = requests.post(container_url, params=params)
container_id = response.json()["id"]

# Step 2: Publish
publish_url = f"https://graph.facebook.com/v18.0/{ig_account_id}/media_publish"
params = {
    "creation_id": container_id,
    "access_token": access_token
}

response = requests.post(publish_url, params=params)
media_id = response.json()["id"]

print(f"Instagram post published! ID: {media_id}")
```

## Best Practices

1. **Always Require Approval**: Never auto-post without human review
2. **Use Long-Lived Tokens**: Page tokens don't expire
3. **Optimal Timing**: Post when audience is most active
4. **Engagement Monitoring**: Respond to comments within 24 hours
5. **Content Mix**: Balance promotional, educational, engaging content
6. **Hashtag Strategy**: Use 3-5 relevant hashtags
7. **Image Quality**: 1080x1080 minimum for Instagram
8. **Rate Limiting**: Respect API limits (25 posts/day)

## Troubleshooting

### Error: Invalid OAuth Access Token

```
facebook.GraphAPIError: Invalid OAuth access token
```

**Solution:**
```bash
# Generate new long-lived token
https://developers.facebook.com/tools/explorer

# Update facebook_config.json
```

### Error: Missing Permissions

```
facebook.GraphAPIError: Missing permissions
```

**Solution:**
1. Go to App Dashboard → App Review
2. Submit permissions for review
3. Use test users during development

### Error: facebook-sdk Not Installed

```
[WARN] facebook-sdk not installed
```

**Solution:**
```bash
pip install facebook-sdk
```

### Error: Instagram Account Not Connected

```
[WARN] Instagram Business account not connected
```

**Solution:**
1. Go to Facebook Page Settings
2. Connect Instagram Business account
3. Ensure account type is Business

## Security

### Token Management

| Token Type | Expiration | Storage |
|------------|------------|---------|
| User Token (Short) | 1-2 hours | Testing only |
| User Token (Long) | 60 days | Development |
| **Page Token** | **Never** | **Production** |

### Best Practices

- ✅ Use Page Tokens (never expire)
- ✅ Store tokens in config file (not code)
- ✅ Add config to `.gitignore`
- ✅ Use environment variables in production
- ✅ Rotate tokens monthly
- ✅ Monitor token usage in App Dashboard

### Environment Variables (Production)

```bash
# .env file
FACEBOOK_APP_ID=123456789012345
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_PAGE_ACCESS_TOKEN=EAAG...
FACEBOOK_PAGE_ID=1234567890
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000000
```

```python
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "app_id": os.getenv("FACEBOOK_APP_ID"),
    "app_secret": os.getenv("FACEBOOK_APP_SECRET"),
    "page_access_token": os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN"),
    "page_id": os.getenv("FACEBOOK_PAGE_ID"),
    "instagram_account_id": os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
}
```

## Testing

### Run Test Suite

```bash
python AI_Employee_Vault/scripts/test_facebook_mcp.py "../AI_Employee_Vault"
```

### Expected Output

```
======================================================================
  FACEBOOK/INSTAGRAM MCP - TEST SUITE
======================================================================

[OK] FacebookMCP module imported
[OK] Facebook MCP initialized

TEST 1: Create Facebook Post Draft
[PASS] Facebook post draft created: FB_POST_20260307_180245.md

TEST 2: Create Instagram Post Draft
[PASS] Instagram post draft created: IG_POST_20260307_180245.md

TEST 3: Create Facebook Post with Link
[PASS] Facebook post with link created

TEST 4: Process Approved Posts
[PASS] Processed 1 approved post(s)

Total: 4/4 tests passed (100.0%)
[SUCCESS] ALL TESTS PASSED!
```

## Complete Workflow Example

```bash
# 1. AI creates post based on business goals
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" ^
  --post "Excited to announce our Q1 results! Revenue up 45% 🚀 #growth #business"

# 2. Review draft
# File created: Pending_Approval/FB_POST_20260307_*.md

# 3. Human approves (move to Approved/)
move Pending_Approval\FB_POST_*.md Approved\

# 4. Publish via Graph API
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" --post-approved

# Output:
# [INFO] Posting to Facebook: Excited to announce...
# [OK] Facebook post published! ID: 1234567890_9876543210
# ======================================================================
#   POSTS PUBLISHED: 1
# ======================================================================

# 5. Logged to Logs/facebook_2026-03-07.json
```

## Resources

- [Facebook Graph API Documentation](https://developers.facebook.com/docs/graph-api)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer)
- [Facebook SDK for Python](https://github.com/mobolic/facebook-sdk)
- [Access Token Debugger](https://developers.facebook.com/tools/debug/access_token)
- [Setup Guide](../FACEBOOK_GRAPH_API_SETUP.md)

## Comparison: Graph API vs Playwright

| Feature | Graph API (Recommended) | Playwright |
|---------|------------------------|------------|
| **Official Support** | ✅ Yes (Meta) | ❌ No |
| **Reliability** | ✅ High | ⚠️ Medium |
| **Rate Limits** | ✅ Clear limits | ⚠️ Account risk |
| **Features** | ✅ Full API | ⚠️ Limited |
| **Maintenance** | ✅ Low | ⚠️ High |
| **Terms of Service** | ✅ Compliant | ⚠️ Gray area |
| **Instagram Support** | ✅ Full | ⚠️ Limited |

**Recommendation:** Always use Graph API for production!

---

**Your AI Employee uses the official Graph API - no browser automation needed!** ✅
