# Facebook Graph API Setup Guide

This guide walks you through setting up Facebook Graph API integration for the AI Employee.

---

## Overview

The AI Employee uses the **official Facebook Graph API** (via `facebook-sdk`) to:
- Post to Facebook Pages
- Post to Instagram Business accounts
- Read engagement metrics
- Manage comments and messages

**No Playwright/browser automation** - pure API integration.

---

## Step 1: Create Facebook Developer Account

1. Go to https://developers.facebook.com
2. Click **Get Started** or **Log In**
3. Complete developer account verification (may require phone verification)

---

## Step 2: Create a Facebook App

1. Click **My Apps** → **Create App**
2. Select app type: **Business**
3. Fill in app details:
   - **App Name**: AI Employee Social Media
   - **App Contact Email**: your-email@example.com
4. Click **Create App**
5. Complete security verification

---

## Step 3: Configure App Permissions

Add these products to your app:

### Facebook Login
1. In App Dashboard, click **Add Product** → **Facebook Login**
2. Select **Facebook Login for Business**
3. Configure settings:
   - **Valid OAuth Redirect URIs**: `https://localhost`
   - **App Domain**: `localhost` (for development)

### Graph API Permissions

Request these permissions:

| Permission | Purpose | Review Required |
|------------|---------|-----------------|
| `pages_manage_posts` | Create posts on Pages | Yes |
| `pages_read_engagement` | Read Page insights | Yes |
| `pages_read_user_content` | Read Page content | Yes |
| `instagram_basic` | Basic Instagram access | Yes |
| `instagram_content_publish` | Publish to Instagram | Yes |
| `instagram_manage_insights` | Read Instagram insights | Yes |

---

## Step 4: Get Page Access Token

### Option A: Using Graph API Explorer (Recommended for Testing)

1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer)
2. Select your app from dropdown
3. Click **Generate Access Token**
4. Select permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `instagram_basic`
   - `instagram_content_publish`
5. Click **Generate Token**
6. Copy the **Access Token**

### Option B: Using OAuth Flow (Production)

```python
# Get User Token first
import requests

app_id = "YOUR_APP_ID"
app_secret = "YOUR_APP_SECRET"
redirect_uri = "https://localhost"

# Step 1: Get authorization URL
auth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope=pages_manage_posts,pages_read_engagement,instagram_basic,instagram_content_publish"

print(f"Visit this URL: {auth_url}")

# Step 2: After authorization, exchange code for token
code = input("Enter the code from redirect URL: ")

token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
params = {
    "client_id": app_id,
    "redirect_uri": redirect_uri,
    "client_secret": app_secret,
    "code": code
}

response = requests.get(token_url, params=params)
user_token = response.json()["access_token"]

# Step 3: Exchange for long-lived token
long_lived_url = "https://graph.facebook.com/v18.0/oauth/access_token"
params = {
    "grant_type": "fb_exchange_token",
    "client_id": app_id,
    "client_secret": app_secret,
    "fb_exchange_token": user_token
}

response = requests.get(long_lived_url, params=params)
long_lived_token = response.json()["access_token"]

print(f"Long-lived token: {long_lived_token}")
```

### Get Page Access Token

```python
import requests

page_id = "YOUR_PAGE_ID"
user_token = "YOUR_USER_TOKEN"

# Get Page Token
url = f"https://graph.facebook.com/v18.0/{page_id}?fields=access_token&access_token={user_token}"
response = requests.get(url)
page_token = response.json()["access_token"]

print(f"Page Access Token: {page_token}")
```

---

## Step 5: Get Page ID and Instagram Account ID

### Get Page ID

```bash
curl -X GET "https://graph.facebook.com/v18.0/me/accounts?access_token=YOUR_USER_TOKEN"
```

Response:
```json
{
  "data": [
    {
      "name": "Your Page Name",
      "id": "1234567890",
      "access_token": "EAAG..."
    }
  ]
}
```

### Get Instagram Business Account ID

1. Your Instagram account must be a **Business Account**
2. It must be connected to your Facebook Page

```bash
curl -X GET "https://graph.facebook.com/v18.0/YOUR_PAGE_ID?fields=instagram_business_account&access_token=YOUR_PAGE_TOKEN"
```

Response:
```json
{
  "instagram_business_account": {
    "id": "17841400000000000"
  }
}
```

---

## Step 6: Create Configuration File

Create `facebook_config.json` in your project root:

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

**Security Note:** Never commit this file to version control!

Add to `.gitignore`:
```
facebook_config.json
```

---

## Step 7: Install Facebook SDK

```bash
pip install facebook-sdk requests
```

---

## Step 8: Test the Integration

### Test Connection

```python
import facebook

# Initialize Graph API
graph = facebook.GraphAPI(access_token="YOUR_PAGE_ACCESS_TOKEN", version="v18.0")

# Test by getting Page info
page = graph.get_object(id="YOUR_PAGE_ID")
print(f"Connected to Page: {page['name']}")
```

### Test Posting

```python
import facebook

graph = facebook.GraphAPI(access_token="YOUR_PAGE_ACCESS_TOKEN", version="v18.0")

# Post to Facebook
result = graph.put_object(
    parent_object="YOUR_PAGE_ID",
    connection_name="feed",
    message="Hello from AI Employee! #automation"
)

print(f"Post created! ID: {result['id']}")
```

### Test Instagram Posting

```python
import requests

access_token = "YOUR_PAGE_ACCESS_TOKEN"
ig_account_id = "YOUR_INSTAGRAM_ACCOUNT_ID"

# Step 1: Create media container
image_url = "https://example.com/image.jpg"
caption = "Hello Instagram! #automation"

container_url = f"https://graph.facebook.com/v18.0/{ig_account_id}/media"
container_params = {
    "image_url": image_url,
    "caption": caption,
    "access_token": access_token
}

container_response = requests.post(container_url, params=container_params)
container_id = container_response.json()["id"]

# Step 2: Publish the media
publish_url = f"https://graph.facebook.com/v18.0/{ig_account_id}/media_publish"
publish_params = {
    "creation_id": container_id,
    "access_token": access_token
}

publish_response = requests.post(publish_url, params=publish_params)
media_id = publish_response.json()["id"]

print(f"Instagram post created! ID: {media_id}")
```

---

## Step 9: Run AI Employee Facebook MCP

```bash
# Create Facebook post draft
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" ^
  --post "Exciting news from AI Employee! 🚀 #automation #AI"

# Review draft in Pending_Approval/

# Move to Approved/ folder

# Publish
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" --post-approved
```

---

## Troubleshooting

### Error: Invalid OAuth Access Token

**Cause:** Token expired or invalid

**Solution:**
1. Generate new long-lived token
2. Update `facebook_config.json`

### Error: Missing Permissions

**Cause:** App permissions not approved

**Solution:**
1. Go to App Dashboard → App Review
2. Submit permissions for review
3. Use test users during development

### Error: Instagram Account Not Found

**Cause:** Instagram not connected to Facebook Page

**Solution:**
1. Go to Facebook Page Settings
2. Connect Instagram Business account
3. Ensure account is Business (not Personal)

---

## Token Expiration

| Token Type | Expiration | Use Case |
|------------|------------|----------|
| User Token (Short-lived) | 1-2 hours | Testing |
| User Token (Long-lived) | 60 days | Development |
| Page Token | Never | Production |

**Best Practice:** Use Page Tokens for production - they don't expire!

---

## Rate Limits

| Action | Limit |
|--------|-------|
| Posts per day | 25 per Page |
| API calls per hour | 200 per user |
| Instagram posts per day | 25 per account |

---

## App Review Checklist

Before going to production:

1. ✅ Complete App Verification
2. ✅ Submit all permissions for review
3. ✅ Provide screencast of app usage
4. ✅ Complete privacy policy URL
5. ✅ Complete terms of service URL
6. ✅ Pass Facebook security review

---

## Resources

- [Facebook Graph API Documentation](https://developers.facebook.com/docs/graph-api)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer)
- [Facebook SDK for Python](https://github.com/mobolic/facebook-sdk)
- [Access Token Debugger](https://developers.facebook.com/tools/debug/access_token)

---

**Next Step:** Run `test_facebook_mcp.py` to verify integration!

```bash
python AI_Employee_Vault/scripts/test_facebook_mcp.py "../AI_Employee_Vault"
```
