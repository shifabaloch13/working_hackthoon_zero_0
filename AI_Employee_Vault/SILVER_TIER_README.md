# AI Employee - Silver Tier Skills

Complete skill set for Silver Tier AI Employee implementation.

## Silver Tier Deliverables

| Requirement | Skill | Status |
|-------------|-------|--------|
| Two or more Watcher scripts | Gmail + WhatsApp + File System | ✅ |
| Automatically Post on LinkedIn | LinkedIn Posting Skill | ✅ |
| Claude/Qwen reasoning loop | Qwen Reasoning Loop | ✅ |
| One working MCP server | Email MCP Server | ✅ |
| Human-in-the-loop approval | Approval Workflow | ✅ |
| Basic scheduling | Scheduling Skill | ✅ |

## Installed Skills

### 1. Gmail Watcher
**Location:** `.qwen/skills/gmail-watcher/`

Monitor Gmail for new emails and create action files.

```bash
python gmail_watcher.py "D:/AI_Employee_Vault" "D:/credentials.json"
```

**Features:**
- OAuth 2.0 authentication
- Unread email detection
- Action file creation in Needs_Action/
- State management (no duplicates)

---

### 2. WhatsApp Watcher
**Location:** `.qwen/skills/whatsapp-watcher/`

Monitor WhatsApp Web for keyword-based messages.

```bash
python whatsapp_watcher.py "D:/AI_Employee_Vault" --keywords "urgent,asap,invoice,payment"
```

**Features:**
- Playwright-based automation
- Keyword detection
- Session persistence
- Action file creation

---

### 3. Email MCP Server
**Location:** `.qwen/skills/email-mcp-server/`

MCP server for sending, drafting, and searching emails.

**Configuration:**
```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  }
}
```

**Tools:**
- `send_email` - Send emails
- `draft_email` - Create drafts
- `search_emails` - Search Gmail
- `mark_read` - Mark as read
- `reply_to_email` - Reply to threads

---

### 4. Approval Workflow
**Location:** `.qwen/skills/approval-workflow/`

Human-in-the-Loop approval system.

**Folder Flow:**
```
Pending_Approval → Approved → Done
                → Rejected
```

**Approval Request Format:**
```markdown
---
type: approval_request
action: send_email
to: client@example.com
created: 2026-02-26T10:30:00Z
status: pending
---
```

---

### 5. LinkedIn Posting
**Location:** `.qwen/skills/linkedin-posting/`

Automate LinkedIn posts for business marketing.

```bash
python linkedin_poster.py "D:/AI_Employee_Vault" --execute-approved
```

**Features:**
- Playwright automation
- Approval required before posting
- Image upload support
- Content drafting

---

### 6. Scheduling
**Location:** `.qwen/skills/scheduling/`

Schedule tasks with cron or Task Scheduler.

**Windows Task Scheduler:**
```powershell
$action = New-ScheduledTaskAction -Execute "python" `
  -Argument "orchestrator.py ../AI_Employee_Vault --once"
$trigger = New-ScheduledTaskTrigger -Daily -At 8:00AM
Register-ScheduledTask -TaskName "AI_Employee_Daily_Briefing" `
  -Action $action -Trigger $trigger
```

**Linux cron:**
```cron
0 8 * * * python3 /path/to/orchestrator.py /path/to/vault --once
```

---

### 7. Qwen Reasoning Loop
**Location:** `.qwen/skills/qwen-reasoning-loop/`

AI reasoning and planning system.

**Plan.md Format:**
```markdown
---
created: 2026-02-26T10:30:00Z
status: pending
action_type: email
---

# Action Plan

## Objective
Process client invoice request.

## Steps
- [ ] Read email
- [ ] Generate invoice
- [ ] Request approval
- [ ] Send after approval
```

---

## Complete System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL SOURCES                         │
│     Gmail        WhatsApp        LinkedIn        Files      │
└────────┬──────────┬────────────────┬──────────────┬─────────┘
         │          │                │              │
         ▼          ▼                ▼              ▼
┌─────────────────────────────────────────────────────────────┐
│                    WATCHERS (Senses)                        │
│  Gmail Watcher   WhatsApp Watcher   File System Watcher     │
└─────────┬──────────┬────────────────┬───────────────────────┘
          │          │                │
          ▼          ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                 NEEDS_ACTION FOLDER                         │
│  EMAIL_*.md    WHATSAPP_*.md    FILE_*.md                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              QWEN REASONING LOOP (Brain)                    │
│  Read → Analyze → Plan → Create Plan.md → Request Approval  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    PLANS FOLDER                             │
│  PLAN_*.md (with checkboxes and decisions)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              APPROVAL WORKFLOW (Safety)                     │
│  Pending_Approval → Approved → Execute → Done               │
│                   → Rejected → Log                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 MCP SERVERS (Hands)                         │
│   Email MCP    LinkedIn MCP    Browser MCP                  │
└─────────┬──────────┬────────────────┬───────────────────────┘
          │          │                │
          ▼          ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                  EXTERNAL ACTIONS                           │
│   Send Email   Post to LinkedIn   Web Automation            │
└─────────────────────────────────────────────────────────────┘
                         ▲
                         │
┌────────────────────────┴────────────────────────────────────┐
│                  SCHEDULING (Timing)                        │
│   Task Scheduler (Win)   cron (Linux)   launchd (Mac)       │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start Guide

### 1. Setup Watchers

```bash
# Gmail Watcher
cd AI_Employee_Vault/scripts
python gmail_watcher.py "../AI_Employee_Vault" "D:/secrets/gmail_credentials.json"

# WhatsApp Watcher (in new terminal)
python whatsapp_watcher.py "../AI_Employee_Vault" --keywords "urgent,asap,invoice,payment"

# File System Watcher (in new terminal)
python filesystem_watcher.py "../AI_Employee_Vault"
```

### 2. Run Orchestrator

```bash
# Process all action files
python orchestrator.py "../AI_Employee_Vault"
```

### 3. Configure Qwen Code

Add MCP servers to Qwen Code configuration:

```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  }
}
```

### 4. Set Up Scheduling

**Windows:**
```powershell
# Daily briefing at 8 AM
$action = New-ScheduledTaskAction -Execute "python" `
  -Argument "orchestrator.py ../AI_Employee_Vault --once"
$trigger = New-ScheduledTaskTrigger -Daily -At 8:00AM
Register-ScheduledTask -TaskName "AI_Employee_Daily_Briefing" `
  -Action $action -Trigger $trigger
```

### 5. Test Approval Workflow

```bash
# Create test approval request
echo "---
type: approval_request
action: test
status: pending
---
Test approval" > Pending_Approval/TEST_001.md

# Move to Approved to test
mv Pending_Approval/TEST_001.md Approved/

# Run orchestrator to process
python orchestrator.py "../AI_Employee_Vault" --once
```

---

## Skill Dependencies

```
Bronze Tier (Required)
├── File System Watcher
├── Dashboard.md
├── Company_Handbook.md
└── Basic Orchestrator

Silver Tier (Add-ons)
├── Gmail Watcher → Requires: Google Cloud credentials
├── WhatsApp Watcher → Requires: Playwright, WhatsApp Web
├── Email MCP Server → Requires: Node.js, Gmail API
├── Approval Workflow → Requires: Folder structure
├── LinkedIn Posting → Requires: Playwright, LinkedIn account
├── Scheduling → Requires: OS scheduler access
└── Qwen Reasoning Loop → Requires: Qwen Code
```

---

## Testing Checklist

- [ ] Gmail Watcher detects new emails
- [ ] WhatsApp Watcher detects keyword messages
- [ ] Action files created in Needs_Action/
- [ ] Orchestrator creates Plan.md files
- [ ] Approval workflow moves files correctly
- [ ] Email MCP sends approved emails
- [ ] LinkedIn posts after approval
- [ ] Scheduled tasks run at correct times
- [ ] Dashboard.md updates with activity
- [ ] Logs capture all actions

---

## Upgrade Path to Gold Tier

To upgrade from Silver to Gold:

1. **Add Odoo Integration** - Accounting MCP server
2. **Add Social Media** - Facebook/Instagram MCP
3. **Add Twitter/X** - Twitter API integration
4. **Add CEO Briefing** - Weekly automated reports
5. **Add Ralph Wiggum Loop** - Persistent reasoning
6. **Add Error Recovery** - Graceful degradation

---

## Resources

- **Hackathon Document:** `Personal AI Employee Hackathon 0_...md`
- **Bronze Tier:** `AI_Employee_Vault/README.md`
- **Qwen Code Docs:** https://claude.com/product/claude-code
- **Playwright Docs:** https://playwright.dev
- **Gmail API:** https://developers.google.com/gmail/api

---

*AI Employee v0.2 (Silver Tier) - Powered by Qwen Code*
