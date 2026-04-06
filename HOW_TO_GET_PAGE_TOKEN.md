# How to Get Page Access Token (Not User Token)

**Important:** You need a PAGE token, not a USER token!

---

## ❌ The Problem

Your current token is a **User Access Token**. You need a **Page Access Token**.

**Error you're seeing:**
```
(#200) Requires both pages_read_engagement and pages_manage_posts 
as an admin with sufficient administrative permission
```

---

## ✅ Solution: Get Page Access Token

### Step 1: Go to Graph API Explorer

```
https://developers.facebook.com/tools/explorer/?app_id=969420109076481
```

### Step 2: Generate USER Token First

1. Click **"Generate Access Token"**
2. Select your app
3. Select these permissions:
   - ✅ `pages_manage_posts`
   - ✅ `pages_read_engagement`
   - ✅ `pages_read_user_content`
4. Click **"Generate Token"**
5. Log in and approve permissions

### Step 3: Get PAGE Token

**This is the important step!**

In the same Graph API Explorer, run this query:

```
GET /me/accounts
```

Click **"Submit"**

### Step 4: Copy the PAGE Access Token

You'll see a response like:

```json
{
  "data": [
    {
      "name": "Your Page Name",
      "id": "1004531386081562",
      "access_token": "EAANxrrU9WAEBQ...THIS_IS_YOUR_PAGE_TOKEN"
    }
  ]
}
```

**Copy the `access_token` value** - this is your **Page Access Token**!

### Step 5: Update .env File

Edit `D:\Download\working_hackthoon_zero_0\.env`:

```bash
# Replace this:
FACEBOOK_PAGE_ACCESS_TOKEN=EAAN... (your old user token)

# With this:
FACEBOOK_PAGE_ACCESS_TOKEN=EAAN... (the NEW page token you just copied)
```

### Step 6: Test Posting

```bash
cd D:\Download\working_hackthoon_zero_0\AI_Employee_Vault\scripts
python facebook_poster.py ../../AI_Employee_Vault --post "Testing page token!"
```

Move to Approved:
```bash
cd ..
move Pending_Approval\FB_POST_*.md Approved\
cd scripts
python facebook_poster.py ../../AI_Employee_Vault --post-approved
```

**Expected:** 
```
[OK] Facebook post posted! ID: 1234567890_9876543210
[OK] View post: https://facebook.com/1234567890_9876543210
```

---

## 🔍 How to Tell User Token vs Page Token

### User Token:
- Usually shorter
- Used for personal profile actions
- ❌ Won't work for posting to Page

### Page Token:
- Usually longer
- Used for Page actions
- ✅ Required for posting to your Page
- Never expires!

---

## 📋 Quick Summary

```
1. Go to Graph API Explorer
2. Generate USER token with permissions
3. Run: GET /me/accounts
4. Copy the PAGE access_token (not user token!)
5. Update .env file
6. Test posting
```

---

## 🆘 Still Having Issues?

### Make sure:
- You're admin of the Page
- Token starts with `EAAN`
- You selected all 3 permissions
- You copied the token from `/me/accounts` response (not the initial token)

---

**After getting Page Token, posting will work!** ✅
