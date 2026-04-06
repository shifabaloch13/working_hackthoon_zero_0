# 🏆 Platinum Tier - Architecture Documentation

**Status:** Building...
**Date:** March 11, 2026

---

## 🎯 Platinum Tier Overview

**Tagline:** *Always-On Cloud + Local Executive - Production-Ready AI Employee*

The Platinum Tier extends Gold Tier with:
1. **24/7 Cloud Deployment** - Always-on watchers and orchestrator
2. **Work-Zone Specialization** - Cloud drafts, Local approves
3. **Synced Vault** - Git-based synchronization
4. **Security First** - Secrets never sync
5. **Production Odoo** - Cloud VM with HTTPS and backups

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLOUD VM (Oracle/AWS/GCP)                    │
│                    24/7 Always-On                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Cloud Agent  │  │ Email Triage │  │ Social Drafts│         │
│  │ (Orchestrator│  │ (Draft only) │  │ (Draft only) │         │
│  │  + Watchers) │  │              │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │  /Needs_Action/cloud/                            │          │
│  │  /Plans/cloud/                                   │          │
│  │  /Updates/ (writes updates for Local)            │          │
│  │  /In_Progress/cloud_agent/ (claim-by-move)       │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │ Odoo 19      │  │ Health       │                            │
│  │ (HTTPS)      │  │ Monitoring   │                            │
│  └──────────────┘  └──────────────┘                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                         │
                         │ Git Sync (Vault only, NO secrets)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LOCAL MACHINE                                │
│                    (Your Laptop)                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Local Agent  │  │ Approvals    │  │ Final Send   │         │
│  │ (Orchestrator│  │ (Human-in-   │  │ (Post/Pay/  │         │
│  │  + Watchers) │  │  the-Loop)   │  │  Reply)     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │  /Needs_Action/local/                            │          │
│  │  /Pending_Approval/ (human reviews here)         │          │
│  │  /Approved/ (Local moves to approve)             │          │
│  │  /In_Progress/local_agent/ (claim-by-move)       │          │
│  │  Dashboard.md (single-writer: Local only)        │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ WhatsApp     │  │ Banking      │  │ MCP Servers  │         │
│  │ Session      │  │ Credentials  │  │ (Final Send) │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔑 Key Concepts

### 1. Work-Zone Specialization

| Zone | Owns | Does NOT Own |
|------|------|--------------|
| **Cloud** | Email triage, draft replies, social post drafts, Odoo drafts | Final send, approvals, WhatsApp, banking |
| **Local** | Approvals, WhatsApp, payments, final send/post | Draft creation, initial triage |

### 2. Claim-by-Move Rule

**Prevents double-work:**
- First agent to move item from `/Needs_Action/` to `/In_Progress/<agent>/` owns it
- Other agents must ignore items in `/In_Progress/` that aren't theirs

### 3. Security Rules

**Secrets NEVER sync:**
```
# .gitignore (synced vault)
.env
*.pem
*.key
credentials.json
facebook_config.json
odoo_config.json
whatsapp_session/
```

### 4. Vault Sync (Phase 1)

**Using Git for sync:**
- Cloud pushes updates to Git repo
- Local pulls updates
- Local merges Cloud updates into Dashboard.md

---

## 📁 Folder Structure

### Cloud VM:
```
/opt/ai-employee/
├── vault/
│   ├── Needs_Action/cloud/
│   ├── Plans/cloud/
│   ├── Updates/
│   ├── In_Progress/cloud_agent/
│   ├── Done/
│   └── Logs/
├── scripts/
│   ├── cloud_orchestrator.py
│   ├── email_watcher.py
│   ├── social_draft_poster.py
│   └── health_monitor.py
├── .env.cloud (secrets - NOT synced)
├── .git/
└── docker-compose.yml (Odoo + PostgreSQL)
```

### Local Machine:
```
~/AI_Employee_Vault/
├── Needs_Action/local/
├── Pending_Approval/
├── Approved/
├── In_Progress/local_agent/
├── Dashboard.md (Local writes)
├── Updates/ (Cloud writes, Local merges)
├── scripts/
├── .env.local (secrets - NOT synced)
├── .git/
└── whatsapp_session/
```

---

## 🔄 Sync Workflow

### Cloud → Local:
1. Cloud creates draft in `/Updates/`
2. Cloud commits and pushes to Git
3. Local pulls from Git
4. Local merges `/Updates/` into `Dashboard.md`

### Local → Cloud:
1. Local approves action
2. Local executes via MCP
3. Local logs to `/Done/`
4. Local commits and pushes
5. Cloud pulls and sees completed action

---

## 🛡️ Security Architecture

### What Syncs:
- ✅ Markdown files (.md)
- ✅ State files (.json without secrets)
- ✅ Plans, briefings, logs

### What NEVER Syncs:
- ❌ .env files
- ❌ credentials.json
- ❌ WhatsApp sessions
- ❌ Banking credentials
- ❌ Payment tokens
- ❌ API keys

---

## 🎯 Platinum Demo Flow

**Scenario:** Email arrives while Local is offline

```
1. [Cloud] Email arrives
   ↓
2. [Cloud] Email Watcher detects
   ↓
3. [Cloud] Creates draft reply in /Updates/email_draft_*.md
   ↓
4. [Cloud] Commits and pushes to Git
   ↓
5. [Local Offline] No action (email queued)
   ↓
6. [Local] Comes online, pulls from Git
   ↓
7. [Local] Sees email draft in /Updates/
   ↓
8. [Local] Reviews and moves to /Approved/
   ↓
9. [Local] Executes send via Email MCP
   ↓
10. [Local] Logs to /Done/
    ↓
11. [Local] Commits and pushes
    ↓
12. [Cloud] Pulls and sees completed
```

---

## 📋 Platinum Tier Checklist

- [ ] Cloud VM setup (Oracle Cloud Free Tier)
- [ ] Cloud orchestrator script
- [ ] Email triage watcher (Cloud)
- [ ] Social draft creator (Cloud)
- [ ] Git sync setup
- [ ] Claim-by-move rule implemented
- [ ] Security rules (.gitignore for secrets)
- [ ] Local approval workflow
- [ ] Odoo cloud deployment with HTTPS
- [ ] Health monitoring
- [ ] Platinum demo workflow
- [ ] Documentation complete

---

**Next:** Building each component...
