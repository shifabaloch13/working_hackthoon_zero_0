"""
Error Recovery and Watchdog - Gold Tier

Handles errors with retry logic, graceful degradation, and process monitoring.
Based on hackathon documentation requirements for error recovery and graceful degradation.

Usage:
    python watchdog.py "D:/path/to/AI_Employee_Vault"
"""

import sys
import time
import subprocess
import json
from pathlib import Path
from datetime import datetime
from functools import wraps


# ============================================
# Retry Handler with Exponential Backoff
# ============================================

class TransientError(Exception):
    """Transient error that can be retried."""
    pass


class AuthenticationError(Exception):
    """Authentication error requiring re-authentication."""
    pass


class DataError(Exception):
    """Data error requiring human review."""
    pass


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
                    print(f'[RETRY] Retrying in {delay}s (attempt {attempt+1}/{max_attempts})')
                    print(f'[RETRY] Error: {e}')
                    time.sleep(delay)
                except AuthenticationError as e:
                    print(f'[AUTH] Authentication error: {e}')
                    print(f'[AUTH] Pausing operations, alerting human...')
                    raise
                except DataError as e:
                    print(f'[DATA] Data error: {e}')
                    print(f'[DATA] Quarantining for human review...')
                    raise
        return wrapper
    return decorator


# Example usage
@with_retry(max_attempts=3)
def send_email_with_retry(to, subject, body):
    """Send email with retry logic."""
    # Implementation would go here
    print(f'[EMAIL] Sending to {to}: {subject}')
    # Simulate potential transient error
    # raise TransientError("Network timeout")
    return True


# ============================================
# Graceful Degradation Handler
# ============================================

class GracefulDegradation:
    """Handle service failures gracefully."""
    
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.logs_folder = self.vault / 'Logs'
        self.degradation_state = {}
    
    def handle_gmail_error(self, error: Exception):
        """Handle Gmail API errors."""
        print(f'[GMAIL] Gmail API error: {error}')
        print(f'[GMAIL] Queueing emails locally...')
        
        # Queue emails for later
        queue_file = self.logs_folder / 'email_queue.json'
        queue = []
        if queue_file.exists():
            with open(queue_file, 'r') as f:
                queue = json.load(f)
        
        # Add to queue
        queue.append({
            'timestamp': datetime.now().isoformat(),
            'status': 'queued',
            'reason': 'Gmail API unavailable'
        })
        
        with open(queue_file, 'w') as f:
            json.dump(queue, f, indent=2)
        
        print(f'[GMAIL] Emails queued. {len(queue)} pending.')
    
    def handle_database_error(self, error: Exception):
        """Handle database errors."""
        print(f'[DATABASE] Database error: {error}')
        print(f'[DATABASE] Switching to in-memory cache...')
        
        # Switch to memory cache
        self.degradation_state['database'] = 'memory_cache'
        
        print(f'[DATABASE] Using memory cache until database is restored.')
    
    def handle_disk_space_error(self, error: Exception):
        """Handle disk space errors."""
        print(f'[DISK] Disk space error: {error}')
        print(f'[DISK] Cleaning up old logs...')
        
        # Clean up old logs
        logs_folder = self.vault / 'Logs'
        if logs_folder.exists():
            for log_file in logs_folder.glob('*.json'):
                # Delete logs older than 7 days
                mtime = log_file.stat().st_mtime
                age_days = (datetime.now().timestamp() - mtime) / 86400
                if age_days > 7:
                    log_file.unlink()
                    print(f'[DISK] Deleted old log: {log_file.name}')
        
        print(f'[DISK] Cleanup complete.')


# ============================================
# Watchdog Process Monitor
# ============================================

class Watchdog:
    """Monitor and restart critical processes."""
    
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.logs_folder = self.vault / 'Logs'
        self.pid_folder = self.logs_folder / 'pids'
        self.pid_folder.mkdir(parents=True, exist_ok=True)
        
        # Define critical processes
        self.processes = {
            'orchestrator': {
                'command': f'python orchestrator.py "{self.vault}"',
                'check_interval': 60
            },
            'gmail_watcher': {
                'command': f'python gmail_watcher.py "{self.vault}" "{self.vault.parent}/credeintals.json"',
                'check_interval': 30
            },
            'filesystem_watcher': {
                'command': f'python filesystem_watcher.py "{self.vault}"',
                'check_interval': 30
            }
        }
        
        self.running_processes = {}
    
    def start_process(self, name: str) -> subprocess.Popen:
        """Start a process."""
        cmd = self.processes[name]['command']
        print(f'[WATCHDOG] Starting {name}...')
        
        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Save PID
        pid_file = self.pid_folder / f'{name}.pid'
        pid_file.write_text(str(proc.pid))
        
        self.running_processes[name] = proc
        print(f'[WATCHDOG] {name} started (PID: {proc.pid})')
        
        return proc
    
    def check_process(self, name: str) -> bool:
        """Check if a process is running."""
        if name not in self.running_processes:
            return False
        
        proc = self.running_processes[name]
        return proc.poll() is None
    
    def restart_process(self, name: str):
        """Restart a process."""
        print(f'[WATCHDOG] {name} not running, restarting...')
        
        # Stop old process if exists
        if name in self.running_processes:
            proc = self.running_processes[name]
            if proc.poll() is None:
                proc.terminate()
        
        # Start new process
        self.start_process(name)
        
        # Alert human
        self._notify_human(f'{name} was restarted')
    
    def _notify_human(self, message: str):
        """Notify human of important events."""
        print(f'[ALERT] {message}')
        
        # Log the notification
        alert_file = self.logs_folder / f'alert_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        alert_file.write_text(f'{datetime.now().isoformat()}: {message}\n')
    
    def run(self):
        """Run the watchdog."""
        print()
        print('=' * 70)
        print('  WATCHDOG - Process Monitor')
        print('=' * 70)
        print()
        print(f'[INFO] Monitoring {len(self.processes)} processes:')
        for name in self.processes:
            print(f'  - {name}')
        print()
        print('[INFO] Press Ctrl+C to stop')
        print()
        
        # Start all processes
        for name in self.processes:
            self.start_process(name)
        
        # Monitor loop
        try:
            while True:
                for name, config in self.processes.items():
                    if not self.check_process(name):
                        self.restart_process(name)
                
                time.sleep(config['check_interval'])
        except KeyboardInterrupt:
            print()
            print('[WATCHDOG] Stopping all processes...')
            for name, proc in self.running_processes.items():
                if proc.poll() is None:
                    proc.terminate()
                    print(f'[WATCHDOG] {name} stopped')
            print('[WATCHDOG] Watchdog stopped')


def main():
    if len(sys.argv) < 2:
        print('Usage: python watchdog.py <vault_path>')
        print()
        print('Examples:')
        print('  python watchdog.py "../AI_Employee_Vault"  # Start watchdog')
        print('  python watchdog.py "../AI_Employee_Vault" --check  # Check status')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    # Start watchdog
    watchdog = Watchdog(vault_path)
    watchdog.run()


if __name__ == '__main__':
    main()
