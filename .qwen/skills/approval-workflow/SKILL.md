---
name: approval-workflow
description: |
  Human-in-the-Loop approval system for sensitive AI actions.
  Files move through: Pending_Approval -> Approved -> Done or Rejected.
  Use for payments, email sending, and other high-risk actions.
---

# Human-in-the-Loop Approval Workflow

Safety system for AI Employee sensitive actions.

## Folder Structure

```
AI_Employee_Vault/
├── Pending_Approval/    # Awaiting human review
├── Approved/            # Approved - ready for execution
├── Rejected/            # Rejected - will not execute
└── Done/                # Completed actions
```

## Workflow

```
1. AI detects action needed (payment, email send, etc.)
           ↓
2. AI creates approval request in Pending_Approval/
           ↓
3. Human reviews the request
           ↓
4a. Human moves to Approved/    →  AI executes action
4b. Human moves to Rejected/    →  AI logs and skips
```

## Approval Request Format

```markdown
---
type: approval_request
action: send_email
to: client@example.com
subject: Invoice #1234
amount: 1500.00
created: 2026-02-26T10:30:00Z
expires: 2026-02-27T10:30:00Z
status: pending
priority: normal
---

# Approval Request: Send Email

## Action Details
- **Action Type**: send_email
- **Recipient**: client@example.com
- **Subject**: Invoice #1234
- **Amount**: $1,500.00

## Context
Client requested invoice for January consulting work.

## To Approve
Move this file to `/Approved` folder.

## To Reject
Move this file to `/Rejected` folder with reason.

---
*Created by AI Employee - Requires Human Approval*
```

## Approval Thresholds

Configure in `Company_Handbook.md`:

```markdown
## Payment Approval Rules

| Amount | Action |
|--------|--------|
| < $50 | Auto-approve (if recurring) |
| $50 - $500 | Require approval |
| > $500 | Require approval + manager review |

## Email Approval Rules

| Recipient | Action |
|-----------|--------|
| Known contacts | Auto-draft, no approval |
| New contacts | Require approval |
| Bulk (>5) | Require approval |
```

## Python Implementation

### Approval Manager

```python
# approval_manager.py
from pathlib import Path
from datetime import datetime
import shutil

class ApprovalManager:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path)
        self.pending = self.vault / 'Pending_Approval'
        self.approved = self.vault / 'Approved'
        self.rejected = self.vault / 'Rejected'
        self.done = self.vault / 'Done'
        
        for folder in [self.pending, self.approved, self.rejected, self.done]:
            folder.mkdir(parents=True, exist_ok=True)
    
    def create_approval_request(self, request_data: dict) -> Path:
        """Create approval request file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        action_type = request_data.get('action', 'unknown')
        filename = f"APPROVAL_{timestamp}_{action_type}.md"
        filepath = self.pending / filename
        
        content = self._format_request(request_data)
        filepath.write_text(content, encoding='utf-8')
        
        return filepath
    
    def check_approvals(self) -> list:
        """Check for approved files ready for execution."""
        approved_files = []
        for f in self.approved.iterdir():
            if f.suffix == '.md':
                approved_files.append(f)
        return approved_files
    
    def process_approved(self, approved_file: Path, executor) -> bool:
        """Process an approved file."""
        content = approved_file.read_text(encoding='utf-8')
        
        # Parse frontmatter
        data = self._parse_frontmatter(content)
        
        try:
            # Execute the approved action
            result = executor.execute(data)
            
            # Move to Done
            shutil.move(str(approved_file), str(self.done / approved_file.name))
            
            return True
        except Exception as e:
            # Log error
            print(f"Error executing approval: {e}")
            return False
    
    def _format_request(self, data: dict) -> str:
        """Format approval request as markdown."""
        return f"""---
type: approval_request
action: {data.get('action', 'unknown')}
created: {datetime.now().isoformat()}
status: pending
---

# Approval Request: {data.get('action', 'Unknown Action')}

## Details
{chr(10).join(f'- **{k.title()}**: {v}' for k, v in data.items() if k != 'action')}

## To Approve
Move this file to `/Approved` folder.

## To Reject
Move this file to `/Rejected` folder.
"""
    
    def _parse_frontmatter(self, content: str) -> dict:
        """Parse YAML frontmatter."""
        import yaml
        lines = content.split('\n')
        if lines[0].strip() != '---':
            return {}
        
        end = lines.index('---', 1)
        yaml_content = '\n'.join(lines[1:end])
        return yaml.safe_load(yaml_content)
```

## Integration with Orchestrator

```python
# In orchestrator.py
def run_cycle(self):
    # Check for new approvals
    approved = self.approval_manager.check_approvals()
    
    for approval_file in approved:
        success = self.approval_manager.process_approved(
            approval_file, 
            self.email_executor
        )
        
        if success:
            self.logger.info(f"Executed approval: {approval_file.name}")
        else:
            self.logger.error(f"Failed approval: {approval_file.name}")
```

## Notification System

Optional: Notify human when approval needed

```python
def notify_approval_needed(filepath: Path):
    """Send notification when approval is needed."""
    # Options:
    # - Desktop notification (plyer)
    # - Email notification
    # - SMS via Twilio
    # - WhatsApp message
    # - Slack message
    
    print(f"[ALERT] Approval needed: {filepath.name}")
```

## Security Rules

1. **Never auto-execute** sensitive actions
2. **Always log** approval decisions
3. **Set expiration** on approvals (24 hours default)
4. **Require re-approval** for modified actions
5. **Audit trail** of all approvals

## Best Practices

1. **Clear descriptions**: Explain what the action does
2. **Include context**: Why is this action needed?
3. **Set priorities**: Urgent vs normal approvals
4. **Regular review**: Check pending approvals daily
5. **Document rejections**: Note why an action was rejected
