---
name: qwen-reasoning-loop
description: |
  Qwen Code reasoning loop that creates Plan.md files and processes action items.
  Implements the cognitive layer of AI Employee with file-based state management.
  Use for multi-step task planning, decision making, and workflow orchestration.
---

# Qwen Code Reasoning Loop

AI reasoning and planning system for AI Employee.

## Overview

The reasoning loop is the "brain" of the AI Employee:

```
Input (Action Files) → Reasoning (Qwen Code) → Output (Plans + Actions)
```

## Plan.md Format

```markdown
---
created: 2026-02-26T10:30:00Z
status: pending
action_type: email
source_file: EMAIL_20260226_client_request.md
priority: high
---

# Action Plan: Client Invoice Request

## Objective
Process client request for invoice and send billing document.

## Context
- Client: Acme Corporation
- Request: Invoice for January services
- Amount: $1,500.00
- Due Date: March 15, 2026

## Steps

- [x] Read email from client
- [x] Identify client in database
- [ ] Generate invoice PDF
- [ ] Create email draft with attachment
- [ ] Request human approval (Payment > $1000)
- [ ] Send email after approval
- [ ] Log transaction
- [ ] Move to Done folder

## Decisions Made

1. **Invoice amount**: $1,500 (standard rate)
2. **Payment terms**: Net 30
3. **Approval required**: Yes (amount > $1000)

## Notes

*Add notes during execution*

---
*Created by Qwen Code AI Employee*
```

## Reasoning Process

### Step 1: Read Action Files

```python
def read_action_files(needs_action_folder: Path) -> list:
    """Read all action files from Needs_Action folder."""
    action_files = []
    
    for f in needs_action_folder.iterdir():
        if f.suffix == '.md':
            content = f.read_text(encoding='utf-8')
            data = parse_frontmatter(content)
            action_files.append({
                'file': f,
                'type': data.get('type', 'unknown'),
                'content': content,
                'data': data
            })
    
    return action_files
```

### Step 2: Analyze and Plan

```python
def analyze_and_plan(action_file: dict, company_handbook: str) -> dict:
    """Analyze action file and create plan."""
    
    # Extract key information
    action_type = action_file['type']
    content = action_file['content']
    
    # Apply company rules
    rules = parse_handbook(company_handbook)
    
    # Determine required actions
    steps = []
    approvals_needed = []
    
    if action_type == 'email':
        steps = [
            'Read email content',
            'Identify sender and intent',
            'Determine response type',
            'Draft response',
            'Check approval requirements',
            'Execute or request approval'
        ]
        
        # Check if approval needed
        if requires_approval(action_file, rules):
            approvals_needed.append('human_review')
    
    return {
        'steps': steps,
        'approvals': approvals_needed,
        'priority': determine_priority(action_file, rules)
    }
```

### Step 3: Create Plan File

```python
def create_plan_file(action_file: dict, plan_data: dict, plans_folder: Path) -> Path:
    """Create Plan.md file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"PLAN_{timestamp}_{action_file['file'].stem}.md"
    filepath = plans_folder / filename
    
    content = format_plan_markdown(action_file, plan_data)
    filepath.write_text(content, encoding='utf-8')
    
    return filepath
```

## Integration with Orchestrator

```python
# orchestrator.py
class Orchestrator:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path)
        self.needs_action = self.vault / 'Needs_Action'
        self.plans = self.vault / 'Plans'
        self.handbook = self.vault / 'Company_Handbook.md'
    
    def run_reasoning_loop(self):
        """Run Qwen Code reasoning loop."""
        # Read action files
        action_files = self.read_action_files()
        
        # Read company handbook
        handbook_content = self.handbook.read_text(encoding='utf-8') if self.handbook.exists() else ''
        
        # Process each action file
        for action_file in action_files:
            # Analyze and create plan
            plan_data = self.analyze_and_plan(action_file, handbook_content)
            plan_file = self.create_plan_file(action_file, plan_data)
            
            # Check if approval needed
            if plan_data['approvals']:
                self.create_approval_request(action_file, plan_data)
            
            # Update dashboard
            self.update_dashboard(action_file, plan_file)
```

## Qwen Code Prompt Template

```markdown
# AI Employee Reasoning Task

## Context
You are an AI Employee assistant. Process action files from the Needs_Action folder
and create plans for execution.

## Input
- Action files in: /Needs_Action/
- Company rules: /Company_Handbook.md
- Business goals: /Business_Goals.md

## Task
For each action file:
1. Read and understand the content
2. Identify the type of action needed
3. Check Company_Handbook.md for rules
4. Create a Plan.md with steps
5. Flag items requiring human approval

## Output Format
Create Plan.md files in /Plans/ folder with:
- Objective
- Context
- Steps (checkbox format)
- Decisions made
- Approval requirements

## Rules
- Payments > $500 require approval
- Emails to new contacts require approval
- Never auto-execute sensitive actions
- Log all decisions

## Files to Process
{action_files_list}
```

## State Management

```python
class ReasoningState:
    def __init__(self, vault_path: str):
        self.state_file = Path(vault_path) / 'Logs' / 'reasoning_state.json'
        self.state = self.load()
    
    def load(self) -> dict:
        """Load state from file."""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text(encoding='utf-8'))
        return {'processed_files': [], 'pending_plans': []}
    
    def save(self):
        """Save state to file."""
        self.state_file.write_text(json.dumps(self.state, indent=2), encoding='utf-8')
    
    def mark_processed(self, file_path: str):
        """Mark a file as processed."""
        if file_path not in self.state['processed_files']:
            self.state['processed_files'].append(file_path)
            self.save()
    
    def is_processed(self, file_path: str) -> bool:
        """Check if file was already processed."""
        return file_path in self.state['processed_files']
```

## Error Handling

```python
def safe_reasoning_step(func, action_file, default=None):
    """Execute reasoning step with error handling."""
    try:
        return func(action_file)
    except Exception as e:
        log_error(f"Error processing {action_file['file'].name}: {e}")
        return default

def log_error(message: str):
    """Log error to file."""
    timestamp = datetime.now().isoformat()
    log_file = Path('Logs') / f"errors_{datetime.now().strftime('%Y-%m-%d')}.json"
    
    error = {
        'timestamp': timestamp,
        'message': message
    }
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(error) + '\n')
```

## Best Practices

1. **Always create plans**: Every action file gets a Plan.md
2. **Use checkboxes**: Track progress visually
3. **Document decisions**: Note why actions were taken
4. **Flag approvals**: Never skip human review for sensitive actions
5. **Update state**: Track processed files to avoid duplicates

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Plans not created | Check file permissions |
| Duplicate processing | Clear reasoning state file |
| Approval not flagged | Review Company_Handbook.md rules |
| State file corrupted | Delete and recreate state file |
