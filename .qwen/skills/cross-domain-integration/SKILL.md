---
name: cross-domain-integration
description: |
  Full cross-domain integration for Personal and Business domains.
  Separates personal affairs from business operations with domain-specific handling.
  Use for comprehensive life and business management.
---

# Cross-Domain Integration Skill

Personal + Business domain separation and integration.

## Overview

Integrates multiple life domains:
- **Personal**: Gmail, WhatsApp, Personal Bank
- **Business**: LinkedIn, Twitter, Business Bank, Odoo
- **Health**: Fitness tracking, Medical appointments
- **Learning**: Courses, Certifications

## Domain Configuration

### domains.json

```json
{
  "personal": {
    "email": "personal@gmail.com",
    "phone": "+1234567890",
    "bank": "personal_bank_account",
    "priority_keywords": ["urgent", "asap", "family"]
  },
  "business": {
    "email": "business@company.com",
    "phone": "+0987654321",
    "bank": "business_bank_account",
    "priority_keywords": ["invoice", "client", "payment"]
  }
}
```

## Implementation

### Domain Router

```python
#!/usr/bin/env python3
"""
Domain Router - Routes actions to appropriate domain handler
"""

from pathlib import Path


class DomainRouter:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.domains = {
            'personal': self.vault / 'Domains' / 'Personal',
            'business': self.vault / 'Domains' / 'Business'
        }
    
    def route_action(self, action_file: Path) -> str:
        """Route action file to appropriate domain."""
        content = action_file.read_text(encoding='utf-8')
        
        # Check for business keywords
        business_keywords = ['invoice', 'client', 'payment', 'business']
        for keyword in business_keywords:
            if keyword.lower() in content.lower():
                return 'business'
        
        # Default to personal
        return 'personal'
    
    def process(self, action_file: Path):
        """Process action file with domain-specific handling."""
        domain = self.route_action(action_file)
        
        if domain == 'business':
            self._process_business(action_file)
        else:
            self._process_personal(action_file)
    
    def _process_business(self, action_file: Path):
        """Process business domain action."""
        # Business-specific handling
        pass
    
    def _process_personal(self, action_file: Path):
        """Process personal domain action."""
        # Personal-specific handling
        pass
```

## Integration with AI Employee

### Multi-Domain Dashboard

```markdown
# AI Employee Dashboard

## Personal Domain
- Emails: 3 unread
- Messages: 5 unread
- Tasks: 2 pending

## Business Domain
- Emails: 10 unread
- Leads: 3 new
- Invoices: 2 pending
- Revenue MTD: $4,500
```

## Best Practices

1. **Separate credentials** for each domain
2. **Domain-specific rules** in Company_Handbook.md
3. **Clear boundaries** between personal and business
4. **Unified dashboard** for overview
