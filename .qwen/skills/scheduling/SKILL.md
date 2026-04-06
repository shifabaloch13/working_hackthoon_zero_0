---
name: scheduling
description: |
  Schedule automated tasks using cron (Linux/Mac) or Task Scheduler (Windows).
  Run watchers, orchestrators, and briefings at specific times.
  Use for daily briefings, weekly audits, and continuous monitoring.
---

# Scheduling Skill

Automate AI Employee tasks with system schedulers.

## Overview

| Platform | Scheduler | Use Case |
|----------|-----------|----------|
| **Windows** | Task Scheduler | Desktop automation |
| **Linux** | cron | Server/VM automation |
| **macOS** | cron or launchd | Desktop automation |

## Windows Task Scheduler

### Daily Briefing (8:00 AM)

```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "python" `
  -Argument "C:\path\to\AI_Employee_Vault\scripts\orchestrator.py C:\path\to\AI_Employee_Vault --once"
$trigger = New-ScheduledTaskTrigger -Daily -At 8:00AM
$principal = New-ScheduledTaskPrincipal -UserId "YOUR_USERNAME" -LogonType S4U -RunLevel Highest
Register-ScheduledTask -TaskName "AI_Employee_Daily_Briefing" `
  -Action $action -Trigger $trigger -Principal $principal
```

### Continuous Watcher (Startup)

```powershell
# Start watchers on user login
$action = New-ScheduledTaskAction -Execute "python" `
  -Argument "C:\path\to\AI_Employee_Vault\scripts\gmail_watcher.py C:\path\to\AI_Employee_Vault C:\path\to\credentials.json"
$trigger = New-ScheduledTaskTrigger -AtLogon
$principal = New-ScheduledTaskPrincipal -UserId "YOUR_USERNAME" -LogonType Interactive
Register-ScheduledTask -TaskName "AI_Employee_Gmail_Watcher" `
  -Action $action -Trigger $trigger -Principal $principal
```

### Weekly CEO Briefing (Monday 7:00 AM)

```powershell
# Weekly briefing
$action = New-ScheduledTaskAction -Execute "python" `
  -Argument "C:\path\to\AI_Employee_Vault\scripts\ceo_briefing.py C:\path\to\AI_Employee_Vault"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 7:00AM
$principal = New-ScheduledTaskPrincipal -UserId "YOUR_USERNAME" -LogonType S4U -RunLevel Highest
Register-ScheduledTask -TaskName "AI_Employee_Weekly_Briefing" `
  -Action $action -Trigger $trigger -Principal $principal
```

### GUI Method

1. Open **Task Scheduler** (search in Start menu)
2. Click **Create Basic Task**
3. Name: `AI Employee - Daily Briefing`
4. Trigger: `Daily` at `8:00 AM`
5. Action: `Start a program`
6. Program: `python.exe`
7. Arguments: `C:\path\to\orchestrator.py C:\path\to\AI_Employee_Vault --once`
8. Start in: `C:\path\to\AI_Employee_Vault\scripts`
9. Finish

## Linux/Unix cron

### Setup crontab

```bash
# Edit crontab
crontab -e

# Add entries
```

### Daily Briefing (8:00 AM)

```cron
0 8 * * * /usr/bin/python3 /home/user/AI_Employee_Vault/scripts/orchestrator.py /home/user/AI_Employee_Vault --once >> /var/log/ai_employee.log 2>&1
```

### Continuous Watcher (every 2 minutes)

```cron
*/2 * * * * /usr/bin/python3 /home/user/AI_Employee_Vault/scripts/gmail_watcher.py /home/user/AI_Employee_Vault /path/to/credentials.json >> /var/log/ai_employee.log 2>&1
```

### Weekly CEO Briefing (Monday 7:00 AM)

```cron
0 7 * * 1 /usr/bin/python3 /home/user/AI_Employee_Vault/scripts/ceo_briefing.py /home/user/AI_Employee_Vault >> /var/log/ai_employee.log 2>&1
```

### WhatsApp Watcher (every 30 seconds via shell loop)

```bash
# Create wrapper script: /home/user/ai_employee/whatsapp_loop.sh
#!/bin/bash
while true; do
    python3 /home/user/AI_Employee_Vault/scripts/whatsapp_watcher.py /home/user/AI_Employee_Vault --interval 30
    sleep 30
done

# Make executable
chmod +x /home/user/ai_employee/whatsapp_loop.sh

# Add to crontab (runs on boot)
@reboot /home/user/ai_employee/whatsapp_loop.sh >> /var/log/ai_employee.log 2>&1
```

## macOS launchd

### Create plist file

```xml
<!-- ~/Library/LaunchAgents/com.aiemployee.briefing.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aiemployee.briefing</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/AI_Employee_Vault/scripts/orchestrator.py</string>
        <string>/path/to/AI_Employee_Vault</string>
        <string>--once</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/ai_employee.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/ai_employee.err</string>
</dict>
</plist>
```

### Load the job

```bash
launchctl load ~/Library/LaunchAgents/com.aiemployee.briefing.plist
```

## Scheduled Task Templates

### Daily Briefing Script

```python
# daily_briefing.py
"""Generate daily briefing in Dashboard.md"""
from pathlib import Path
from datetime import datetime

def generate_daily_briefing(vault_path: str):
    vault = Path(vault_path)
    dashboard = vault / 'Dashboard.md'
    done_folder = vault / 'Done'
    
    # Count completed tasks yesterday
    yesterday = datetime.now().strftime('%Y-%m-%d')
    
    # Generate briefing
    briefing = f"""
## Daily Briefing - {yesterday}

### Completed Tasks
- Review Needs_Action folder
- Process pending items
- Update Dashboard

### Pending Items
- Check for new emails
- Review WhatsApp messages

### Notes
- Auto-generated by AI Employee
"""
    
    # Append to dashboard or create separate briefing file
    briefing_file = vault / 'Briefings' / f'{yesterday}_Daily.md'
    briefing_file.parent.mkdir(parents=True, exist_ok=True)
    briefing_file.write_text(briefing, encoding='utf-8')
    
    print(f"[OK] Daily briefing created: {briefing_file}")

if __name__ == '__main__':
    import sys
    generate_daily_briefing(sys.argv[1] if len(sys.argv) > 1 else '.')
```

### Weekly CEO Briefing Script

```python
# ceo_briefing.py
"""Generate weekly CEO briefing with revenue and bottlenecks"""
from pathlib import Path
from datetime import datetime, timedelta

def generate_ceo_briefing(vault_path: str):
    vault = Path(vault_path)
    business_goals = vault / 'Business_Goals.md'
    briefing_file = vault / 'Briefings' / f'CEO_Briefing_{datetime.now().strftime("%Y-%m-%d")}.md'
    
    # Read business goals
    goals_content = business_goals.read_text(encoding='utf-8') if business_goals.exists() else ''
    
    # Generate briefing
    briefing = f"""---
generated: {datetime.now().isoformat()}
period: Weekly CEO Briefing
---

# CEO Briefing - {datetime.now().strftime('%B %d, %Y')}

## Executive Summary
*Auto-generated weekly briefing*

## Revenue This Week
- Review bank transactions in Accounting/
- Total: $X,XXX (update manually or via integration)

## Completed Tasks
- Check Done/ folder for completed items
- Key milestones achieved

## Bottlenecks
- Tasks that took longer than expected
- Items requiring attention

## Upcoming Deadlines
- Review Business_Goals.md for project deadlines

## Proactive Suggestions
- AI-generated recommendations

---
*Generated by AI Employee v0.2 (Silver Tier)*
"""
    
    briefing_file.parent.mkdir(parents=True, exist_ok=True)
    briefing_file.write_text(briefing, encoding='utf-8')
    
    print(f"[OK] CEO briefing created: {briefing_file}")

if __name__ == '__main__':
    import sys
    generate_ceo_briefing(sys.argv[1] if len(sys.argv) > 1 else '.')
```

## Verification

### Check Scheduled Tasks (Windows)

```powershell
# List all tasks
Get-ScheduledTask | Where-Object {$_.TaskName -like "*AI_Employee*"}

# View task details
Get-ScheduledTask -TaskName "AI_Employee_Daily_Briefing" | Get-ScheduledTaskInfo
```

### Check cron Jobs (Linux/Mac)

```bash
# List all cron jobs
crontab -l

# Check cron logs
grep CRON /var/log/syslog
```

## Best Practices

1. **Log everything**: Redirect output to log files
2. **Error handling**: Use try/catch in scheduled scripts
3. **Notifications**: Send alerts on failures
4. **Testing**: Test manually before scheduling
5. **Documentation**: Document all scheduled tasks

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Task doesn't run | Check user permissions, run level |
| Python not found | Use full path to python.exe |
| Script fails | Check working directory |
| No output | Verify log file permissions |
