"""
Create Email Draft for Approval Workflow

Creates an email draft in Pending_Approval folder.
Move to Approved/ to send.
"""

import sys
from pathlib import Path
from datetime import datetime

def create_email_draft(to, subject, body):
    """Create email draft for approval"""
    
    vault_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path("../AI_Employee_Vault")
    pending_approval = vault_path / "Pending_Approval"
    pending_approval.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"EMAIL_APPROVAL_{timestamp}.md"
    filepath = pending_approval / filename
    
    content = f"""---
type: email_approval_request
to: {to}
subject: {subject}
created: {datetime.now().isoformat()}
status: pending_approval
---

# Email Approval Request

## Recipient
- **To:** {to}
- **Subject:** {subject}

## Email Body
{body}

## To Approve
Move this file to `/Approved` folder to send this email.

## To Reject
Move this file to `/Rejected` folder with reason.

---
*Created by AI Employee Email System*
"""
    
    filepath.write_text(content, encoding='utf-8')
    
    print()
    print("=" * 70)
    print("  ✅ EMAIL DRAFT CREATED!")
    print("=" * 70)
    print()
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print()
    print(f"Draft saved to: {filepath}")
    print()
    print("NEXT STEPS:")
    print("  1. Review the draft")
    print("  2. Move to Approved/ to send:")
    print(f"     move {filepath.name} ..\\Approved\\")
    print("  3. Run: python email_mcp_server.py ../../AI_Employee_Vault ../../credeintals.json")
    print()

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python create_email_draft.py <vault_path> <to> <subject> <body>")
        print()
        print("Example:")
        print('  python create_email_draft.py "../../AI_Employee_Vault" "test@example.com" "Test" "Hello!"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    to = sys.argv[2]
    subject = sys.argv[3]
    body = sys.argv[4]
    
    create_email_draft(to, subject, body)
