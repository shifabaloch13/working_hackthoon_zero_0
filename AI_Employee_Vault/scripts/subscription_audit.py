"""
Subscription Audit Logic - Gold Tier

Analyzes bank transactions to identify subscription services and flag unused ones.
Based on the hackathon documentation subscription audit requirements.

Usage:
    python subscription_audit.py "D:/path/to/AI_Employee_Vault"
"""

import sys
import re
from pathlib import Path
from datetime import datetime, timedelta


# Subscription patterns from hackathon documentation
SUBSCRIPTION_PATTERNS = {
    'netflix.com': 'Netflix',
    'spotify.com': 'Spotify',
    'adobe.com': 'Adobe Creative Cloud',
    'notion.so': 'Notion',
    'slack.com': 'Slack',
    'github.com': 'GitHub',
    'amazon.com/aws': 'AWS',
    'azure.microsoft.com': 'Microsoft Azure',
    'cloud.google.com': 'Google Cloud',
    'zoom.us': 'Zoom',
    'dropbox.com': 'Dropbox',
    'icloud.com': 'iCloud',
    'youtube.com': 'YouTube Premium',
    'hulu.com': 'Hulu',
    'disneyplus.com': 'Disney+',
    'office.com': 'Microsoft 365',
    'jetbrains.com': 'JetBrains',
    'figma.com': 'Figma',
    'canva.com': 'Canva',
}


class SubscriptionAuditor:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.accounting_folder = self.vault / 'Accounting'
        self.briefings_folder = self.vault / 'Briefings'
        self.pending_approval = self.vault / 'Pending_Approval'
        
        for folder in [self.accounting_folder, self.briefings_folder, self.pending_approval]:
            folder.mkdir(parents=True, exist_ok=True)
    
    def analyze_transactions(self) -> list:
        """Analyze transactions to identify subscriptions."""
        subscriptions = []
        
        # Look for transaction files
        if self.accounting_folder.exists():
            for file in self.accounting_folder.iterdir():
                if file.suffix == '.md':
                    content = file.read_text(encoding='utf-8')
                    found_subs = self._find_subscriptions(content, file.name)
                    subscriptions.extend(found_subs)
        
        return subscriptions
    
    def _find_subscriptions(self, content: str, filename: str) -> list:
        """Find subscription payments in transaction content."""
        subscriptions = []
        
        for pattern, name in SUBSCRIPTION_PATTERNS.items():
            if pattern.lower() in content.lower():
                # Extract amount using regex
                amount_match = re.search(r'\$?(\d+(?:\.\d{2})?)', content)
                amount = float(amount_match.group(1)) if amount_match else 0.0
                
                # Extract date from filename or content
                date_match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
                date_str = date_match.group(0) if date_match else datetime.now().strftime('%Y-%m-%d')
                
                subscriptions.append({
                    'name': name,
                    'pattern': pattern,
                    'amount': amount,
                    'date': date_str,
                    'source': filename
                })
        
        return subscriptions
    
    def check_usage(self, subscriptions: list, days_threshold: int = 30) -> list:
        """Check for subscriptions with no recent usage."""
        unused = []
        
        for sub in subscriptions:
            sub_date = datetime.strptime(sub['date'], '%Y-%m-%d')
            days_since = (datetime.now() - sub_date).days
            
            if days_since > days_threshold:
                unused.append({
                    **sub,
                    'days_inactive': days_since,
                    'recommendation': 'cancel' if days_since > 60 else 'review'
                })
        
        return unused
    
    def generate_audit_report(self) -> Path:
        """Generate subscription audit report."""
        subscriptions = self.analyze_transactions()
        unused = self.check_usage(subscriptions)
        
        # Calculate totals
        total_monthly = sum(sub['amount'] for sub in subscriptions)
        potential_savings = sum(sub['amount'] for sub in unused if sub['recommendation'] == 'cancel')
        
        # Generate report
        report_date = datetime.now().strftime('%Y-%m-%d')
        report_file = self.briefings_folder / f'Subscription_Audit_{report_date}.md'
        
        content = self._format_report(subscriptions, unused, total_monthly, potential_savings)
        report_file.write_text(content, encoding='utf-8')
        
        # Create approval request for cancellations
        if unused:
            self._create_cancellation_requests(unused)
        
        return report_file
    
    def _format_report(self, subscriptions: list, unused: list, 
                       total_monthly: float, potential_savings: float) -> str:
        """Format audit report as Markdown."""
        
        # Active subscriptions table
        active_table = "| Service | Amount | Last Charged | Source |\n"
        active_table += "|---------|--------|--------------|--------|\n"
        
        for sub in subscriptions:
            active_table += f"| {sub['name']} | ${sub['amount']:.2f} | {sub['date']} | {sub['source']} |\n"
        
        # Unused subscriptions
        unused_section = ""
        if unused:
            unused_section = "## ⚠️ Potentially Unused Subscriptions\n\n"
            for sub in unused:
                action = "Cancel" if sub['recommendation'] == 'cancel' else "Review"
                unused_section += f"- **{sub['name']}** (${sub['amount']:.2f}/month) - {sub['days_inactive']} days inactive - [{action}]\n"
        else:
            unused_section = "## ✅ All Subscriptions Active\n\nNo unused subscriptions detected.\n"
        
        return f"""---
generated: {datetime.now().isoformat()}
type: subscription_audit
total_subscriptions: {len(subscriptions)}
unused_count: {len(unused)}
---

# Subscription Audit Report

## Summary

- **Total Subscriptions Found**: {len(subscriptions)}
- **Monthly Cost**: ${total_monthly:.2f}
- **Potentially Unused**: {len(unused)}
- **Potential Monthly Savings**: ${potential_savings:.2f}

## Active Subscriptions

{active_table}
{unused_section}
## Recommendations

1. Review subscriptions marked for cancellation
2. Check if team members are still using the service
3. Look for duplicate functionality across services
4. Consider annual plans for frequently used services

---
*Generated by AI Employee Subscription Auditor (Gold Tier)*
"""
    
    def _create_cancellation_requests(self, unused: list):
        """Create approval requests for subscription cancellations."""
        for sub in unused:
            if sub['recommendation'] == 'cancel':
                request_file = self.pending_approval / f"CANCEL_{sub['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md"
                
                content = f"""---
type: cancellation_request
service: {sub['name']}
monthly_cost: {sub['amount']:.2f}
days_inactive: {sub['days_inactive']}
created: {datetime.now().isoformat()}
status: pending
---

# Subscription Cancellation Request

## Details

- **Service**: {sub['name']}
- **Monthly Cost**: ${sub['amount']:.2f}
- **Days Since Last Use**: {sub['days_inactive']}
- **Annual Cost**: ${sub['amount'] * 12:.2f}

## Reason

This subscription hasn't been used in {sub['days_inactive']} days.

## To Approve

Move this file to `/Approved` folder to proceed with cancellation.

## To Reject

Move this file to `/Rejected` folder with reason.

---
*Created by AI Employee Subscription Auditor*
"""
                request_file.write_text(content, encoding='utf-8')


def main():
    if len(sys.argv) < 2:
        print('Usage: python subscription_audit.py <vault_path>')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    auditor = SubscriptionAuditor(vault_path)
    report_file = auditor.generate_audit_report()
    
    print()
    print('=' * 70)
    print('  SUBSCRIPTION AUDIT COMPLETE')
    print('=' * 70)
    print()
    print(f'[OK] Audit report saved to: {report_file}')
    print()
    print('Next Steps:')
    print('  1. Review the audit report in Briefings/')
    print('  2. Check Pending_Approval/ for cancellation requests')
    print('  3. Approve cancellations to save money')
    print()


if __name__ == '__main__':
    main()
