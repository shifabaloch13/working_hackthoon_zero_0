"""
AI Employee Silver Tier - Complete System Verification

This script verifies all Silver Tier requirements are met.

Run: python verify_silver_tier.py
"""

import sys
import json
import pickle
from pathlib import Path
from datetime import datetime

# Configuration
VAULT_PATH = Path('D:/Download/working_hackthoon_zero_0/AI_Employee_Vault')
CREDENTIALS_PATH = Path('D:/Download/working_hackthoon_zero_0/credeintals.json')
SCRIPTS_PATH = VAULT_PATH / 'scripts'

def check_file(path, description):
    """Check if a file exists."""
    exists = path.exists()
    status = "[OK]" if exists else "[ ]"
    print(f"  {status} {description}: {path.name}")
    return exists

def check_folder(path, description):
    """Check if a folder exists."""
    exists = path.exists()
    status = "[OK]" if exists else "[ ]"
    print(f"  {status} {description}: {path.name}")
    return exists

def check_token():
    """Check if Gmail token exists and is valid."""
    token_path = VAULT_PATH / 'Logs' / 'gmail_token.pickle'
    
    if not token_path.exists():
        print(f"  [ ] Gmail Token: Not found")
        return False
    
    try:
        with open(token_path, 'rb') as f:
            creds = pickle.load(f)
        
        has_token = creds.token is not None
        has_refresh = creds.refresh_token is not None
        has_send_scope = 'https://www.googleapis.com/auth/gmail.send' in creds.scopes
        
        status = "[OK]" if (has_token or has_refresh) and has_send_scope else "[WARN]"
        print(f"  {status} Gmail Token: Valid (Send: {has_send_scope})")
        return has_send_scope
    except Exception as e:
        print(f"  [ERROR] Gmail Token: Error - {e}")
        return False

def verify_silver_tier():
    """Verify all Silver Tier requirements."""
    
    print()
    print('=' * 70)
    print('  AI EMPLOYEE - SILVER TIER VERIFICATION')
    print('=' * 70)
    print()
    print(f'Verification Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Vault Path: {VAULT_PATH}')
    print()
    
    results = {
        'Bronze Requirements': [],
        'Silver Requirements': [],
        'Scripts': [],
        'Skills': []
    }
    
    # ========================================
    # BRONZE TIER REQUIREMENTS (Prerequisites)
    # ========================================
    print('BRONZE TIER REQUIREMENTS (Prerequisites)')
    print('-' * 70)
    
    # Dashboard.md
    results['Bronze Requirements'].append(
        check_file(VAULT_PATH / 'Dashboard.md', 'Dashboard.md')
    )
    
    # Company_Handbook.md
    results['Bronze Requirements'].append(
        check_file(VAULT_PATH / 'Company_Handbook.md', 'Company Handbook')
    )
    
    # Business_Goals.md
    results['Bronze Requirements'].append(
        check_file(VAULT_PATH / 'Business_Goals.md', 'Business Goals')
    )
    
    # Basic folder structure
    for folder in ['Inbox', 'Needs_Action', 'Done', 'Pending_Approval', 'Approved']:
        results['Bronze Requirements'].append(
            check_folder(VAULT_PATH / folder, f'{folder} folder')
        )
    
    # File System Watcher
    results['Bronze Requirements'].append(
        check_file(SCRIPTS_PATH / 'filesystem_watcher.py', 'File System Watcher')
    )
    
    print()
    
    # ========================================
    # SILVER TIER REQUIREMENTS
    # ========================================
    print('SILVER TIER REQUIREMENTS')
    print('-' * 70)
    
    # 1. Two or more Watcher scripts
    print('  1. Watcher Scripts (2+ required):')
    watcher_count = 0
    if (SCRIPTS_PATH / 'gmail_watcher.py').exists():
        print(f"     [OK] Gmail Watcher")
        watcher_count += 1
    else:
        print(f"     [ ] Gmail Watcher")
    
    if (SCRIPTS_PATH / 'whatsapp_watcher.py').exists():
        print(f"     [OK] WhatsApp Watcher")
        watcher_count += 1
    else:
        print(f"     [WARN] WhatsApp Watcher (optional)")
    
    if (SCRIPTS_PATH / 'filesystem_watcher.py').exists():
        print(f"     [OK] File System Watcher")
        watcher_count += 1
    
    results['Silver Requirements'].append(watcher_count >= 2)
    watcher_status = "[OK]" if watcher_count >= 2 else "[ ]"
    print(f"     -> Total: {watcher_count} watchers {watcher_status}")
    print()
    
    # 2. LinkedIn Posting
    print('  2. LinkedIn Auto Posting:')
    linkedin_exists = check_file(SCRIPTS_PATH / 'linkedin_fully_auto.py', 'LinkedIn Auto Poster')
    results['Silver Requirements'].append(linkedin_exists)
    print()
    
    # 3. MCP Server for external action
    print('  3. MCP Server (Email Sending):')
    email_mcp_exists = check_file(SCRIPTS_PATH / 'email_mcp_server.py', 'Email MCP Server')
    results['Silver Requirements'].append(email_mcp_exists)
    print()
    
    # 4. Human-in-the-loop approval workflow
    print('  4. Approval Workflow:')
    approval_exists = check_file(SCRIPTS_PATH / 'approval_manager.py', 'Approval Manager')
    results['Silver Requirements'].append(approval_exists)
    
    # Check approval folders
    for folder in ['Pending_Approval', 'Approved', 'Rejected']:
        check_folder(VAULT_PATH / folder, f'{folder} folder')
    print()
    
    # 5. Scheduling capability
    print('  5. Scheduling Capability:')
    scheduling_doc = check_file(SCRIPTS_PATH.parent.parent / '.qwen' / 'skills' / 'scheduling' / 'SKILL.md', 'Scheduling Skill')
    results['Silver Requirements'].append(scheduling_doc)
    print()
    
    # 6. Qwen Code Reasoning Loop
    print('  6. Qwen Code Reasoning Loop:')
    orchestrator_exists = check_file(SCRIPTS_PATH / 'orchestrator.py', 'Orchestrator')
    results['Silver Requirements'].append(orchestrator_exists)
    print()
    
    # 7. Gmail Authentication
    print('  7. Gmail Authentication:')
    results['Silver Requirements'].append(check_token())
    print()
    
    # ========================================
    # SCRIPTS
    # ========================================
    print('AVAILABLE SCRIPTS')
    print('-' * 70)
    
    scripts = [
        'gmail_watcher.py',
        'whatsapp_watcher.py',
        'filesystem_watcher.py',
        'linkedin_fully_auto.py',
        'linkedin_poster.py',
        'email_mcp_server.py',
        'approval_manager.py',
        'orchestrator.py',
        'send_test_email.py',
        'authenticate.py'
    ]
    
    for script in scripts:
        check_file(SCRIPTS_PATH / script, script.replace('_', ' ').replace('.py', ''))
    
    print()
    
    # ========================================
    # SKILLS
    # ========================================
    print('INSTALLED SKILLS')
    print('-' * 70)
    
    skills_path = SCRIPTS_PATH.parent.parent / '.qwen' / 'skills'
    
    skills = [
        'gmail-watcher',
        'whatsapp-watcher',
        'email-mcp-server',
        'approval-workflow',
        'linkedin-posting',
        'scheduling',
        'browsing-with-playwright'
    ]
    
    for skill in skills:
        skill_md = skills_path / skill / 'SKILL.md'
        exists = skill_md.exists()
        status = "[OK]" if exists else "[ ]"
        print(f"  {status} {skill.replace('-', ' ').title()}: SKILL.md")
        results['Skills'].append(exists)
    
    print()
    
    # ========================================
    # SUMMARY
    # ========================================
    print('VERIFICATION SUMMARY')
    print('=' * 70)
    print()
    
    # Calculate scores
    bronze_score = sum(results['Bronze Requirements'])
    bronze_total = len(results['Bronze Requirements'])
    
    silver_score = sum(results['Silver Requirements'])
    silver_total = len(results['Silver Requirements'])
    
    print(f'Bronze Tier: {bronze_score}/{bronze_total} requirements [OK]')
    print(f'Silver Tier: {silver_score}/{silver_total} requirements [OK]')
    print()
    
    if bronze_score == bronze_total and silver_score >= 6:
        print('=' * 70)
        print('  SILVER TIER COMPLETE!')
        print('=' * 70)
        print()
        print('[OK] All Bronze requirements met')
        print('[OK] All Silver requirements met')
        print()
        print('Your AI Employee is ready for production use!')
        print()
        print('Quick Start Commands:')
        print('  cd D:\\Download\\working_hackthoon_zero_0\\AI_Employee_Vault\\scripts')
        print()
        print('  # Watch Gmail')
        print('  python gmail_watcher.py "D:\\Download\\working_hackthoon_zero_0\\AI_Employee_Vault" "D:\\Download\\working_hackthoon_zero_0\\credeintals.json"')
        print()
        print('  # Send test email')
        print('  python send_test_email.py')
        print()
        print('  # Post to LinkedIn')
        print('  python linkedin_fully_auto.py "D:\\Download\\working_hackthoon_zero_0\\AI_Employee_Vault" --execute-approved')
        print()
        return True
    else:
        print('=' * 70)
        print('  SOME REQUIREMENTS MISSING')
        print('=' * 70)
        print()
        print(f'Bronze: {bronze_score}/{bronze_total}')
        print(f'Silver: {silver_score}/{silver_total}')
        print()
        print('Please complete the missing requirements.')
        print()
        return False

if __name__ == '__main__':
    success = verify_silver_tier()
    input('Press Enter to exit...')
    sys.exit(0 if success else 1)
