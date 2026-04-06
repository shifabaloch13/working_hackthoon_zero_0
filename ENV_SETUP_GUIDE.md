# .env File Setup Guide for Facebook Integration

**Secure credential management for AI Employee Facebook automation**

---

## ✅ What We Did

Moved all Facebook credentials from `facebook_config.json` to `.env` file for better security.

### Before (❌ Insecure):
```json
// facebook_config.json
{
  "facebook": {
    "page_access_token": "EAAN...long_token"  // Exposed in code!
  }
}
```

### After (✅ Secure):
```bash
# .env file
FACEBOOK_PAGE_ACCESS_TOKEN=EAAN...long_token  # Not in code!
```

---

## 📁 File Locations

### Your `.env` File Location:
```
D:\Download\working_hackthoon_zero_0\.env
```

### Your Credentials (Already Configured):
```bash
# Facebook App Credentials
FACEBOOK_APP_ID=969420109076481
FACEBOOK_APP_SECRET=0d01d9c2c6d3d4663872c058b1ec6c3f

# Facebook Page Access Token (never expires)
FACEBOOK_PAGE_ACCESS_TOKEN=EAANxrrU9WAEBQwBKJz05TbYGfdsIJehZAPuWgY7ZBrXXrZAxOchobABlNpI7PMV9yZCAKPuIsMGKOWQRWhN0mBMhqrGOinsWmOWrHGab6gvt3BozvMVQaVAwGFtA6sZCTFWRuxjJsOo6xl7oUcV2ZAy9lbpP7KNeRk4d0gO26q3wgOpOtCoL2dZABu7ZCUIzbgTgzbjkQLpsD7gP8C2dVGcH6yqbuijGJhsTwJsVRpVKayEZD

# Facebook Page ID
FACEBOOK_PAGE_ID=1004531386081562

# Graph API Version
FACEBOOK_GRAPH_API_VERSION=18.0

# Instagram (optional - update when you have Instagram Business)
INSTAGRAM_BUSINESS_ACCOUNT_ID=YOUR_INSTAGRAM_BUSINESS_ACCOUNT_ID
```

---

## 🔒 Why Use .env File?

### Security Benefits:

| Aspect | facebook_config.json | .env File |
|--------|---------------------|-----------|
| **Git Safety** | ❌ Can be accidentally committed | ✅ Always in .gitignore |
| **Code Separation** | ❌ Credentials in config | ✅ Credentials separate from code |
| **Environment Specific** | ❌ Same for all envs | ✅ Different for dev/prod |
| **Best Practice** | ❌ No | ✅ Yes (12-factor app) |

### .gitignore Protection:

```gitignore
# .gitignore
.env                    # ← Never committed!
facebook_config.json    # ← Template only, no secrets
```

---

## 📋 How Scripts Load Credentials

### Python Scripts Now:

```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get credentials
app_id = os.getenv('FACEBOOK_APP_ID')
token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
page_id = os.getenv('FACEBOOK_PAGE_ID')
```

### No More Config File Reading:

```python
# OLD WAY (don't use)
with open('facebook_config.json') as f:
    config = json.load(f)

# NEW WAY (use this)
token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
```

---

## 🧪 Testing Your Setup

### Test .env Loading:

```bash
cd D:\Download\working_hackthoon_zero_0
python test_env.py
```

**Expected Output:**
```
============================================================
Testing .env File Loading
============================================================

Facebook Credentials:
  FACEBOOK_APP_ID: 969420109076481
  FACEBOOK_APP_SECRET: ***6c3f
  FACEBOOK_PAGE_ACCESS_TOKEN: ***VRpVKayEZD
  FACEBOOK_PAGE_ID: 1004531386081562
  FACEBOOK_GRAPH_API_VERSION: 18.0

[OK] All required Facebook credentials found!

Ready to use Facebook_auto-posting and comment detection!
```

### Test Facebook Posting:

```bash
cd D:\Download\working_hackthoon_zero_0\AI_Employee_Vault\scripts
python facebook_poster.py ../../AI_Employee_Vault --post "Test post from .env!"
```

**Expected Output:**
```
[OK] Facebook Graph API client created (v18.0)
[OK] Facebook post draft created: FB_POST_20260310_*.md
```

### Test Comment Watcher:

```bash
cd D:\Download\working_hackthoon_zero_0\AI_Employee_Vault\scripts
python facebook_comment_watcher.py ../../AI_Employee_Vault --once
```

**Expected Output:**
```
[OK] Facebook Graph API client created (v18.0)
[INFO] Running in --once mode
[INFO] Found 0 total comments
[OK] Done
```

---

## 🔑 Your Current Credentials

### Facebook App:
- **App ID:** `969420109076481`
- **App Secret:** `0d01d9c2c6d3d4663872c058b1ec6c3f`

### Facebook Page:
- **Page ID:** `1004531386081562`
- **Page Access Token:** `EAANxrrU9WAEBQwBKJz05TbYGfds...` (long token)

### Status:
✅ All credentials loaded from `.env`
✅ Scripts configured to use environment variables
✅ `facebook_config.json` cleaned (no secrets)

---

## 🛡️ Security Best Practices

### 1. Never Share .env File

```bash
# ❌ DON'T:
git add .env
git commit -m "Add credentials"

# ✅ DO:
echo ".env" >> .gitignore
```

### 2. Use .env.template for Sharing

Create `.env.template` with placeholder values:

```bash
# .env.template (safe to commit)
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here
FACEBOOK_PAGE_ACCESS_TOKEN=your_token_here
FACEBOOK_PAGE_ID=your_page_id_here
```

### 3. Backup Your .env Securely

```bash
# Store in password manager
# Or encrypted backup
# NOT in git!
```

---

## 📁 Project Structure

```
D:\Download\working_hackthoon_zero_0\
├── .env                          ← YOUR SECRETS HERE (never commit!)
├── .env.template                 ← Safe template (can commit)
├── .gitignore                    ← Includes .env
├── facebook_config.json          ← Template only (no secrets)
├── test_env.py                   ← Test script
├── AI_Employee_Vault/
│   └── scripts/
│       ├── facebook_poster.py    ← Loads from .env
│       └── facebook_comment_watcher.py  ← Loads from .env
└── ...
```

---

## 🔄 Migration Complete

### What Changed:

| File | Before | After |
|------|--------|-------|
| `.env` | ❌ Didn't exist | ✅ Contains all secrets |
| `facebook_config.json` | ❌ Had secrets | ✅ Template only |
| Scripts | ❌ Read JSON file | ✅ Use `os.getenv()` |
| `.gitignore` | ❌ No .env | ✅ Blocks .env |

### Your Credentials Are Now:

✅ **More Secure** - Not in config files
✅ **Environment Isolated** - Different per environment
✅ **Git Safe** - Never accidentally committed
✅ **Best Practice** - Following 12-factor app methodology

---

## 🚀 Quick Commands

```bash
# Test .env loading
python test_env.py

# Create Facebook post
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" --post "Hello!"

# Start comment monitoring
python AI_Employee_Vault/scripts/facebook_comment_watcher.py "../AI_Employee_Vault"
```

---

## ⚠️ Important Notes

1. **Never delete `.env` file** - Your credentials will be lost
2. **Never commit `.env` to git** - It's in `.gitignore` for a reason
3. **Update `.env` when rotating tokens** - Keep it current
4. **Backup `.env` securely** - Password manager recommended

---

## 🆘 Troubleshooting

### Error: "No Facebook credentials found"

**Solution:**
1. Check `.env` file exists at: `D:\Download\working_hackthoon_zero_0\.env`
2. Verify credentials are not empty
3. Restart Python script

### Error: "python-dotenv not installed"

**Solution:**
```bash
pip install python-dotenv
```

### Error: "Invalid token"

**Solution:**
1. Check token in `.env` is copied correctly (no extra spaces)
2. Regenerate token from Graph API Explorer
3. Update `.env` file

---

**Your credentials are now securely managed in `.env`!** ✅

**Questions?** Check the main guides:
- [FACEBOOK_SIMPLE_GUIDE.md](FACEBOOK_SIMPLE_GUIDE.md)
- [FACEBOOK_COMPLETE_GUIDE.md](FACEBOOK_COMPLETE_GUIDE.md)
