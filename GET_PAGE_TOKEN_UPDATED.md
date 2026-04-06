# Get Page Access Token - Updated Method

**The `/me/accounts` endpoint requires the user token first. Here's the correct flow:**

---

## ✅ Correct Steps to Get Page Access Token

### Step 1: Generate User Token WITH Permissions

1. Go to: https://developers.facebook.com/tools/explorer/?app_id=969420109076481

2. Click **"Generate Access Token"**

3. **BEFORE clicking generate, select these permissions:**
   - ✅ `pages_manage_posts`
   - ✅ `pages_read_engagement`  
   - ✅ `pages_read_user_content`
   - ✅ `manage_pages` (if available)

4. Click **"Generate Access Token"**

5. Log in and **Approve** the permissions

### Step 2: Now Run /me/accounts

**After you have the user token:**

1. In the Graph API Explorer, at the top you'll see your token

2. In the query box (where it says "Enter a Graph API query..."), type:
   ```
   /me/accounts
   ```

3. Make sure **"GET"** is selected (not POST)

4. Click **"Submit"**

### Step 3: Copy Page Access Token

You should see:

```json
{
  "data": [
    {
      "name": "Your Page Name",
      "id": "1004531386081562",
      "access_token": "EAANxrrU9WAEBQ...VERY_LONG_TOKEN_HERE"
    }
  ]
}
```

**Copy the `access_token` value** - this is your **Page Access Token**!

---

## 🔄 Alternative Method (If /me/accounts Doesn't Work)

### Method 2: Get Token from Page Settings

1. Go to: https://www.facebook.com/1004531386081562

2. Go to your Page

3. Click **Settings** → **New Page Experience** (or **Page Access** in old layout)

4. Click **Generate Access Token** or **Get Token**

5. Copy the token shown

---

### Method 3: Use Access Token Tool

1. Go to: https://developers.facebook.com/tools/accesstoken/

2. Select your app

3. Click **"Get Token"** → **"Get Page Access Token"**

4. Select your Page from the list

5. Copy the token

---

## 🎯 Quickest Method (Recommended)

### Use This Direct Link:

```
https://developers.facebook.com/tools/explorer/permissions/explorer/?app_id=969420109076481
```

1. Select permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`

2. Click **"Generate Token"**

3. After token is generated, scroll down to **"Page"** section

4. Select your Page

5. The token will change to a **Page Token**

6. Copy that token!

---

## ✅ After Getting Page Token

Give me the token and I'll update your `.env` file!

It should look like:
```
EAANxrrU9WAEBQ... (very long, 200+ characters)
```

---

## 🆘 If Nothing Works

### Try This Direct Query:

In Graph API Explorer, run:

```
GET /1004531386081562?fields=access_token&access_token=YOUR_USER_TOKEN
```

Replace `YOUR_USER_TOKEN` with the user token you generated.

This will return:
```json
{
  "access_token": "EAAN...PAGE_TOKEN_HERE",
  "id": "1004531386081562"
}
```

---

**Once you get the Page Access Token, share it and I'll update `.env`!** 🚀
