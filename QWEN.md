# Personal AI Employee (Digital FTE) Project

## Project Overview

This is a **hackathon project** for building a "Personal AI Employee" or "Digital FTE" (Full-Time Equivalent) - an autonomous AI agent that manages personal and business affairs 24/7. The project uses **Claude Code** as the reasoning engine and **Obsidian** (local Markdown) as the dashboard/memory system.

**Tagline:** *Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

### Core Architecture

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Brain** | Claude Code | Reasoning engine, task planning, execution |
| **Memory/GUI** | Obsidian Vault | Dashboard, long-term memory, state management |
| **Senses** | Python Watchers | Monitor Gmail, WhatsApp, filesystems for triggers |
| **Hands** | MCP Servers | External actions (email, browser automation, payments) |

### Key Concepts

- **Watchers:** Lightweight Python scripts that monitor inputs and create `.md` files in `/Needs_Action` folder
- **Ralph Wiggum Loop:** A Stop hook pattern that keeps Claude iterating until tasks are complete
- **Human-in-the-Loop:** Sensitive actions require approval via file movement (`/Pending_Approval` → `/Approved`)
- **CEO Briefing:** Autonomous weekly business audit with revenue, bottlenecks, and proactive suggestions

## Directory Structure

```
D:\Download\working_hackthoon_zero_0\
├── Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md  # Main hackathon guide
├── skills-lock.json          # Skill versioning/locking configuration
├── .gitattributes            # Git text file settings
├── .qwen/
│   └── skills/
│       └── browsing-with-playwright/  # Browser automation skill
│           ├── SKILL.md              # Playwright MCP usage documentation
│           ├── references/
│           │   └── playwright-tools.md
│           └── scripts/
│               ├── mcp-client.py     # MCP client for browser automation
│               ├── start-server.sh   # Start Playwright MCP server
│               ├── stop-server.sh    # Stop Playwright MCP server
│               └── verify.py         # Server verification script
```

## Key Files

| File | Purpose |
|------|---------|
| `Personal AI Employee Hackathon 0_...md` | Comprehensive hackathon blueprint with architecture, templates, and tiered deliverables (Bronze/Silver/Gold/Platinum) |
| `.qwen/skills/browsing-with-playwright/SKILL.md` | Browser automation documentation using Playwright MCP |
| `skills-lock.json` | Tracks installed skills and their versions |

## Hackathon Tiers

| Tier | Time | Deliverables |
|------|------|--------------|
| **Bronze** | 8-12 hours | Obsidian vault, 1 Watcher script, basic Claude integration |
| **Silver** | 20-30 hours | Multiple Watchers, MCP server, approval workflow, scheduling |
| **Gold** | 40+ hours | Full integration, Odoo accounting, social media, Ralph Wiggum loop |
| **Platinum** | 60+ hours | Cloud deployment, domain specialization, A2A upgrade |

## Building and Running

### Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| [Claude Code](https://claude.com/product/claude-code) | Active subscription | Primary reasoning engine |
| [Obsidian](https://obsidian.md/download) | v1.10.6+ | Knowledge base & dashboard |
| [Python](https://www.python.org/downloads/) | 3.13+ | Watcher scripts & orchestration |
| [Node.js](https://nodejs.org/) | v24+ LTS | MCP servers & automation |
| [GitHub Desktop](https://desktop.github.com/download/) | Latest | Version control |

### Setup Steps

1. **Create Obsidian Vault:**
   ```bash
   mkdir AI_Employee_Vault
   cd AI_Employee_Vault
   mkdir Inbox Needs_Action Done Pending_Approval Approved Plans Briefings
   ```

2. **Verify Claude Code:**
   ```bash
   claude --version
   ```

3. **Start Playwright MCP Server (for browser automation):**
   ```bash
   # Windows (convert .sh to .bat or run via Git Bash)
   bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh
   
   # Or manually
   npx @playwright/mcp@latest --port 8808 --shared-browser-context
   ```

4. **Verify Server:**
   ```bash
   python .qwen/skills/browsing-with-playwright/scripts/verify.py
   ```

5. **Stop Server (when done):**
   ```bash
   bash .qwen/skills/browsing-with-playwright/scripts/stop-server.sh
   ```

### Watcher Script Pattern

All Watchers follow this base structure:

```python
from pathlib import Path
from abc import ABC, abstractmethod
import time

class BaseWatcher(ABC):
    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process"""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder"""
        pass

    def run(self):
        while True:
            items = self.check_for_updates()
            for item in items:
                self.create_action_file(item)
            time.sleep(self.check_interval)
```

### MCP Server Configuration

Configure in `~/.config/claude-code/mcp.json`:

```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json"
      }
    },
    {
      "name": "browser",
      "command": "npx",
      "args": ["@anthropic/browser-mcp"],
      "env": {
        "HEADLESS": "true"
      }
    }
  ]
}
```

## Development Conventions

### File Naming

- **Action Files:** `TYPE_Description_Date.md` (e.g., `EMAIL_ClientMeeting_2026-01-07.md`)
- **Approval Files:** `APPROVAL_Action_Recipient_Date.md`
- **Briefings:** `YYYY-MM-DD_Day_Briefing.md`

### Folder Structure (Obsidian Vault)

```
Vault/
├── Inbox/              # Raw incoming items
├── Needs_Action/       # Items awaiting processing
├── In_Progress/<agent>/ # Items being worked on (claim-by-move rule)
├── Pending_Approval/   # Awaiting human approval
├── Approved/           # Approved actions (triggers execution)
├── Rejected/           # Rejected actions
├── Done/               # Completed tasks
├── Plans/              # Multi-step task plans
├── Briefings/          # CEO briefings
├── Accounting/         # Financial records
└── Business_Goals.md   # Objectives and metrics
```

### Human-in-the-Loop Pattern

For sensitive actions, Claude writes an approval request:

```markdown
---
type: approval_request
action: payment
amount: 500.00
recipient: Client A
created: 2026-01-07T10:30:00Z
status: pending
---

## Payment Details
- Amount: $500.00
- To: Client A
- Reference: Invoice #1234

## To Approve
Move this file to /Approved folder.
```

### Ralph Wiggum Loop (Persistence)

Keep Claude working until task completion:

```bash
# Start a Ralph loop
/ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

## Testing Practices

1. **Verify MCP servers** before each session: `verify.py`
2. **Test Watchers** with sample data before deployment
3. **Log all actions** in audit files
4. **Use staging vault** for testing new features

## Resources

- **Hackathon Documentation:** `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Playwright Tools Reference:** `.qwen/skills/browsing-with-playwright/references/playwright-tools.md`
- **Ralph Wiggum Pattern:** https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum
- **Agent Skills:** https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

## Community

- **Research Meetings:** Wednesdays at 10:00 PM PKT on Zoom
- **First Meeting:** January 7th, 2026
- **YouTube:** https://www.youtube.com/@panaversity
