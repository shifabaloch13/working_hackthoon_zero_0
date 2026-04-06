"""
AI Employee System Test Script
Tests the complete workflow from file drop to dashboard update
"""

import sys
import time
from pathlib import Path

# Add scripts folder to path
sys.path.insert(0, str(Path(__file__).parent))

from filesystem_watcher import FileSystemWatcher
from orchestrator import Orchestrator

# Vault path
VAULT_PATH = "D:/Download/working_hackthoon_zero_0/AI_Employee_Vault"

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_step(num, text):
    print(f"\n[STEP {num}] {text}")
    print("-" * 40)

def main():
    print_header("AI EMPLOYEE SYSTEM - COMPLETE WORKFLOW TEST")
    
    # Initialize components
    print_step(0, "Initializing Components")
    watcher = FileSystemWatcher(VAULT_PATH)
    orchestrator = Orchestrator(VAULT_PATH)
    print("[OK] FileSystemWatcher initialized")
    print("[OK] Orchestrator initialized")
    
    # Check initial state
    print_step(1, "Checking Initial State")
    drop_folder = Path(VAULT_PATH) / "Drop"
    needs_action = Path(VAULT_PATH) / "Needs_Action"
    plans = Path(VAULT_PATH) / "Plans"
    
    drop_files = list(drop_folder.iterdir())
    na_files = list(needs_action.iterdir())
    plan_files = list(plans.iterdir())
    
    print("  Drop folder: {} files".format(len(drop_files)))
    print("  Needs_Action folder: {} files".format(len(na_files)))
    print("  Plans folder: {} files".format(len(plan_files)))
    
    if len(drop_files) == 0 and len(na_files) == 0 and len(plan_files) == 0:
        print("[OK] Initial state is clean")
    else:
        print("[WARN] Folders are not empty")
    
    # Test file content
    test_content = """
PAYMENT REQUEST
===============
Request ID: PAY-2026-001
Date: February 26, 2026

Vendor: ABC Supplies
Amount: $750.00
Description: Office supplies for Q1
Due Date: March 15, 2026

Approval Required: Yes
"""
    
    # Create test file
    print_step(2, "Creating Test File in Drop Folder")
    test_file = drop_folder / "payment_request_PAY-2026-001.txt"
    test_file.write_text(test_content, encoding='utf-8')
    print("  Created: {}".format(test_file.name))
    print("  Size: {} bytes".format(test_file.stat().st_size))
    print("[OK] Test file created")
    
    # Run watcher
    print_step(3, "Running FileSystemWatcher")
    print("  Scanning Drop folder...")
    items = watcher.check_for_updates()
    print("  Found {} new file(s)".format(len(items)))
    
    if len(items) > 0:
        print("  Creating action files...")
        for item in items:
            filepath = watcher.create_action_file(item)
            print("    -> Created: {}".format(filepath.name))
        print("[OK] FileSystemWatcher completed")
    else:
        print("[ERROR] No files detected!")
        return False
    
    # Run orchestrator
    print_step(4, "Running Orchestrator")
    print("  Processing Needs_Action folder...")
    orchestrator.run_once()
    print("[OK] Orchestrator completed")
    
    # Verify results
    print_step(5, "Verifying Results")
    
    # Check Needs_Action
    na_files = list(needs_action.iterdir())
    print("  Needs_Action files: {}".format(len(na_files)))
    for f in na_files:
        print("    [OK] {}".format(f.name))
    
    # Check Plans
    plan_files = list(plans.iterdir())
    print("  Plans files: {}".format(len(plan_files)))
    for f in plan_files:
        print("    [OK] {}".format(f.name))
    
    # Check Dashboard
    dashboard = Path(VAULT_PATH) / "Dashboard.md"
    if dashboard.exists():
        content = dashboard.read_text(encoding='utf-8')
        if "payment_request" in content.lower():
            print("  [OK] Dashboard.md updated with activity")
        else:
            print("  [WARN] Dashboard.md may not be updated correctly")
    else:
        print("  [ERROR] Dashboard.md not found!")
    
    # Check Logs
    logs_folder = Path(VAULT_PATH) / "Logs"
    log_files = list(logs_folder.iterdir())
    print("  Log files: {}".format(len(log_files)))
    for f in log_files:
        print("    -> {}".format(f.name))
    
    # Final summary
    print_header("TEST SUMMARY")
    
    success = True
    
    if len(items) > 0:
        print("[PASS] FileSystemWatcher")
    else:
        print("[FAIL] FileSystemWatcher")
        success = False
    
    if len(na_files) > 0:
        print("[PASS] Action File Creation")
    else:
        print("[FAIL] Action File Creation")
        success = False
    
    if len(plan_files) > 0:
        print("[PASS] Plan Creation")
    else:
        print("[FAIL] Plan Creation")
        success = False
    
    if dashboard.exists() and "payment_request" in content.lower():
        print("[PASS] Dashboard Update")
    else:
        print("[FAIL] Dashboard Update")
        success = False
    
    print()
    if success:
        print_header("ALL TESTS PASSED")
    else:
        print_header("SOME TESTS FAILED")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
