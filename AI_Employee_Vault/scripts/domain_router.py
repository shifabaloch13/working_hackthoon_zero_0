"""
Cross-Domain Router - Gold Tier

Routes actions to appropriate domain handlers (Personal vs Business).
Based on hackathon documentation requirements for cross-domain integration.

Usage:
    python domain_router.py "D:/path/to/AI_Employee_Vault" --file action_file.md
"""

import sys
import json
from pathlib import Path
from datetime import datetime


# Domain configuration
DOMAIN_CONFIG = {
    'personal': {
        'email': 'balckcat699@gmail.com',
        'keywords': ['family', 'personal', 'friend', 'urgent', 'asap'],
        'folders': ['Personal'],
        'priority': 'high'
    },
    'business': {
        'email': 'business@company.com',
        'keywords': ['invoice', 'client', 'payment', 'business', 'project', 'meeting'],
        'folders': ['Business'],
        'priority': 'high'
    }
}


class DomainRouter:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.domains_folder = self.vault / 'Domains'
        self.needs_action = self.vault / 'Needs_Action'
        
        # Create domain folders
        for domain in DOMAIN_CONFIG:
            (self.domains_folder / domain).mkdir(parents=True, exist_ok=True)
    
    def route_action(self, action_file: Path) -> str:
        """Route action file to appropriate domain."""
        content = action_file.read_text(encoding='utf-8')
        
        # Score for each domain
        personal_score = 0
        business_score = 0
        
        # Check for business keywords
        for keyword in DOMAIN_CONFIG['business']['keywords']:
            if keyword.lower() in content.lower():
                business_score += 1
        
        # Check for personal keywords
        for keyword in DOMAIN_CONFIG['personal']['keywords']:
            if keyword.lower() in content.lower():
                personal_score += 1
        
        # Determine domain
        if business_score > personal_score:
            return 'business'
        elif personal_score > business_score:
            return 'personal'
        else:
            # Default to personal if tie
            return 'personal'
    
    def process(self, action_file: Path) -> dict:
        """Process action file with domain-specific handling."""
        domain = self.route_action(action_file)
        
        result = {
            'file': action_file.name,
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'status': 'routed'
        }
        
        if domain == 'business':
            self._process_business(action_file, result)
        else:
            self._process_personal(action_file, result)
        
        return result
    
    def _process_business(self, action_file: Path, result: dict):
        """Process business domain action."""
        # Move to business domain folder
        dest = self.domains_folder / 'business' / action_file.name
        action_file.rename(dest)
        
        result['destination'] = str(dest)
        result['status'] = 'routed_to_business'
        
        print(f'[BUSINESS] Routed {action_file.name} to business domain')
    
    def _process_personal(self, action_file: Path, result: dict):
        """Process personal domain action."""
        # Move to personal domain folder
        dest = self.domains_folder / 'personal' / action_file.name
        action_file.rename(dest)
        
        result['destination'] = str(dest)
        result['status'] = 'routed_to_personal'
        
        print(f'[PERSONAL] Routed {action_file.name} to personal domain')
    
    def get_domain_stats(self) -> dict:
        """Get statistics for each domain."""
        stats = {
            'personal': {
                'files': 0,
                'folders': []
            },
            'business': {
                'files': 0,
                'folders': []
            }
        }
        
        for domain in ['personal', 'business']:
            domain_folder = self.domains_folder / domain
            if domain_folder.exists():
                stats[domain]['files'] = len(list(domain_folder.iterdir()))
                stats[domain]['folders'] = [f.name for f in domain_folder.iterdir() if f.is_dir()]
        
        return stats


class MultiDomainDashboard:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.router = DomainRouter(vault_path)
        self.dashboard = self.vault / 'Dashboard.md'
    
    def update_dashboard(self):
        """Update dashboard with multi-domain stats."""
        stats = self.router.get_domain_stats()
        
        content = f"""---
last_updated: {datetime.now().isoformat()}
status: active
---

# 🎯 AI Employee Dashboard - Multi-Domain

## 📊 Quick Stats

| Domain | Files | Status |
|--------|-------|--------|
| Personal | {stats['personal']['files']} | ✅ Active |
| Business | {stats['business']['files']} | ✅ Active |

---

## 👤 Personal Domain

- **Files**: {stats['personal']['files']}
- **Folders**: {', '.join(stats['personal']['folders']) if stats['personal']['folders'] else 'None'}

### Recent Activity
*Personal domain activity logged here*

---

## 💼 Business Domain

- **Files**: {stats['business']['files']}
- **Folders**: {', '.join(stats['business']['folders']) if stats['business']['folders'] else 'None'}

### Recent Activity
*Business domain activity logged here*

---

## 🔔 Alerts

- ⚠️ **Domain Routing**: All actions are automatically routed to appropriate domains

---

## 📁 Quick Links

- [[Company_Handbook]] - Rules of Engagement
- [[Business_Goals]] - Objectives and Metrics
- [Personal Domain](file://./Domains/personal)
- [Business Domain](file://./Domains/business)
- [Needs_Action](file://./Needs_Action) - Items awaiting routing
- [Done](file://./Done) - Completed tasks

---
*Generated by AI Employee Multi-Domain Dashboard (Gold Tier)*
"""
        
        self.dashboard.write_text(content, encoding='utf-8')
        print(f'[DASHBOARD] Dashboard updated with multi-domain stats')


def main():
    if len(sys.argv) < 2:
        print('Usage: python domain_router.py <vault_path> [--file <action_file>]')
        sys.exit(1)
    
    vault_path = Path(sys.argv[1]).resolve()
    
    if not vault_path.exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    router = DomainRouter(str(vault_path))
    
    if '--file' in sys.argv:
        # Process specific file
        file_idx = sys.argv.index('--file') + 1
        if file_idx < len(sys.argv):
            action_file = Path(sys.argv[file_idx])
            if action_file.exists():
                result = router.process(action_file)
                print(f'[OK] Routed: {json.dumps(result, indent=2)}')
            else:
                print(f'[ERROR] File not found: {action_file}')
        else:
            print('[ERROR] No file specified after --file')
    else:
        # Show stats and update dashboard
        stats = router.get_domain_stats()
        print()
        print('=' * 70)
        print('  DOMAIN ROUTER - Statistics')
        print('=' * 70)
        print()
        print(f'Personal Domain: {stats["personal"]["files"]} files')
        print(f'Business Domain: {stats["business"]["files"]} files')
        print()
        
        # Update dashboard
        dashboard = MultiDomainDashboard(str(vault_path))
        dashboard.update_dashboard()


if __name__ == '__main__':
    main()
