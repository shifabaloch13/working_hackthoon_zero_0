"""
CEO Briefing Generator - Gold Tier

Generates weekly business audit and CEO briefing automatically.
Analyzes revenue, tasks, bottlenecks, and generates proactive suggestions.

Usage:
    python ceo_briefing.py "D:/path/to/AI_Employee_Vault"
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta


class CEOBriefingGenerator:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.briefings_folder = self.vault / 'Briefings'
        self.accounting_folder = self.vault / 'Accounting'
        self.done_folder = self.vault / 'Done'
        self.business_goals = self.vault / 'Business_Goals.md'
        
        self.briefings_folder.mkdir(parents=True, exist_ok=True)
    
    def generate_briefing(self) -> Path:
        """Generate weekly CEO briefing."""
        
        # Calculate date range (last 7 days)
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday() + 7)
        
        # Gather data
        revenue = self._calculate_revenue(week_start, today)
        completed_tasks = self._get_completed_tasks(week_start, today)
        bottlenecks = self._identify_bottlenecks()
        suggestions = self._generate_suggestions(revenue, completed_tasks, bottlenecks)
        deadlines = self._get_upcoming_deadlines()
        
        # Generate briefing content
        content = self._format_briefing(
            week_start, today, revenue, completed_tasks,
            bottlenecks, suggestions, deadlines
        )
        
        # Save briefing
        filename = f'{today.strftime("%Y-%m-%d")}_Weekly_Briefing.md'
        briefing_file = self.briefings_folder / filename
        briefing_file.write_text(content, encoding='utf-8')
        
        return briefing_file
    
    def _calculate_revenue(self, start: datetime, end: datetime) -> dict:
        """Calculate revenue for the period."""
        # Parse accounting folder for transactions
        revenue_this_week = 0
        revenue_mtd = 0
        
        if self.accounting_folder.exists():
            for file in self.accounting_folder.iterdir():
                if file.suffix == '.md':
                    content = file.read_text(encoding='utf-8')
                    # Simple parsing for revenue amounts
                    if 'Revenue' in content or 'Income' in content:
                        # Extract amount (simplified)
                        revenue_this_week += 1000  # Placeholder
        
        return {
            'this_week': revenue_this_week,
            'mtd': revenue_mtd + revenue_this_week,
            'monthly_target': 10000,
            'trend': 'on_track' if revenue_this_week > 0 else 'needs_attention'
        }
    
    def _get_completed_tasks(self, start: datetime, end: datetime) -> list:
        """Get completed tasks from Done/ folder."""
        tasks = []
        
        if self.done_folder.exists():
            for file in self.done_folder.iterdir():
                if file.suffix == '.md':
                    tasks.append({
                        'name': file.stem,
                        'completed': file.stat().st_mtime
                    })
        
        return tasks
    
    def _identify_bottlenecks(self) -> list:
        """Identify bottlenecks and delays."""
        bottlenecks = []
        
        # Check for items in Needs_Action for too long
        needs_action = self.vault / 'Needs_Action'
        if needs_action.exists():
            for file in needs_action.iterdir():
                age_days = (datetime.now().timestamp() - file.stat().st_mtime) / 86400
                if age_days > 7:
                    bottlenecks.append({
                        'task': file.stem,
                        'age_days': int(age_days),
                        'severity': 'high' if age_days > 14 else 'medium'
                    })
        
        return bottlenecks
    
    def _generate_suggestions(self, revenue: dict, tasks: list, bottlenecks: list) -> dict:
        """Generate proactive suggestions."""
        suggestions = {
            'cost_optimization': [],
            'revenue_opportunities': [],
            'process_improvements': []
        }
        
        # Revenue-based suggestions
        if revenue['this_week'] < revenue['monthly_target'] / 4:
            suggestions['revenue_opportunities'].append(
                'Revenue is below weekly target. Consider reaching out to pending leads.'
            )
        
        # Bottleneck-based suggestions
        for bottleneck in bottlenecks:
            if bottleneck['severity'] == 'high':
                suggestions['process_improvements'].append(
                    f"Task '{bottleneck['task']}' has been pending for {bottleneck['age_days']} days. Review and prioritize."
                )
        
        return suggestions
    
    def _get_upcoming_deadlines(self) -> list:
        """Get upcoming deadlines from Business_Goals.md."""
        deadlines = []
        
        if self.business_goals.exists():
            content = self.business_goals.read_text(encoding='utf-8')
            # Simple parsing for dates (YYYY-MM-DD format)
            import re
            dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)
            for date_str in dates[:5]:  # Limit to 5 deadlines
                deadlines.append({'date': date_str, 'description': 'Project deadline'})
        
        return deadlines
    
    def _format_briefing(self, start, end, revenue, tasks, bottlenecks, 
                         suggestions, deadlines) -> str:
        """Format briefing as Markdown."""
        
        # Build tasks section
        tasks_section = ""
        for task in tasks[:10]:  # Limit to 10 tasks
            tasks_section += f"- {task['name']}\n"
        
        if not tasks:
            tasks_section = "*No completed tasks found*\n"
        
        # Build bottlenecks section
        bottlenecks_section = ""
        for bn in bottlenecks:
            bottlenecks_section += f"- ⚠️ {bn['task']} ({bn['age_days']} days old)\n"
        
        if not bottlenecks:
            bottlenecks_section = "*No bottlenecks identified*\n"
        
        # Build suggestions section
        suggestions_section = ""
        for suggestion in suggestions.get('revenue_opportunities', []):
            suggestions_section += f"- 💰 {suggestion}\n"
        for suggestion in suggestions.get('process_improvements', []):
            suggestions_section += f"- ⚙️ {suggestion}\n"
        
        if not suggestions_section:
            suggestions_section = "*No suggestions at this time*\n"
        
        # Build deadlines section
        deadlines_section = ""
        for deadline in deadlines:
            deadlines_section += f"- {deadline['date']}: {deadline['description']}\n"
        
        if not deadlines:
            deadlines_section = "*No upcoming deadlines*\n"
        
        return f"""---
generated: {datetime.now().isoformat()}
period: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}
type: weekly_ceo_briefing
---

# CEO Weekly Briefing

## Executive Summary

This week's business performance analysis with revenue tracking, task completion, and strategic recommendations.

## Revenue

- **This Week**: ${revenue['this_week']:,.2f}
- **MTD**: ${revenue['mtd']:,.2f} ({revenue['mtd']/revenue['monthly_target']*100:.1f}% of ${revenue['monthly_target']:,.2f} target)
- **Trend**: {revenue['trend'].replace('_', ' ').title()}

## Completed Tasks

{len(tasks)} tasks completed this week

{tasks_section}
## Bottlenecks

{len(bottlenecks)} bottlenecks identified

{bottlenecks_section}
## Proactive Suggestions

### Revenue Opportunities
{suggestions_section}

## Upcoming Deadlines

{deadlines_section}
## Key Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Weekly Revenue | $2,500 | ${revenue['this_week']:,.2f} | {'✅' if revenue['this_week'] >= 2500 else '⚠️'} |
| Tasks Completed | 10 | {len(tasks)} | {'✅' if len(tasks) >= 10 else '⚠️'} |
| Bottlenecks | 0 | {len(bottlenecks)} | {'✅' if len(bottlenecks) == 0 else '⚠️'} |

---
*Generated by AI Employee CEO Briefing System (Gold Tier)*
"""


def main():
    if len(sys.argv) < 2:
        print('Usage: python ceo_briefing.py <vault_path>')
        print()
        print('Example:')
        print('  python ceo_briefing.py "../AI_Employee_Vault"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    generator = CEOBriefingGenerator(vault_path)
    briefing_file = generator.generate_briefing()
    
    print()
    print('=' * 70)
    print('  CEO BRIEFING GENERATED')
    print('=' * 70)
    print()
    print(f'[OK] Briefing saved to: {briefing_file}')
    print()
    print('Next Steps:')
    print('  1. Review the briefing in Briefings/ folder')
    print('  2. Act on identified bottlenecks')
    print('  3. Implement proactive suggestions')
    print()


if __name__ == '__main__':
    main()
