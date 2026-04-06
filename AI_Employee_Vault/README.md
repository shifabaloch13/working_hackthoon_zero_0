# AI Employee - Bronze Tier

A Personal AI Employee implementation using Qwen Code and Obsidian. This is the **Bronze Tier** (Foundation) implementation of the Personal AI Employee Hackathon.

## 🏆 Bronze Tier Deliverables (Complete)

- [x] Obsidian vault with Dashboard.md and Company_Handbook.md
- [x] One working Watcher script (File System monitoring)
- [x] Claude Code successfully reading from and writing to the vault
- [x] Basic folder structure: /Inbox, /Needs_Action, /Done
- [x] Orchestrator for processing action files

## 📁 Project Structure

```
AI_Employee_Vault/
├── Dashboard.md              # Main dashboard with real-time stats
├── Company_Handbook.md       # Rules of Engagement
├── Business_Goals.md         # Objectives and metrics
├── Drop/                     # Drop files here for processing
├── Inbox/                    # Raw incoming items
├── Needs_Action/             # Items awaiting processing
├── Done/                     # Completed tasks
├── Pending_Approval/         # Awaiting human approval
├── Approved/                 # Approved actions (triggers execution)
├── Plans/                    # Multi-step task plans
├── Briefings/                # CEO briefings
├── Accounting/               # Financial records
├── Logs/                     # System logs
└── scripts/
    ├── base_watcher.py       # Base class for all watchers
    ├── filesystem_watcher.py # File system watcher implementation
    └── orchestrator.py       # Main orchestrator
```

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.10 or higher
- **Obsidian**: v1.10.6+ (free)
- **Qwen Code**: Active subscription (optional for advanced features)

### Setup

1. **Open the vault in Obsidian:**
   - Open Obsidian
   - Click "Open folder as vault"
   - Select the `AI_Employee_Vault` folder

2. **Run the File System Watcher:**
   ```bash
   cd AI_Employee_Vault/scripts
   python filesystem_watcher.py ../
   ```

3. **Run the Orchestrator (in a separate terminal):**
   ```bash
   cd AI_Employee_Vault/scripts
   python orchestrator.py ../ --once
   ```

### Usage

1. **Drop a file** into the `Drop/` folder
2. The **FileSystemWatcher** detects it and creates an action file in `Needs_Action/`
3. The **Orchestrator** processes the action file and creates a plan in `Plans/`
4. Review the **Dashboard.md** for activity updates

## 📋 Scripts

### FileSystemWatcher

Monitors the `Drop/` folder for new files and creates action files.

```bash
# Basic usage
python filesystem_watcher.py /path/to/vault

# With custom check interval (default: 30 seconds)
python filesystem_watcher.py /path/to/vault --interval 60
```

**Features:**
- Tracks processed files by MD5 hash (no duplicates)
- Creates detailed action files with metadata
- Logs all activity to `Logs/` folder

### Orchestrator

Processes files in `Needs_Action/` and coordinates workflow.

```bash
# Run once and exit
python orchestrator.py /path/to/vault --once

# Run continuously (checks every 60 seconds)
python orchestrator.py /path/to/vault

# Custom interval
python orchestrator.py /path/to/vault --interval 30
```

**Features:**
- Creates Plan.md files for each action
- Updates Dashboard.md with recent activity
- Logs all actions in JSON format

## 🔧 Configuration

### Company Handbook

Edit `Company_Handbook.md` to customize:
- Communication rules
- Payment thresholds
- Task priority assignment
- Security rules

### Business Goals

Edit `Business_Goals.md` to set:
- Revenue targets
- Key metrics
- Active projects
- Subscription tracking

## 📊 Testing

The system has been tested with:
- ✅ File drop detection
- ✅ Action file creation
- ✅ Plan generation
- ✅ Dashboard updates
- ✅ Logging to JSON files

### Test It Yourself

1. Drop any file into `AI_Employee_Vault/Drop/`
2. Wait 30 seconds (or check immediately)
3. Look in `Needs_Action/` for the created action file
4. Run the orchestrator to process it

## 🔄 Workflow Example

```
1. User drops invoice.pdf into Drop/
2. FileSystemWatcher detects the file
3. Creates FILE_20260226_invoice.pdf.md in Needs_Action/
4. Orchestrator reads the action file
5. Creates PLAN_20260226_invoice.pdf.md in Plans/
6. Updates Dashboard.md with activity
7. Logs action to Logs/YYYY-MM-DD.json
```

## 📝 Next Steps (Silver Tier)

To upgrade to Silver Tier, add:
- [ ] Gmail Watcher (monitor emails)
- [ ] WhatsApp Watcher (monitor messages)
- [ ] MCP Server for external actions (send emails)
- [ ] Human-in-the-loop approval workflow
- [ ] Scheduled tasks via cron/Task Scheduler

## 🛠️ Troubleshooting

### Watcher doesn't detect files

- Check if the Drop folder exists
- Verify file permissions
- Check logs in `Logs/watcher_YYYY-MM-DD.log`

### Orchestrator doesn't process files

- Ensure files are in `Needs_Action/` folder
- Check file extension is `.md`
- Review logs in `Logs/` folder

### Python errors

- Verify Python version: `python --version`
- Ensure you're in the `scripts/` directory
- Check file paths are correct

## 📚 Resources

- [Hackathon Document](../Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Obsidian Help](https://help.obsidian.md/)
- [Qwen Code Docs](https://claude.com/product/claude-code)

## 🤝 Contributing

This is a hackathon project. Feel free to:
- Add new watcher types
- Improve the orchestrator
- Create MCP servers for external integrations
- Enhance the Dashboard templates

## 📄 License

This project is part of the Personal AI Employee Hackathon 0.

---

*Built with ❤️ for the Personal AI Employee Hackathon 0*
