# Platinum Tier Demo Workflow

**Email Arrives While Local is Offline → Cloud Drafts → Local Approves → Local Sends**

---

## 🎯 Demo Scenario

This demo shows the Platinum Tier's key feature: **Cloud/Local separation with async processing**.

**Scenario:**
1. Email arrives while Local machine is offline
2. Cloud Agent detects and drafts reply
3. Cloud syncs to Git
4. Local comes online, pulls from Git
5. Human reviews and approves draft
6. Local sends email via MCP
7. Action logged and synced back to Cloud

---

## 📋 Step-by-Step Demo

### Phase 1: Setup

#### 1.1 Cloud VM is Running
```bash
# On Cloud VM
ssh opc@<cloud-ip>

# Check services
sudo systemctl status ai-employee-cloud
docker ps
```

**Expected:** Cloud orchestrator is running

#### 1.2 Local Machine is Offline (Simulated)
```bash
# On Local machine
# Turn off WiFi or disconnect network
```

---

### Phase 2: Email Arrives

#### 2.1 Gmail Watcher Detects Email (Cloud)

**On Cloud VM:**
```bash
# Simulate email arrival
cat > /opt/ai-employee/vault/Needs_Action/cloud/EMAIL_demo_123.md << 'EOF'
---
type: email
from: client@example.com
subject: Invoice Request
received: 2026-03-11T12:00:00Z
priority: high
status: pending
---

# Email Content

Hi,

Can you please send me the invoice for January services?

Thanks,
Client A
EOF
```

#### 2.2 Cloud Orchestrator Processes

**Cloud logs:**
```
[INFO] Processing: EMAIL_demo_123.md
[INFO] Claimed: EMAIL_demo_123.md
[INFO] Created update: UPDATE_EMAIL_REPLY_20260311_120000.md
[INFO] Git sync successful
```

**On Cloud:**
```bash
# Check Updates folder
ls -la /opt/ai-employee/vault/Updates/

# Should see:
# UPDATE_EMAIL_REPLY_*.md
```

---

### Phase 3: Local Comes Online

#### 3.1 Local Machine Connects

```bash
# Turn on WiFi
# Wait for network connection
```

#### 3.2 Local Agent Syncs from Cloud

**On Local machine:**
```bash
cd ~/AI_Employee_Vault

# Pull from Git
python scripts/vault_sync.py --mode local --action pull

# Merge updates
python scripts/vault_sync.py --mode local --action merge
```

**Local logs:**
```
[local] Pulling from Git...
[local] Pull successful
[local] Merged 1 updates from Cloud
```

#### 3.3 Human Reviews Draft

**On Local machine:**
```bash
# Check Pending_Approval folder
ls Pending_Approval/

# Read the draft
cat Pending_Approval/UPDATE_EMAIL_REPLY_*.md
```

**Draft content:**
```markdown
---
type: email_reply_draft
original: EMAIL_demo_123.md
created: 2026-03-11T12:00:00Z
status: pending_approval
---

# Email Reply Draft

## Original Email
From: client@example.com
Subject: Invoice Request

Can you please send me the invoice for January services?

## Suggested Reply
Dear Client A,

Thank you for your inquiry. Please find attached the invoice for January services.

Total: $1,500.00
Due: Net 30

Best regards,
AI Employee Team

## To Send
Move this file to /Approved folder to send.
```

---

### Phase 4: Human Approves

#### 4.1 Move to Approved

**On Local machine:**
```bash
# Approve the draft
mv Pending_Approval/UPDATE_EMAIL_REPLY_*.md Approved/
```

#### 4.2 Local Agent Detects Approval

**Local logs:**
```
[INFO] Found 1 approved items
[INFO] Executing email send: UPDATE_EMAIL_REPLY_*.md
[INFO] Would send email (MCP integration)
[INFO] Moved to Done: UPDATE_EMAIL_REPLY_*.md
```

---

### Phase 5: Execute and Sync

#### 5.1 Local Executes Send

**On Local machine:**
```bash
# Check Done folder
ls Done/

# Check logs
cat Logs/local_2026-03-11.json
```

**Log entry:**
```json
{
  "timestamp": "2026-03-11T12:05:00",
  "action": "email_send",
  "file": "UPDATE_EMAIL_REPLY_*.md",
  "result": "success",
  "agent": "local_agent"
}
```

#### 5.2 Local Syncs to Cloud

**On Local machine:**
```bash
# Push to Git
python scripts/vault_sync.py --mode local --action push
```

**Local logs:**
```
[local] Pushing to Git...
[local] Push successful
```

#### 5.3 Cloud Pulls Updates

**On Cloud VM:**
```bash
# Pull from Git
cd /opt/ai-employee
git pull origin main
```

**Cloud logs:**
```
[INFO] Git sync successful
[INFO] Pulled completed action from Local
```

---

## ✅ Demo Complete!

### What We Demonstrated:

1. ✅ **Cloud detects** email while Local offline
2. ✅ **Cloud drafts** reply (draft-only, no send)
3. ✅ **Cloud syncs** draft to Git
4. ✅ **Local pulls** when online
5. ✅ **Human reviews** and approves
6. ✅ **Local sends** via MCP (has credentials)
7. ✅ **Local syncs** completed action back to Cloud

---

## 🎯 Key Platinum Features Shown:

| Feature | Demonstrated |
|---------|--------------|
| **Work-Zone Separation** | ✅ Cloud drafts, Local sends |
| **Async Processing** | ✅ Works while Local offline |
| **Git Sync** | ✅ Cloud ↔ Local sync |
| **Claim-by-Move** | ✅ No double-work |
| **Security** | ✅ Credentials stay Local |
| **Audit Trail** | ✅ Full logging |

---

## 📊 Demo Timeline

```
T+0:00  Email arrives (Cloud detects)
T+0:01  Cloud creates draft
T+0:02  Cloud syncs to Git
T+0:03  Local offline (no action)
T+0:10  Local comes online
T+0:11  Local pulls from Git
T+0:12  Human reviews draft
T+0:13  Human approves (moves to Approved/)
T+0:14  Local sends email
T+0:15  Local syncs to Cloud
T+0:16  Cloud pulls completed action
```

**Total Time:** ~16 minutes (including offline period)

---

## 🔧 Commands Reference

### Cloud VM:
```bash
# Check status
sudo systemctl status ai-employee-cloud

# View logs
tail -f /var/log/ai_employee_cloud.log

# Check vault
ls /opt/ai-employee/vault/Needs_Action/cloud/
ls /opt/ai-employee/vault/Updates/

# Sync manually
cd /opt/ai-employee && git pull && git push
```

### Local Machine:
```bash
# Sync from Cloud
python scripts/vault_sync.py --mode local --action pull

# Merge updates
python scripts/vault_sync.py --mode local --action merge

# Check approvals
ls Pending_Approval/

# Approve
mv Pending_Approval/*.md Approved/

# Sync to Cloud
python scripts/vault_sync.py --mode local --action push
```

---

**Platinum Tier Demo Complete!** 🏆
