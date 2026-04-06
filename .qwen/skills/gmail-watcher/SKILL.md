---
name: gmail-watcher
description: |
  Monitor Gmail for new unread/important emails and create action files in Obsidian vault.
  Creates structured .md files in Needs_Action folder for AI Employee to process.
  Use for email triage, client communication tracking, and inbox management.
---

# Gmail Watcher Skill

Monitor Gmail and create action files for new emails in your AI Employee vault.

## Prerequisites

1. **Google Cloud Project** with Gmail API enabled
2. **OAuth 2.0 Credentials** (credentials.json)
3. **Python packages**: `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, `google-api-python-client`

### Install Dependencies

```bash
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Setup Google Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `credentials.json` to secure location

## Usage

### Start the Watcher

```bash
cd AI_Employee_Vault/scripts
python gmail_watcher.py "D:/path/to/AI_Employee_Vault" "D:/path/to/credentials.json"
```

### Command Line Options

```bash
python gmail_watcher.py <vault_path> <credentials_path> [--interval SECONDS] [--label LABEL]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--interval` | 120 | Check interval in seconds |
| `--label` | INBOX | Gmail label to monitor |
| `--query` | `is:unread` | Gmail search query |

## How It Works

1. **Authenticate** with Gmail API using OAuth 2.0
2. **Poll** every N seconds for new unread emails
3. **Create action file** in `Needs_Action/` folder for each new email
4. **Track processed** email IDs to avoid duplicates
5. **Log all activity** to `Logs/watcher_YYYY-MM-DD.log`

## Action File Format

Each email creates a `.md` file like:

```markdown
---
type: email
from: client@example.com
subject: Invoice Request
received: 2026-02-26T10:30:00
priority: high
status: pending
email_id: 18e4a1b2c3d4e5f6
---

# Email: Invoice Request

## Sender
client@example.com

## Received
2026-02-26 10:30:00

## Body
Hi, could you please send me the invoice for January?

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
```

## State Management

Watcher maintains state in `Logs/gmail_watcher_state.txt`:
- Stores processed email IDs
- Survives restarts without re-processing
- Clean state file to re-process all emails

## Security Notes

- **Never commit** `token.json` to version control
- Store credentials in secure location
- Use app-specific passwords if 2FA enabled
- Rotate credentials monthly

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication failed | Delete `token.json`, re-authenticate |
| No emails detected | Check Gmail query, verify API enabled |
| Rate limit errors | Increase check interval (>60s) |
| Permission denied | Grant Gmail API permissions |

## Integration with AI Employee

Once watcher creates action files:

```bash
# Run orchestrator to process emails
python orchestrator.py "D:/path/to/AI_Employee_Vault" --once

# Or run continuously
python orchestrator.py "D:/path/to/AI_Employee_Vault"
```

Qwen Code can then:
- Read emails from `Needs_Action/`
- Draft replies using Email MCP
- Create plans in `Plans/`
- Request approval for sensitive actions

## Example: Full Setup

```bash
# 1. Install dependencies
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# 2. Run watcher (first time will open browser for auth)
python gmail_watcher.py "../AI_Employee_Vault" "D:/secrets/gmail_credentials.json"

# 3. In another terminal, run orchestrator
python orchestrator.py "../AI_Employee_Vault"
```
