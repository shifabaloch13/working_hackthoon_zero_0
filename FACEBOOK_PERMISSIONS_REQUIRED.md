# Facebook Permissions Required - Complete List

**All permissions your AI Employee needs for full functionality**

---

## ✅ Required Permissions (Must Have)

### For Auto-Posting:

| Permission | What It Does | Status |
|------------|-------------|--------|
| **`pages_manage_posts`** | Create and publish posts to your Facebook Page | ✅ Required |
| **`pages_read_engagement`** | Read engagement metrics (likes, comments, shares) | ✅ Required |

### For Comment Detection:

| Permission | What It Does | Status |
|------------|-------------|--------|
| **`pages_read_user_content`** | Read comments and messages on your Page | ✅ Required |
| **`pages_read_engagement`** | Access comments on posts | ✅ Required |

### For Instagram (Optional):

| Permission | What It Does | Status |
|------------|-------------|--------|
| **`instagram_basic`** | Access Instagram Business account info | ⚠️ Optional |
| **`instagram_content_publish`** | Post to Instagram Business account | ⚠️ Optional |

---

## 📋 Complete Permission List

### Copy This List:

```
pages_manage_posts
pages_read_engagement
pages_read_user_content
instagram_basic
instagram_content_publish
```

---

## 🔧 How to Add Permissions

### Step 1: Go to App Dashboard

```
https://developers.facebook.com/apps/969420109076481/
```

### Step 2: Navigate to App Review

1. Click **App Review** in left menu
2. Click **Permissions and Features** tab

### Step 3: Add Each Permission

For each permission in the list above:

1. Click **Add Permission**
2. Search for permission name (e.g., `pages_manage_posts`)
3. Click to add it
4. Toggle to **ON**

### Step 4: For Each Permission, Provide Details

Facebook will ask for:

1. **What data does this permission access?**
   - Answer: "We access Page posts and comments to automate social media management for business owners."

2. **How does your app use this permission?**
   - Answer: "Our AI Employee app automatically creates posts and monitors comments on behalf of Page administrators."

3. **Does your app use any of these permissions or features?**
   - Answer: Yes (if applicable)

4. **Provide screenshots/video**
   - Record a short video showing:
     - How you generate access token
     - How posts are created
     - How comments are monitored

### Step 5: Submit for Review

1. Click **Save Changes** for each permission
2. Click **Submit for Review** button
3. Wait for approval (usually 1-3 business days)

---

## ⚡ Quick Setup (For Development/Testing)

While waiting for approval, you can use **Test Users**:

### Create Test User:

1. Go to **App Dashboard** → **Roles** → **Test Users**
2. Click **Add** to create a test user
3. Generate access token for test user
4. Use test token for development

### Test with Your Own Page:

Since you're the Page owner, you can use these permissions immediately for testing on your own Page without full review.

---

## 🎯 Minimum Permissions for Basic Functionality

If you want to start **right now**, add these 3 permissions:

```
✅ pages_manage_posts      (for posting)
✅ pages_read_engagement   (for reading comments)
✅ pages_read_user_content (for comment detection)
```

**Instagram permissions can be added later.**

---

## 📝 Permission Descriptions for Facebook Review

When submitting, use these descriptions:

### pages_manage_posts
> "Allows the app to create and publish posts on behalf of Page administrators. Used for automated social media scheduling and posting."

### pages_read_engagement
> "Allows the app to read engagement metrics and comments on Page posts. Used for monitoring audience responses and generating analytics."

### pages_read_user_content
> "Allows the app to read user-generated content on the Page, including comments and messages. Used for comment detection and response automation."

### instagram_basic
> "Allows the app to access Instagram Business account information. Used for cross-platform posting to Instagram."

### instagram_content_publish
> "Allows the app to publish content to Instagram Business accounts. Used for automated Instagram posting."

---

## 🔗 Direct Links

### App Dashboard:
```
https://developers.facebook.com/apps/969420109076481/dashboard/
```

### App Review:
```
https://developers.facebook.com/apps/969420109076481/app-review/
```

### Permissions:
```
https://developers.facebook.com/apps/969420109076481/permissions/
```

### Graph API Explorer (for testing):
```
https://developers.facebook.com/tools/explorer/?app_id=969420109076481
```

---

## ✅ After Adding Permissions

### Test Your Permissions:

1. **Go to Graph API Explorer:**
   ```
   https://developers.facebook.com/tools/explorer/?app_id=969420109076481
   ```

2. **Select your app**

3. **Click "Generate Access Token"**

4. **Select all permissions you added**

5. **Test posting:**
   ```
   POST /{page-id}/feed
   message=Test post from AI Employee
   ```

6. **Test reading comments:**
   ```
   GET /{page-id}/feed?fields=comments
   ```

### Then Test in AI Employee:

```bash
# Test posting
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" --post "Testing permissions!"

# Test comment watcher
python AI_Employee_Vault/scripts/facebook_comment_watcher.py "../AI_Employee_Vault" --once
```

---

## 🚨 Common Issues

### Issue: "Permission Denied"

**Solution:**
- Make sure permission is added in App Review
- Make sure you generated token with that permission selected
- For some permissions, you need to be Page admin

### Issue: "Requires Review"

**Solution:**
- Some permissions require Facebook approval
- You can still use them with test users or your own Page during development
- Submit for review for production use

### Issue: "Token Expired"

**Solution:**
- Use Page Access Token (doesn't expire)
- Not User Access Token (expires in hours/days)
- Get token from: `GET /me/accounts`

---

## 📊 Permission Status Tracker

| Permission | Added? | Approved? | Working? |
|------------|--------|-----------|----------|
| pages_manage_posts | ⬜ | ⬜ | ⬜ |
| pages_read_engagement | ⬜ | ⬜ | ⬜ |
| pages_read_user_content | ⬜ | ⬜ | ⬜ |
| instagram_basic | ⬜ | ⬜ | ⬜ |
| instagram_content_publish | ⬜ | ⬜ | ⬜ |

**Print this and check off as you complete each step!**

---

## 🎯 Quick Checklist

- [ ] Go to App Dashboard
- [ ] Navigate to App Review → Permissions
- [ ] Add `pages_manage_posts`
- [ ] Add `pages_read_engagement`
- [ ] Add `pages_read_user_content`
- [ ] (Optional) Add `instagram_basic`
- [ ] (Optional) Add `instagram_content_publish`
- [ ] Submit for review (if required)
- [ ] Generate new access token with all permissions
- [ ] Test in AI Employee
- [ ] Verify posting works
- [ ] Verify comment detection works

---

**That's it! Add these permissions and your AI Employee will have full Facebook functionality!** 🚀

**Questions?** Check: [FINAL_FACEBOOK_STATUS.md](FINAL_FACEBOOK_STATUS.md)
