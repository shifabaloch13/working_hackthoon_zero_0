---
name: ralph-wiggum-loop
description: |
  Persistence loop that keeps Qwen Code working until tasks are complete.
  Implements the Ralph Wiggum Stop hook pattern for autonomous multi-step task completion.
  Use for complex workflows requiring multiple iterations.
---

# Ralph Wiggum Loop Skill

Autonomous task persistence system for AI Employee.

## Overview

The Ralph Wiggum Loop keeps Qwen Code working autonomously until a task is complete by:
1. Intercepting exit attempts
2. Checking if task is complete
3. Re-injecting prompt if incomplete
4. Continuing until completion or max iterations

## Prerequisites

1. **Qwen Code** with Stop hook support
2. **State files** in Plans/ folder
3. **Completion criteria** defined

## Usage

### Start Ralph Loop

```bash
# Start a Ralph loop
/ralph-loop "Process all files in Needs_Action, move to Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

### Completion Strategies

**1. Promise-based (Simple):**
Qwen Code outputs `<promise>TASK_COMPLETE</promise>` when done.

**2. File movement (Advanced):**
Stop hook detects when task file moves to Done/.

## Implementation

### ralph_wiggum.py

```python
#!/usr/bin/env python3
"""
Ralph Wiggum Loop - Persistence for AI Employee

Keeps Qwen Code working until tasks are complete.
"""

import sys
import time
from pathlib import Path


class RalphWiggumLoop:
    def __init__(self, vault_path: str, prompt: str, max_iterations: int = 10):
        self.vault = Path(vault_path).resolve()
        self.prompt = prompt
        self.max_iterations = max_iterations
        self.state_file = self.vault / 'Logs' / 'ralph_state.json'
        
    def run(self):
        """Run the Ralph Wiggum persistence loop."""
        
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f'\n[Ralph Loop] Iteration {iteration}/{self.max_iterations}')
            
            # Check if task is complete
            if self._is_task_complete():
                print('[Ralph Loop] Task complete! Exiting.')
                return True
            
            # Execute prompt
            print(f'[Ralph Loop] Executing: {self.prompt}')
            self._execute_prompt()
            
            # Wait for completion
            time.sleep(5)
        
        print('[Ralph Loop] Max iterations reached.')
        return False
    
    def _is_task_complete(self) -> bool:
        """Check if task is complete."""
        # Check if Needs_Action is empty
        needs_action = self.vault / 'Needs_Action'
        if needs_action.exists():
            files = list(needs_action.iterdir())
            if len(files) == 0:
                return True
        return False
    
    def _execute_prompt(self):
        """Execute the prompt."""
        # Implementation to execute Qwen Code with prompt
        pass


def main():
    if len(sys.argv) < 3:
        print('Usage: python ralph_wiggum.py <vault_path> <prompt>')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    prompt = sys.argv[2]
    
    loop = RalphWiggumLoop(vault_path, prompt)
    loop.run()


if __name__ == '__main__':
    main()
```

## Integration

### Qwen Code Stop Hook

Configure in Qwen Code settings:

```json
{
  "stop_hooks": [
    {
      "pattern": "exit",
      "action": "check_ralph_loop",
      "script": "python scripts/ralph_wiggum.py"
    }
  ]
}
```

## Best Practices

1. **Define clear completion criteria**
2. **Set reasonable max iterations** (5-10)
3. **Log each iteration** for debugging
4. **Monitor resource usage**
