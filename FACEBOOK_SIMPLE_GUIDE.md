# Facebook Auto-Posting & Comment Detection - Simple Guide

**Easy-to-understand guide for AI Employee Facebook automation**

---

## Part 1: Auto-Posting How It Works

### The Complete Flow (Simple)

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: Something Happens (Trigger)                             │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: AI Writes a Post                                        │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: Save Draft to File                                      │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: You Review & Approve                                    │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: Post to Facebook Automatically                          │
└─────────────────────────────────────────────────────────────────┘
```

---

### STEP 1: Something Happens (Trigger)

**What can trigger a post?**

| Trigger | Example |
|---------|---------|
| **Email received** | Client asks for update |
| **WhatsApp message** | Lead asks about pricing |
| **Scheduled time** | Every day at 9 AM |
| **Business milestone** | Reached 100 clients |
| **Manual** | You want to post something |

**Example:**
```
Email arrives: "Can you send me an update on your services?"
       ↓
Gmail Watcher detects it
       ↓
Creates file: Needs_Action/EMAIL_client_update.md
```

---

### STEP 2: AI Writes a Post

**AI Employee reads the trigger and creates post content:**

```python
# AI thinks:
"Client asked about services → Create promotional post"

# AI generates:
🎉 Exciting news! Our AI Employee system helps businesses:

✅ Auto-post to Facebook & Instagram
✅ Detect and respond to comments
✅ Save 10+ hours per week

Want to learn more? Visit our website!

#automation #AI #business #productivity
```

---

### STEP 3: Save Draft to File

**The post is saved as a Markdown file:**

📁 `Pending_Approval/FB_POST_20260308_093000.md`

```markdown
---
type: facebook_post_request
message: 🎉 Exciting news! Our AI Employee system...
platform: facebook
created: 2026-03-08T09:30:00
character_count: 156
status: pending
---

# Facebook Post Draft

## Content
🎉 Exciting news! Our AI Employee system helps businesses:

✅ Auto-post to Facebook & Instagram
✅ Detect and respond to comments
✅ Save 10+ hours per week

Want to learn more? Visit our website!

#automation #AI #business #productivity

## To Approve
Move this file to `/Approved` folder to post.
```

---

### STEP 4: You Review & Approve

**You see a notification** (file in Pending_Approval folder)

**You review:**
- ✅ Content looks good
- ✅ Hashtags are relevant
- ✅ No typos
- ✅ Link is correct (if any)

**You approve by moving the file:**

```bash
# Move from Pending_Approval to Approved
move Pending_Approval\FB_POST_20260308_093000.md Approved\
```

---

### STEP 5: Post to Facebook Automatically

**Run the posting command:**

```bash
python facebook_poster.py "../AI_Employee_Vault" --post-approved
```

**What happens internally:**

```python
# 1. Find all approved posts
approved_files = [
    "Approved/FB_POST_20260308_093000.md"
]

# 2. For each post, read content
post_data = {
    "message": "🎉 Exciting news!...",
    "platform": "facebook"
}

# 3. Call Facebook Graph API
import facebook

graph = facebook.GraphAPI(
    access_token="YOUR_PAGE_ACCESS_TOKEN",
    version="18.0"
)

result = graph.put_object(
    parent_object="PAGE_ID",
    connection_name="feed",
    message=post_data["message"]
)

# Returns: {'id': '1234567890_9876543210'}
print(f"[OK] Facebook post posted! ID: {result['id']}")

# 4. Move file to Done folder
move Approved\FB_POST_*.md Done\

# 5. Log the action
Logs/facebook_2026-03-08.json:
{
    "timestamp": "2026-03-08T09:30:00",
    "action": "facebook_post",
    "post_id": "1234567890_9876543210",
    "result": "success"
}
```

**Result:** Your post appears on Facebook! 🎉

---

## Part 2: Comment Detection How It Works

### The Complete Flow (Simple)

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: Watcher Runs Every 5 Minutes                            │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: Fetch New Comments from Facebook                        │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: Analyze Each Comment (Type & Priority)                  │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: Create Alert File with AI Response                      │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: You Review & Send Reply                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### STEP 1: Watcher Runs Every 5 Minutes

**A background script runs continuously:**

```bash
# Start the comment watcher
python facebook_comment_watcher.py "../AI_Employee_Vault"

# Output:
[INFO] Starting Facebook Comment Watcher...
[INFO] Checking every 300 seconds (5 minutes)
```

**What it does:**
- Wakes up every 5 minutes
- Checks Facebook for new comments
- Goes back to sleep

---

### STEP 2: Fetch New Comments from Facebook

**Watcher calls Facebook Graph API:**

```python
import facebook

graph = facebook.GraphAPI(
    access_token="YOUR_PAGE_ACCESS_TOKEN",
    version="18.0"
)

# Get recent posts with comments
posts = graph.get_connections(
    id="PAGE_ID",
    connection_name="feed",
    fields="comments,message,created_time"
)

# Extract comments from last 1 hour
comments = []
for post in posts["data"]:
    if "comments" in post:
        for comment in post["comments"]["data"]:
            comments.append(comment)
```

**Example comment received:**
```json
{
    "id": "1234567890",
    "from": {"name": "John Smith"},
    "message": "How much does your service cost?",
    "created_time": "2026-03-08T14:30:00+0000"
}
```

---

### STEP 3: Analyze Each Comment

**AI analyzes the comment to determine:**

#### A. Type of Comment

| Type | Keywords | Example |
|------|----------|---------|
| **Inquiry** | price, cost, how much, quote | "How much does this cost?" |
| **Complaint** | problem, issue, broken, wrong | "This isn't working!" |
| **Positive** | great, love, thank, awesome | "Love your product!" |
| **Urgent** | urgent, asap, emergency | "Need help ASAP!" |
| **General** | (no keywords) | "Nice post!" |

#### B. Priority Level

| Priority | When |
|----------|------|
| **High** | Urgent or Complaint |
| **Medium** | Inquiry (sales opportunity) |
| **Low** | Positive feedback |
| **Normal** | General comments |

**Example Analysis:**

```python
comment = "How much does your service cost?"

# AI scans for keywords:
# - "cost" → inquiry keyword found!
# - "how much" → inquiry keyword found!

# Classification:
{
    "type": "inquiry",
    "priority": "medium",  # Sales opportunity!
    "requires_response": True
}
```

---

### STEP 4: Create Alert File with AI Response

**Watcher creates an alert file:**

📁 `Needs_Action/COMMENT_123456_20260308_143000.md`

```markdown
---
type: facebook_comment
comment_id: 1234567890
from_name: John Smith
message: How much does your service cost?
priority: medium
comment_type: inquiry
requires_response: true
status: pending
---

# Facebook Comment Alert

## Comment Details
- **From**: John Smith
- **Time**: 2026-03-08 14:30
- **Priority**: MEDIUM (Sales opportunity!)
- **Type**: inquiry

## Comment Text
> How much does your service cost?

## Suggested Actions
- [ ] Respond with pricing information
- [ ] Send DM for detailed discussion
- [ ] Create lead in CRM

## AI Suggested Response
> Hi John! Thanks for your interest. I'd be happy to 
> provide pricing information. I'll send you a DM with 
> details. Looking forward to helping you!

## Quick Links
- [View on Facebook](https://facebook.com/post123)
- [Reply via Facebook](https://facebook.com/post123)
```

**You get notified** (file appears in Needs_Action folder)

---

### STEP 5: You Review & Send Reply

**You open the file and see:**
- The comment
- Classification (inquiry, medium priority)
- AI-suggested response

**You review the suggested response:**
- ✅ Looks good
- ✅ Professional tone
- ✅ Addresses the question

**You approve:**

```bash
# Move to Approved folder
move Needs_Action\COMMENT_*.md Approved\
```

**Send the reply:**

```bash
python facebook_poster.py "../AI_Employee_Vault" --send-approved-replies
```

**What happens internally:**

```python
# Read approved reply
reply_data = {
    "comment_id": "1234567890",
    "message": "Hi John! Thanks for your interest..."
}

# Call Facebook Graph API to reply
graph.put_comment(
    parent_object=reply_data["comment_id"],
    message=reply_data["message"]
)

# Move to Done
move Approved\COMMENT_*.md Done\

# Log
Logs/facebook_comments_2026-03-08.json:
{
    "timestamp": "2026-03-08T14:35:00",
    "comment_id": "1234567890",
    "from": "John Smith",
    "type": "inquiry",
    "response_sent": true
}
```

**Result:** Reply posted to Facebook! ✅

---

## Real Examples

### Example 1: Auto-Post from Email

```
📧 Email arrives: "Can you share your success story?"
    ↓
🤖 AI creates post:
    "🎉 We just reached 100 clients! Thank you for 
    trusting us. Here's to continued growth! 🚀
    #milestone #100clients #grateful"
    ↓
📁 Draft saved: Pending_Approval/FB_POST_*.md
    ↓
👤 You review and move to Approved/
    ↓
📤 Posted to Facebook automatically
    ↓
✅ Result: 50 likes, 10 comments, 5 new leads
```

---

### Example 2: Comment Detection - Sales Inquiry

```
💬 Comment on Facebook: "What's the pricing for 50 users?"
    ↓
🔍 Watcher detects (running every 5 min)
    ↓
🤖 AI classifies:
    - Type: inquiry
    - Priority: medium (sales opportunity!)
    - Requires response: Yes
    ↓
📁 Alert created: Needs_Action/COMMENT_*.md
    - AI suggests: "Hi! Thanks for interest. Our 
      pricing for 50 users starts at $400/month..."
    ↓
👤 You review and approve
    ↓
📤 Reply sent via Facebook API
    ↓
✅ Result: Lead captured, deal closed!
```

---

### Example 3: Comment Detection - Complaint

```
💬 Comment on Facebook: "Your service is not working! 
                         Very disappointed!"
    ↓
🔍 Watcher detects
    ↓
🤖 AI classifies:
    - Type: complaint
    - Priority: HIGH (needs immediate attention!)
    - Requires response: Yes
    ↓
📁 Alert created with URGENT flag
    - AI suggests: "Hi, I'm very sorry to hear about 
      this issue. This isn't the experience we want.
      Please check your DMs - we're reaching out to 
      resolve this immediately."
    ↓
👤 You see HIGH priority alert, respond within 15 min
    ↓
📤 Reply sent + DM sent
    ↓
✅ Result: Issue resolved, customer retained!
```

---

## Commands You Need to Know

### Auto-Posting Commands

```bash
# Create a post draft
python facebook_poster.py "../AI_Employee_Vault" --post "Your message here"

# Create post with link
python facebook_poster.py "../AI_Employee_Vault" --post "Check this out!" --link "https://example.com"

# Create Instagram post (requires photo)
python facebook_poster.py "../AI_Employee_Vault" --instagram --post "New product!" --photo "image.jpg"

# After moving drafts to Approved/, publish them
python facebook_poster.py "../AI_Employee_Vault" --post-approved
```

### Comment Detection Commands

```bash
# Start comment watcher (runs continuously)
python facebook_comment_watcher.py "../AI_Employee_Vault"

# Start with custom check interval (every 1 minute)
python facebook_comment_watcher.py "../AI_Employee_Vault" --check-interval 60

# Test mode (run once, then exit)
python facebook_comment_watcher.py "../AI_Employee_Vault" --once
```

### File Management

```bash
# Approve a post draft
move Pending_Approval\FB_POST_*.md Approved\

# Approve a comment response
move Needs_Action\COMMENT_*.md Approved\

# Reject (move to rejected folder)
move Pending_Approval\FB_POST_*.md Rejected\
```

---

## Setup Checklist

### To Enable Auto-Posting:

- [ ] Get Facebook Page Access Token
- [ ] Update `facebook_config.json` with token
- [ ] Install facebook-sdk: `pip install facebook-sdk`
- [ ] Test: `python test_facebook_mcp.py "../AI_Employee_Vault"`
- [ ] Create first post: `python facebook_poster.py "../AI_Employee_Vault" --post "Hello!"`

### To Enable Comment Detection:

- [ ] Ensure token has `pages_read_user_content` permission
- [ ] Start watcher: `python facebook_comment_watcher.py "../AI_Employee_Vault"`
- [ ] Test with a real comment on your Facebook post
- [ ] Check Needs_Action folder for alert file

### To Enable Scheduled Posting:

```bash
# Daily post at 9 AM
schtasks /create /tn "Facebook_Daily_Post" ^
  /tr "python facebook_auto_post.py" ^
  /sc daily /st 09:00

# Check comments every 5 minutes
schtasks /create /tn "Facebook_Comment_Check" ^
  /tr "python facebook_comment_watcher.py" ^
  /sc minute /mo 5
```

---

## Visual Flow Chart

```
┌─────────────────────────────────────────────────────────────────┐
│                    FACEBOOK AUTO-POSTING                        │
└─────────────────────────────────────────────────────────────────┘

  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
  │ TRIGGER  │────▶│   AI     │────▶│  DRAFT   │────▶│  HUMAN   │
  │ Email,   │     │ WRITES   │     │  FILE    │     │  REVIEW  │
  │ Schedule │     │ CONTENT  │     │ CREATED  │     │          │
  └──────────┘     └──────────┘     └──────────┘     └──────────┘
                                                              │
  ┌──────────┐     ┌──────────┐     ┌──────────┐             │
  │   LOG    │◀────│  POSTED  │◀────│ APPROVED │◀────────────┘
  │  ACTION  │     │   TO     │     │  (Move   │
  │          │     │ FACEBOOK │     │  file)   │
  └──────────┘     └──────────┘     └──────────┘


┌─────────────────────────────────────────────────────────────────┐
│                 COMMENT DETECTION                               │
└─────────────────────────────────────────────────────────────────┘

  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
  │ WATCHER  │────▶│  FETCH   │────▶│ ANALYZE  │────▶│  CREATE  │
  │  RUNS    │     │ COMMENTS │     │ (Type &  │     │  ALERT   │
  │(5 min)   │     │          │     │ Priority)│     │   FILE   │
  └──────────┘     └──────────┘     └──────────┘     └──────────┘
                                                              │
  ┌──────────┐     ┌──────────┐     ┌──────────┐             │
  │  LOG &   │◀────│  REPLY   │◀────│  HUMAN   │◀────────────┘
  │  DONE    │     │   SENT   │     │  REVIEW  │
  │          │     │          │     │ & APPROVE│
  └──────────┘     └──────────┘     └──────────┘
```

---

## FAQ

**Q: Do I need to approve every post?**
A: Yes, by default. This is safety-first. You can enable auto-post for certain types later.

**Q: Can it post to Instagram too?**
A: Yes! Use `--instagram` flag. Requires Instagram Business account connected to Facebook Page.

**Q: How fast are comments detected?**
A: Within 5 minutes (default check interval). You can reduce to 1 minute if needed.

**Q: What if I don't respond to a comment?**
A: High-priority comments stay in Needs_Action until handled. You can set up email alerts.

**Q: Can it auto-reply without my approval?**
A: Not recommended for safety. But you can set up rules for simple comments (e.g., "Thank you" comments).

**Q: Does it work 24/7?**
A: Yes, if you run the watcher as a background service (Windows Task Scheduler).

---

## Next Steps

1. **Get your Facebook Page Access Token**
   - Go to: https://developers.facebook.com/tools/explorer
   - Generate token with required permissions

2. **Update facebook_config.json**
   ```json
   {
     "facebook": {
       "page_access_token": "EAAG...your_token_here"
     }
   }
   ```

3. **Test auto-posting**
   ```bash
   python test_facebook_mcp.py "../AI_Employee_Vault"
   ```

4. **Start comment watcher**
   ```bash
   python facebook_comment_watcher.py "../AI_Employee_Vault"
   ```

5. **Set up scheduled tasks** (optional)
   - Daily posts
   - Continuous comment monitoring

---

**That's it! Your AI Employee now handles Facebook automatically!** 🎉

**Questions?** Check the detailed guides:
- [FACEBOOK_COMPLETE_GUIDE.md](FACEBOOK_COMPLETE_GUIDE.md)
- [FACEBOOK_AUTO_POSTING_COMMENT_GUIDE.md](FACEBOOK_AUTO_POSTING_COMMENT_GUIDE.md)
- [FACEBOOK_GRAPH_API_SETUP.md](FACEBOOK_GRAPH_API_SETUP.md)
