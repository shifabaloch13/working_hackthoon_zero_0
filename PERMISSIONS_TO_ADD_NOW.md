# Facebook Permissions - Priority List

**Add these permissions NOW in order of importance**

---

## 🔴 CRITICAL (Must Add - Core Functionality)

### 1. `pages_read_engagement`
**What it does:** Allows reading comments on your Facebook posts

**Why you need it:** 
- Detect comments on your posts
- Monitor engagement (likes, shares, comments)
- AI can respond to comments

**Without this:** Comment detection WON'T work ❌

---

### 2. `pages_read_user_content`
**What it does:** Allows reading user-generated content (comments, messages)

**Why you need it:**
- Read comment text
- Access user names and profiles
- Detect urgent comments

**Without this:** Can't read comment content ❌

---

### 3. `pages_manage_posts`
**What it does:** Create and publish posts to your Page

**Why you need it:**
- Auto-post to Facebook
- Schedule posts
- Post with images/links

**Without this:** Auto-posting WON'T work ❌

---

## 🟡 IMPORTANT (Add If Using Instagram)

### 4. `instagram_basic`
**What it does:** Access Instagram Business account info

**Why you need it:**
- Connect Instagram Business account
- Get Instagram account ID
- Basic Instagram features

**Without this:** Instagram integration won't work (but Facebook still works) ⚠️

---

### 5. `instagram_content_publish`
**What it does:** Post to Instagram Business account

**Why you need it:**
- Auto-post to Instagram
- Cross-post from Facebook to Instagram

**Without this:** Can't post to Instagram (but Facebook still works) ⚠️

---

## 🟢 OPTIONAL (Nice to Have - Add Later)

### 6. `pages_manage_metadata`
**What it does:** Manage Page settings and info

**Why you might want it:**
- Update Page info
- Manage Page settings

**Without this:** Core features still work ✅

---

### 7. `pages_show_list`
**What it does:** List Pages you manage

**Why you might want it:**
- See all your Pages in one place

**Without this:** Core features still work ✅

---

## 📋 Quick Copy List

### For Facebook Auto-Posting + Comment Detection (REQUIRED):
```
pages_manage_posts
pages_read_engagement
pages_read_user_content
```

### For Instagram Too (OPTIONAL):
```
instagram_basic
instagram_content_publish
```

---

## 🚀 How to Add (Step-by-Step)

### Step 1: Go to App Review
```
https://developers.facebook.com/apps/969420109076481/app-review/
```

### Step 2: Click "Permissions and Features"

### Step 3: Add Each Permission

For each permission in the **CRITICAL** list above:

1. Click **"Add Permission"**
2. Search for permission name (e.g., `pages_read_engagement`)
3. Click on it to add
4. Toggle to **ON**

### Step 4: For Each Permission, Facebook Asks:

**Q: What data does this permission access?**

**Your Answer:**
> "Access to Facebook Page comments and posts for automated social media management."

**Q: How does your app use this permission?**

**Your Answer:**
> "The AI Employee app monitors comments on our Facebook Page and automatically creates posts to keep our audience engaged."

**Q: Does your app use any of these permissions or features?**

**Your Answer:**
> Select "Yes" if applicable

**Q: Provide a video or detailed description**

**Your Answer:**
> Record a quick screen recording showing:
> 1. You generating an access token
> 2. Creating a post
> 3. Reading comments
> 
> OR write detailed description:
> "User logs in, grants Page permissions, app creates posts and monitors comments automatically."

### Step 5: Save & Submit

1. Click **"Save Changes"** for each permission
2. Click **"Submit for Review"** at the top
3. Wait for approval (usually 1-3 business days)

---

## ⚡ Quick Tip: Use During Development

While waiting for approval, you can still use these permissions for **testing on your own Page**:

1. You're the Page owner
2. You can grant yourself permissions
3. No approval needed for testing on your own Page

**Just regenerate your token with the permissions selected:**

1. Go to: https://developers.facebook.com/tools/explorer/?app_id=969420109076481
2. Select your app
3. Click **"Generate Access Token"**
4. **Select all 3 CRITICAL permissions**
5. Copy the token
6. Update `.env` file

---

## ✅ After Adding Permissions

### Test Immediately:

```bash
# Test comment detection
cd D:\Download\working_hackthoon_zero_0\AI_Employee_Vault\scripts
python facebook_comment_watcher.py ../../AI_Employee_Vault --once
```

**If working, you'll see:**
```
[OK] Facebook Graph API client created
[INFO] Found X new comment(s)
[OK] Created: COMMENT_*.md
```

**If still waiting for approval:**
```
[ERROR] This endpoint requires the 'pages_read_engagement' permission
```

---

## 📊 Permission Checklist

Print this and check off as you add each one:

```
CRITICAL (Add These First):
☐ pages_manage_posts
☐ pages_read_engagement  
☐ pages_read_user_content

OPTIONAL (For Instagram):
☐ instagram_basic
☐ instagram_content_publish

NICE TO HAVE (Add Later):
☐ pages_manage_metadata
☐ pages_show_list
```

---

## 🎯 Minimum Viable Set

**If you only add 3 permissions, add these:**

```
1. pages_manage_posts      ← For posting
2. pages_read_engagement   ← For reading comments
3. pages_read_user_content ← For comment detection
```

**These 3 give you 100% of core Facebook functionality!**

---

## 🔗 Direct Links

### Add Permissions:
```
https://developers.facebook.com/apps/969420109076481/permissions/
```

### Graph API Explorer (Test):
```
https://developers.facebook.com/tools/explorer/?app_id=969420109076481
```

### App Review Status:
```
https://developers.facebook.com/apps/969420109076481/app-review/
```

---

## 🆘 If You Get Stuck

### Error: "Permission Denied"
**Solution:** Make sure you selected the permission when generating token

### Error: "Requires Review"
**Solution:** This is normal! Submit for review. You can still test on your own Page.

### Error: "Invalid Token"
**Solution:** Regenerate token with new permissions selected

---

## ✅ Summary

### Add These 3 NOW:
```
✅ pages_manage_posts
✅ pages_read_engagement
✅ pages_read_user_content
```

### Add These Later (If Using Instagram):
```
⚪ instagram_basic
⚪ instagram_content_publish
```

**That's it! Add the 3 critical permissions and you're done!** 🚀

---

**Questions?** Check: [FINAL_STATUS_WITH_PERMISSIONS.md](FINAL_STATUS_WITH_PERMISSIONS.md)
