---
name: whatsapp-watcher
description: |
  Monitor WhatsApp Web for new messages containing keywords (urgent, invoice, payment, etc.).
  Uses Playwright for browser automation. Creates action files in Obsidian vault.
  Use for lead capture, urgent message detection, and client communication tracking.
---

# WhatsApp Watcher Skill

Monitor WhatsApp Web for messages containing specific keywords and create action files.

## Prerequisites

1. **Python 3.10+**
2. **Playwright**: `pip install playwright`
3. **Playwright browsers**: `playwright install`
4. **WhatsApp Web account** (phone with WhatsApp)

## Installation

```bash
# Install Playwright
pip install playwright

# Install browser (Chromium)
playwright install chromium
```

## Usage

### Start the Watcher

```bash
cd AI_Employee_Vault/scripts
python whatsapp_watcher.py "D:/path/to/AI_Employee_Vault"
```

### Command Line Options

```bash
python whatsapp_watcher.py <vault_path> [OPTIONS]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--interval` | 30 | Check interval in seconds |
| `--keywords` | urgent,asap,invoice,payment,help | Comma-separated keywords |
| `--headless` | false | Run browser in headless mode |

## How It Works

1. **Launch Chromium** with persistent context (saves session)
2. **Navigate to WhatsApp Web** (web.whatsapp.com)
3. **Scan QR code** (first time only, then session persists)
4. **Monitor chat list** for unread messages
5. **Filter by keywords** (configurable)
6. **Create action file** in `Needs_Action/` folder

## Action File Format

Each matching message creates a `.md` file:

```markdown
---
type: whatsapp
from: +1234567890
chat: John Doe
received: 2026-02-26T10:30:00
keywords: invoice,payment
status: pending
---

# WhatsApp Message

## From
John Doe (+1234567890)

## Received
2026-02-26 10:30:00

## Message
Hi, could you please send me the invoice for January?

## Keywords Detected
- invoice
- payment

## Suggested Actions
- [ ] Reply to sender
- [ ] Send requested invoice
- [ ] Mark as read in WhatsApp
```

## Keyword Detection

Default keywords (configurable):
- `urgent` - Time-sensitive messages
- `asap` - Immediate attention needed
- `invoice` - Billing requests
- `payment` - Payment-related
- `help` - Support requests

Add custom keywords:
```bash
python whatsapp_watcher.py "../AI_Employee_Vault" --keywords "urgent,asap,invoice,payment,help,pricing,quote"
```

## Session Management

- **First run**: Browser opens, scan QR code with WhatsApp mobile app
- **Session saved**: In `AI_Employee_Vault/whatsapp_session/`
- **Subsequent runs**: Auto-login with saved session
- **Session expires**: Re-scan QR code when prompted

## Security Notes

- **Never share** session files (contains auth tokens)
- **Keep session folder** secure and private
- **Log out** from WhatsApp Web when not in use
- **Monitor regularly** for unauthorized access

## Troubleshooting

| Issue | Solution |
|-------|----------|
| QR code not showing | Clear session folder, restart watcher |
| No messages detected | Check keyword spelling, verify unread messages |
| Browser crashes | Reduce check interval, update Playwright |
| Session expired | Re-scan QR code when prompted |
| Rate limit errors | Increase check interval (>30s) |

## Integration with AI Employee

Once watcher creates action files:

```bash
# Run orchestrator to process messages
python orchestrator.py "D:/path/to/AI_Employee_Vault" --once
```

Qwen Code can then:
- Read messages from `Needs_Action/`
- Draft replies
- Create plans in `Plans/`
- Request approval for sensitive actions

## Example: Full Setup

```bash
# 1. Install Playwright
pip install playwright
playwright install chromium

# 2. Run watcher (first time: scan QR code)
python whatsapp_watcher.py "../AI_Employee_Vault" --keywords "urgent,asap,invoice,payment"

# 3. In another terminal, run orchestrator
python orchestrator.py "../AI_Employee_Vault"
```

## Best Practices

1. **Run in background**: Use PM2 or Task Scheduler for continuous monitoring
2. **Set appropriate interval**: 30-60 seconds balances responsiveness and resource usage
3. **Monitor keywords carefully**: Too many false positives reduce effectiveness
4. **Review session regularly**: Ensure no unauthorized access
