---
name: ceo-briefing
description: |
  Generate weekly CEO Briefings with business audit, revenue tracking, and proactive suggestions.
  Analyzes transactions, tasks, and goals to create executive summaries.
  Use for weekly business reviews and strategic planning.
---

# CEO Briefing Skill

Automated weekly business audit and CEO briefing generation.

## Overview

The CEO Briefing skill autonomously audits your business data and generates comprehensive weekly reports including:
- Revenue tracking
- Completed tasks analysis
- Bottleneck identification
- Proactive suggestions
- Upcoming deadlines

## Prerequisites

1. **Python 3.10+**
2. **Obsidian Vault** with Business_Goals.md
3. **Accounting data** in Accounting/ folder
4. **Task history** in Done/ folder

## Usage

### Generate Weekly Briefing

```bash
cd AI_Employee_Vault/scripts
python ceo_briefing.py "../AI_Employee_Vault"
```

### Schedule Weekly (Windows Task Scheduler)

```powershell
$action = New-ScheduledTaskAction -Execute "python" `
  -Argument "ceo_briefing.py ../AI_Employee_Vault"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 7:00AM
Register-ScheduledTask -TaskName "AI_Employee_CEO_Briefing" `
  -Action $action -Trigger $trigger
```

## Briefing Structure

### Generated Output: Briefings/YYYY-MM-DD_Weekly_Briefing.md

```markdown
---
generated: 2026-03-01T07:00:00Z
period: 2026-02-23 to 2026-03-01
type: weekly_ceo_briefing
---

# CEO Weekly Briefing

## Executive Summary
[Brief overview of the week]

## Revenue
- **This Week**: $X,XXX
- **MTD**: $XX,XXX (XX% of monthly target)
- **Trend**: [On track/Ahead/Behind]

## Completed Tasks
- [List of completed tasks from Done/ folder]

## Bottlenecks
| Task | Expected | Actual | Delay |
|------|----------|--------|-------|
| ... | ... | ... | ... |

## Proactive Suggestions

### Cost Optimization
- [Suggestions based on spending patterns]

### Revenue Opportunities
- [Identified opportunities]

### Process Improvements
- [Efficiency recommendations]

## Upcoming Deadlines
- [List of upcoming deadlines from Business_Goals.md]

## Key Metrics
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| ... | ... | ... | ... |
```

## Implementation

### ceo_briefing.py

```python
#!/usr/bin/env python3
"""
CEO Briefing Generator

Generates weekly business audit and CEO briefing.
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
        bottlenecks = self._identify_bottlenecks(week_start, today)
        suggestions = self._generate_suggestions(revenue, completed_tasks)
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
        # Implementation to parse accounting data
        return {
            'this_week': 0,
            'mtd': 0,
            'monthly_target': 10000,
            'trend': 'on_track'
        }
    
    def _get_completed_tasks(self, start: datetime, end: datetime) -> list:
        """Get completed tasks from Done/ folder."""
        tasks = []
        # Implementation to parse Done/ folder
        return tasks
    
    def _identify_bottlenecks(self, start: datetime, end: datetime) -> list:
        """Identify bottlenecks and delays."""
        bottlenecks = []
        # Implementation to analyze task completion times
        return bottlenecks
    
    def _generate_suggestions(self, revenue: dict, tasks: list) -> dict:
        """Generate proactive suggestions."""
        return {
            'cost_optimization': [],
            'revenue_opportunities': [],
            'process_improvements': []
        }
    
    def _get_upcoming_deadlines(self) -> list:
        """Get upcoming deadlines from Business_Goals.md."""
        deadlines = []
        # Implementation to parse Business_Goals.md
        return deadlines
    
    def _format_briefing(self, start, end, revenue, tasks, bottlenecks, 
                         suggestions, deadlines) -> str:
        """Format briefing as Markdown."""
        return f"""---
generated: {datetime.now().isoformat()}
period: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}
type: weekly_ceo_briefing
---

# CEO Weekly Briefing

## Executive Summary
[Auto-generated summary]

## Revenue
- **This Week**: ${revenue['this_week']:,.2f}
- **MTD**: ${revenue['mtd']:,.2f} ({revenue['mtd']/revenue['monthly_target']*100:.1f}% of target)
- **Trend**: {revenue['trend'].replace('_', ' ').title()}

## Completed Tasks
{len(tasks)} tasks completed this week

## Bottlenecks
{len(bottlenecks)} bottlenecks identified

## Proactive Suggestions
See detailed suggestions in full briefing

## Upcoming Deadlines
{len(deadlines)} upcoming deadlines

---
*Generated by AI Employee CEO Briefing System*
"""


def main():
    if len(sys.argv) < 2:
        print('Usage: python ceo_briefing.py <vault_path>')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    generator = CEOBriefingGenerator(vault_path)
    briefing_file = generator.generate_briefing()
    
    print()
    print('=' * 70)
    print('  CEO BRIEFING GENERATED')
    print('=' * 70)
    print()
    print(f'[OK] Briefing saved to: {briefing_file}')
    print()


if __name__ == '__main__':
    main()
```

## Integration with AI Employee

### Automatic Weekly Generation

The CEO Briefing integrates with the scheduling system:

```python
# In orchestrator.py or scheduled task
def generate_weekly_briefing():
    from ceo_briefing import CEOBriefingGenerator
    
    generator = CEOBriefingGenerator('../AI_Employee_Vault')
    briefing = generator.generate_briefing()
    
    # Create action item to review briefing
    create_review_task(briefing)
```

### Qwen Code Integration

Qwen Code can analyze the briefing and create action items:

```bash
qwen "Read the latest CEO Briefing and create action items for identified bottlenecks"
```

## Example Output

See `AI_Employee_Vault/Briefings/YYYY-MM-DD_Weekly_Briefing.md` for generated briefings.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No revenue data | Ensure accounting data exists in Accounting/ folder |
| No tasks found | Check that completed tasks are in Done/ folder |
| Missing deadlines | Update Business_Goals.md with project deadlines |

## Best Practices

1. **Review briefings weekly** - Every Monday morning
2. **Act on suggestions** - Implement at least one suggestion per week
3. **Track metrics** - Update Business_Goals.md with actual vs target
4. **Share with team** - Distribute briefing to stakeholders
