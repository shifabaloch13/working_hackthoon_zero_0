---
name: error-recovery
description: |
  Error recovery and graceful degradation system for AI Employee.
  Handles failures, retries transient errors, and maintains system stability.
  Use for production-ready reliability.
---

# Error Recovery Skill

Fault tolerance and graceful degradation for AI Employee.

## Overview

Provides:
- Automatic retry for transient errors
- Graceful degradation when services fail
- Error categorization and handling
- System health monitoring

## Error Categories

| Category | Examples | Handling |
|----------|----------|----------|
| **Transient** | Network timeout, API rate limit | Exponential backoff retry |
| **Authentication** | Expired token, revoked access | Alert human, pause operations |
| **Logic** | AI misinterprets message | Human review queue |
| **Data** | Corrupted file, missing field | Quarantine + alert |
| **System** | Process crash, disk full | Watchdog + auto-restart |

## Implementation

### retry_handler.py

```python
#!/usr/bin/env python3
"""
Retry Handler with Exponential Backoff
"""

import time
from functools import wraps


def with_retry(max_attempts=3, base_delay=1, max_delay=60):
    """Decorator for retry with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except TransientError as e:
                    if attempt == max_attempts - 1:
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    print(f'Retrying in {delay}s (attempt {attempt+1}/{max_attempts})')
                    time.sleep(delay)
        return wrapper
    return decorator


@with_retry(max_attempts=3)
def send_email(to, subject, body):
    """Send email with retry."""
    # Implementation
    pass
```

### Graceful Degradation

```python
def degrade_gracefully(error: Exception):
    """Handle errors gracefully."""
    
    if isinstance(error, GmailAPIError):
        # Queue emails locally
        queue_email_for_later()
        notify_human('Gmail API unavailable, queuing emails')
        
    elif isinstance(error, DatabaseError):
        # Use in-memory cache
        switch_to_memory_cache()
        notify_human('Database unavailable, using cache')
        
    elif isinstance(error, DiskSpaceError):
        # Free up space or pause
        cleanup_old_logs()
        notify_human('Low disk space, cleaned up logs')
```

## Watchdog Process

```python
# watchdog.py
import subprocess
from pathlib import Path

PROCESSES = {
    'orchestrator': 'python orchestrator.py ../AI_Employee_Vault',
    'gmail_watcher': 'python gmail_watcher.py ../AI_Employee_Vault ../credeintals.json',
    'file_watcher': 'python filesystem_watcher.py ../AI_Employee_Vault'
}

def check_and_restart():
    """Check processes and restart if needed."""
    for name, cmd in PROCESSES.items():
        pid_file = Path(f'/tmp/{name}.pid')
        if not is_process_running(pid_file):
            print(f'{name} not running, restarting...')
            proc = subprocess.Popen(cmd.split())
            pid_file.write_text(str(proc.pid))
            notify_human(f'{name} was restarted')
```

## Best Practices

1. **Always log errors** with full context
2. **Retry transient errors** with backoff
3. **Alert humans** for persistent failures
4. **Degrade gracefully** when possible
5. **Monitor system health** continuously
