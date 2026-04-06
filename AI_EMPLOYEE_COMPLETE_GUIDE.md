# 🤖 AI Employee - Complete Setup Guide

**Status:** ✅ Gold Tier Complete
**Date:** March 11, 2026

---

## 🎯 What You Have Built

You've built a **Personal AI Employee** - an autonomous AI agent that manages your business 24/7!

### ✅ Working Components:

| Component | Status | What It Does |
|-----------|--------|--------------|
| **Facebook Auto-Posting** | ✅ WORKING | Automatically posts to Facebook |
| **Odoo Accounting** | ✅ RUNNING | Business accounting & invoicing |
| **Approval Workflow** | ✅ WORKING | Human-in-the-loop approvals |
| **Audit Logging** | ✅ WORKING | Logs all actions |

---

## 📁 Your System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SOURCES                              │
│  Facebook  Instagram  Gmail  WhatsApp  Odoo  Files              │
└─────────┬──────────┬──────────┬──────────┬─────────┬────────────┘
          │          │          │          │         │
          ▼          ▼          ▼          ▼         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WATCHERS (Senses)                             │
│  Monitors inputs and creates action files                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 NEEDS_ACTION FOLDER                              │
│  Action files waiting to be processed                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              ORCHESTRATOR (Brain)                                │
│  Reads files → Analyzes → Plans → Executes                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
┌─────────────────────┐   ┌─────────────────────┐
│  NEEDS APPROVAL     │   │  DIRECT EXECUTION   │
│  Pending_Approval/  │   │                     │
└──────────┬──────────┘   └──────────┬──────────┘
           │                        │
           ▼                        ▼
    ┌──────────────┐         ┌──────────────┐
    │ Human Review │         │ MCP Servers  │
    └──────┬───────┘         └──────┬───────┘
           │                        │
           ▼                        ▼
    ┌──────────────┐         ┌──────────────┐
    │ Approved/    │         │ Facebook MCP │
    │ Rejected/    │         │ Odoo MCP     │
    └──────┬───────┘         │ Email MCP    │
           │                 └──────┬───────┘
           ▼                        │
    ┌──────────────┐                │
    │ Execute      │◄───────────────┘
    └──────┬───────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DONE FOLDER                                   │
│  Completed actions with full audit trail                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 How It Works

### Step 1: Trigger Event

Something happens that needs action:
- Client emails asking for invoice
- Time for scheduled Facebook post
- New comment on Facebook
- Payment received

### Step 2: Watcher Creates Action File

A watcher script detects the event and creates a `.md` file:

```
Needs_Action/EMAIL_invoice_request.md
```

### Step 3: AI Processes the File

The Orchestrator reads the file and:
- Analyzes what needs to be done
- Creates a plan
- Takes action or requests approval

### Step 4: Human Approval (If Needed)

For sensitive actions (payments, posts):
- File moves to `Pending_Approval/`
- You review the action
- You move to `Approved/` or `Rejected/`

### Step 5: Execute Action

MCP Server executes the action:
- Posts to Facebook
- Creates invoice in Odoo
- Sends email
- Records payment

### Step 6: Log & Complete

- Action logged to `Logs/`
- File moved to `Done/`
- Audit trail created

---

## 📋 Your Folder Structure

```
AI_Employee_Vault/
├── Inbox/                  # Raw incoming items
├── Needs_Action/           # Items awaiting processing
├── Pending_Approval/       # Awaiting your approval
├── Approved/               # Approved actions (ready to execute)
├── Rejected/               # Rejected actions
├── Done/                   # Completed tasks
├── Logs/                   # Audit logs
├── Briefings/              # CEO briefings
├── Accounting/             # Financial records
└── scripts/                # All automation scripts
```

---

## 🎯 How to Use Your AI Employee

### Facebook Auto-Posting

#### Create a Post:
```bash
cd AI_Employee_Vault\scripts

python facebook_poster.py "../AI_Employee_Vault" --post "Your message here #hashtag"
```

#### Approve & Post:
```bash
# Move draft to Approved
move ..\Pending_Approval\FB_POST_*.md ..\Approved\

# Post to Facebook
python facebook_poster.py "../AI_Employee_Vault" --post-approved
```

#### View Posts:
https://www.facebook.com/1004531386081562

---

### Odoo Accounting

#### First Time Setup:
1. Open http://localhost:8069
2. Create database: `ai_employee_db`
3. Install Accounting module
4. Create `odoo_config.json`

#### Create Invoice:
```bash
python odoo/scripts/odoo_mcp_server.py "../AI_Employee_Vault" ^
  --create-invoice --partner "Client Name" --amount 1500 --description "Services"
```

#### Approve & Create in Odoo:
```bash
move ..\Pending_Approval\ODOO_INVOICE_*.md ..\Approved\
python odoo/scripts/odoo_mcp_server.py "../AI_Employee_Vault" --process-approved
```

#### Record Payment:
```bash
python odoo/scripts/odoo_mcp_server.py "../AI_Employee_Vault" ^
  --record-payment --invoice-id 123 --amount 1500
```

---

### Comment Detection (Facebook)

#### Start Comment Monitor:
```bash
python AI_Employee_Vault/scripts/facebook_comment_watcher.py "../AI_Employee_Vault"
```

This runs continuously, checking for new comments every 5 minutes.

---

### CEO Briefing

#### Generate Weekly Briefing:
```bash
python AI_Employee_Vault/scripts/ceo_briefing.py "../AI_Employee_Vault"
```

Output: `Briefings/YYYY-MM-DD_Weekly_Briefing.md`

---

## 📊 Daily Workflow Example

### Morning (9:00 AM):
```bash
# Check overnight activity
cd AI_Employee_Vault\Needs_Action
dir

# Review any pending approvals
cd ..\Pending_Approval
dir
```

### During Day:
- AI monitors Facebook comments
- AI creates post drafts
- AI creates invoice drafts
- You review and approve

### Evening (5:00 PM):
```bash
# Post approved Facebook posts
python facebook_poster.py "../AI_Employee_Vault" --post-approved

# Process approved invoices
python odoo/scripts/odoo_mcp_server.py "../AI_Employee_Vault" --process-approved
```

---

## 🔧 Maintenance Commands

### Check Facebook Status:
```bash
python AI_Employee_Vault/scripts/test_facebook_mcp.py "../AI_Employee_Vault"
```

### Check Odoo Status:
```bash
docker ps
```

### View Logs:
```bash
# Facebook logs
dir AI_Employee_Vault\Logs\facebook_*.json

# Odoo logs
docker logs odoo_community_19
```

### Restart Services:
```bash
# Restart Facebook watcher
# Just run it again

# Restart Odoo
cd odoo
docker-compose restart
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `.env` | Facebook credentials (SECRET!) |
| `facebook_config.json` | Facebook config template |
| `odoo_config.json` | Odoo credentials (create after setup) |
| `AI_Employee_Vault/scripts/` | All automation scripts |
| `AI_Employee_Vault/Logs/` | Audit logs |

---

## 🎯 Quick Start Commands

### Facebook:
```bash
# Create post
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" --post "Hello!"

# Approve (move file)
move AI_Employee_Vault\Pending_Approval\FB_POST_*.md AI_Employee_Vault\Approved\

# Post
python AI_Employee_Vault/scripts/facebook_poster.py "../AI_Employee_Vault" --post-approved
```

### Odoo:
```bash
# Create invoice
python odoo/scripts/odoo_mcp_server.py "../AI_Employee_Vault" ^
  --create-invoice --partner "Client" --amount 1000

# Process
move AI_Employee_Vault\Pending_Approval\ODOO_*.md AI_Employee_Vault\Approved\
python odoo/scripts/odoo_mcp_server.py "../AI_Employee_Vault" --process-approved
```

---

## 🎉 What's Next?

### Optional Enhancements:

1. **Scheduled Posting:**
   ```bash
   # Daily post at 9 AM
   schtasks /create /tn "Facebook_Daily" ^
     /tr "python facebook_auto_post.py" /sc daily /st 09:00
   ```

2. **Comment Monitoring:**
   ```bash
   # Run comment watcher continuously
   python facebook_comment_watcher.py "../AI_Employee_Vault"
   ```

3. **Weekly Briefings:**
   ```bash
   # Monday 7 AM briefing
   schtasks /create /tn "CEO_Briefing" ^
     /tr "python ceo_briefing.py" /sc weekly /d MON /st 07:00
   ```

4. **Instagram Integration:**
   - Connect Instagram Business account
   - Use same Facebook posting workflow

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [FACEBOOK_SIMPLE_GUIDE.md](FACEBOOK_SIMPLE_GUIDE.md) | Facebook usage |
| [ODOO_IS_RUNNING.md](ODOO_IS_RUNNING.md) | Odoo setup |
| [FINAL_STATUS_ALL_PERMISSIONS.md](FINAL_STATUS_ALL_PERMISSIONS.md) | Facebook status |
| [GOLD_TIER_README.md](GOLD_TIER_README.md) | Gold Tier overview |

---

## 🆘 Troubleshooting

### Facebook Not Posting:
1. Check token in `.env` is valid
2. Regenerate token if expired
3. Run: `python test_facebook_mcp.py`

### Odoo Not Accessible:
```bash
docker ps
docker logs odoo_community_19
cd odoo && docker-compose restart
```

### General Issues:
1. Check `AI_Employee_Vault/Logs/` for errors
2. Restart the specific service
3. Check file permissions

---

## 🎉 Congratulations!

**You now have a fully functional AI Employee that:**
- ✅ Posts to Facebook automatically
- ✅ Manages accounting in Odoo
- ✅ Requires your approval for sensitive actions
- ✅ Logs everything for audit
- ✅ Works 24/7 autonomously

**Your AI Employee is ready for business!** 🚀

---

**Questions?** Check the documentation files or run the test scripts!
