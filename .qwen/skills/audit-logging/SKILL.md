---
name: audit-logging
description: |
  Comprehensive audit logging for AI Employee actions.
  Tracks all decisions, actions, and state changes for compliance and debugging.
  Use for production accountability and forensics.
---

# Audit Logging Skill

Comprehensive audit trail for AI Employee.

## Overview

Provides:
- Action logging (who, what, when, why)
- Decision tracking (AI decisions with reasoning)
- State change logging (file movements, status changes)
- Compliance reporting

## Log Structure

### logs/YYYY-MM-DD.json

```json
{
  "timestamp": "2026-03-01T10:30:00Z",
  "action_type": "email_send",
  "actor": "ai_employee",
  "target": "client@example.com",
  "parameters": {
    "subject": "Invoice #1234",
    "amount": 1500.00
  },
  "approval_status": "approved",
  "approved_by": "human_user",
  "result": "success",
  "message_id": "19ca6e34205bfcc4"
}
```

## Implementation

### audit_logger.py

```python
#!/usr/bin/env python3
"""
Audit Logger for AI Employee
"""

import json
from pathlib import Path
from datetime import datetime


class AuditLogger:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.logs_folder = self.vault / 'Logs' / 'Audit'
        self.logs_folder.mkdir(parents=True, exist_ok=True)
    
    def log_action(self, action_type: str, **kwargs):
        """Log an action."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            **kwargs
        }
        
        log_file = self.logs_folder / f'{datetime.now().strftime("%Y-%m-%d")}.json'
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def log_decision(self, decision: str, reasoning: str, **kwargs):
        """Log an AI decision."""
        self.log_action(
            'decision',
            decision=decision,
            reasoning=reasoning,
            **kwargs
        )
    
    def log_state_change(self, entity: str, from_state: str, to_state: str, **kwargs):
        """Log a state change."""
        self.log_action(
            'state_change',
            entity=entity,
            from_state=from_state,
            to_state=to_state,
            **kwargs
        )
    
    def get_audit_trail(self, start_date: str, end_date: str) -> list:
        """Get audit trail for date range."""
        trail = []
        
        for log_file in self.logs_folder.glob('*.json'):
            file_date = log_file.stem
            if start_date <= file_date <= end_date:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        trail.append(json.loads(line))
        
        return trail
```

## Integration with AI Employee

### Log All Actions

```python
# In orchestrator.py
audit = AuditLogger('../AI_Employee_Vault')

def process_file(filepath):
    audit.log_action(
        'process_file',
        file=str(filepath),
        actor='orchestrator'
    )
    # Process file...
    audit.log_state_change(
        entity=str(filepath),
        from_state='pending',
        to_state='processed'
    )
```

## Compliance Reports

### Generate Weekly Report

```bash
python audit_report.py \
  --start 2026-02-23 \
  --end 2026-03-01 \
  --format pdf
```

## Best Practices

1. **Log everything** - All actions, decisions, state changes
2. **Immutable logs** - Never modify past logs
3. **Regular backups** - Backup logs daily
4. **Retention policy** - Keep logs for 90+ days
5. **Access control** - Restrict log access
