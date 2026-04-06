"""
Ralph Wiggum Loop - Gold Tier Implementation

Keeps Qwen Code working autonomously until tasks are complete by detecting
file movement from Needs_Action/ to Done/.

Based on hackathon documentation Section 2D - Persistence (The "Ralph Wiggum" Loop)

Usage:
    python ralph_wiggum.py "D:/path/to/AI_Employee_Vault" --prompt "Process all files"
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime


class RalphWiggumLoop:
    """
    Ralph Wiggum Loop - Persistence for AI Employee
    
    Monitors file movement and keeps processing until all tasks are complete.
    """
    
    def __init__(self, vault_path: str, prompt: str, max_iterations: int = 10):
        self.vault = Path(vault_path).resolve()
        self.prompt = prompt
        self.max_iterations = max_iterations
        self.state_file = self.vault / 'Logs' / 'ralph_state.json'
        self.needs_action = self.vault / 'Needs_Action'
        self.done_folder = self.vault / 'Done'
        
        # Ensure folders exist
        for folder in [self.needs_action, self.done_folder]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Load state
        self.state = self._load_state()
    
    def _load_state(self) -> dict:
        """Load state from file."""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'iterations': 0,
            'files_processed': [],
            'started': datetime.now().isoformat(),
            'last_check': None
        }
    
    def _save_state(self):
        """Save state to file."""
        self.state['last_check'] = datetime.now().isoformat()
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2)
    
    def is_task_complete(self) -> bool:
        """
        Check if task is complete by monitoring file movement.
        
        Task is complete when:
        1. Needs_Action/ folder is empty, OR
        2. All files have been moved to Done/
        """
        # Check if Needs_Action is empty
        if not self.needs_action.exists():
            return True
        
        files = list(self.needs_action.iterdir())
        return len(files) == 0
    
    def get_pending_files(self) -> list:
        """Get list of pending files in Needs_Action."""
        if not self.needs_action.exists():
            return []
        
        return [f.name for f in self.needs_action.iterdir() if f.is_file()]
    
    def run(self):
        """Run the Ralph Wiggum persistence loop."""
        
        print()
        print('=' * 70)
        print('  RALPH WIGGUM LOOP - Task Persistence')
        print('=' * 70)
        print()
        print(f'[INFO] Task: {self.prompt}')
        print(f'[INFO] Max iterations: {self.max_iterations}')
        print(f'[INFO] Monitoring: {self.needs_action}')
        print()
        
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            self.state['iterations'] = iteration
            
            print(f'\n[LOOP] Iteration {iteration}/{self.max_iterations}')
            print('-' * 70)
            
            # Check pending files
            pending = self.get_pending_files()
            print(f'[LOOP] Pending files: {len(pending)}')
            
            for file in pending[:5]:  # Show first 5
                print(f'  - {file}')
            
            if len(pending) > 5:
                print(f'  ... and {len(pending) - 5} more')
            
            # Check if complete
            if self.is_task_complete():
                print()
                print('=' * 70)
                print('  ✅ TASK COMPLETE!')
                print('=' * 70)
                print()
                print(f'[LOOP] All files processed in {iteration} iterations')
                print(f'[LOOP] Started: {self.state["started"]}')
                print(f'[LOOP] Completed: {datetime.now().isoformat()}')
                print()
                
                self._save_state()
                return True
            
            # Execute the task (in real implementation, this would call Qwen Code)
            print()
            print(f'[LOOP] Executing: {self.prompt}')
            print('[LOOP] Waiting for file movement...')
            
            # Wait for file movement (simulated - in real use, Qwen Code would process)
            time.sleep(5)
            
            # Check if files were moved
            new_pending = self.get_pending_files()
            if len(new_pending) < len(pending):
                moved = len(pending) - len(new_pending)
                print(f'[LOOP] {moved} file(s) moved to Done/')
            
            self._save_state()
            
            # Wait before next iteration
            time.sleep(2)
        
        print()
        print('=' * 70)
        print('  [WARN] MAX ITERATIONS REACHED')
        print('=' * 70)
        print()
        print(f'[LOOP] Task not complete after {self.max_iterations} iterations')
        print(f'[LOOP] Remaining files: {len(self.get_pending_files())}')
        print()
        
        self._save_state()
        return False


def main():
    if len(sys.argv) < 3:
        print('Usage: python ralph_wiggum.py <vault_path> <prompt>')
        print()
        print('Example:')
        print('  python ralph_wiggum.py "../AI_Employee_Vault" "Process all files in Needs_Action"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    prompt = sys.argv[2]
    
    # Optional: max iterations
    max_iterations = 10
    if '--max-iterations' in sys.argv:
        idx = sys.argv.index('--max-iterations') + 1
        if idx < len(sys.argv):
            max_iterations = int(sys.argv[idx])
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    loop = RalphWiggumLoop(vault_path, prompt, max_iterations)
    success = loop.run()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
