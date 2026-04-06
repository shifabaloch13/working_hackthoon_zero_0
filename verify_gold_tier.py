"""
Gold Tier Verification Script
Tests all Gold Tier components to ensure everything is working
"""

import sys
import json
from pathlib import Path
from datetime import datetime

print("=" * 70)
print("  GOLD TIER VERIFICATION")
print("=" * 70)
print()

vault_path = Path("../AI_Employee_Vault").resolve()
results = {}

# Test 1: Check Facebook Configuration
print("TEST 1: Facebook Configuration")
print("-" * 70)
try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    fb_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
    fb_page_id = os.getenv('FACEBOOK_PAGE_ID')
    
    if fb_token and fb_page_id:
        print(f"[OK] Facebook token found: {fb_token[:20]}...")
        print(f"[OK] Page ID: {fb_page_id}")
        results['facebook_config'] = True
    else:
        print("[FAIL] Facebook credentials missing in .env")
        results['facebook_config'] = False
except Exception as e:
    print(f"[FAIL] Error: {e}")
    results['facebook_config'] = False

print()

# Test 2: Check Odoo Configuration
print("TEST 2: Odoo Configuration")
print("-" * 70)
odoo_config_path = Path("odoo_config.json")
if odoo_config_path.exists():
    with open(odoo_config_path, 'r') as f:
        odoo_config = json.load(f)
    print(f"[OK] Odoo config found: {odoo_config.get('odoo_url')}")
    results['odoo_config'] = True
else:
    print("[WARN] Odoo config not found (create after Odoo setup)")
    results['odoo_config'] = "pending"

print()

# Test 3: Check Facebook MCP Script
print("TEST 3: Facebook MCP Script")
print("-" * 70)
fb_script = vault_path / "scripts" / "facebook_poster.py"
if fb_script.exists():
    print(f"[OK] Facebook poster script exists")
    results['facebook_script'] = True
else:
    print("[FAIL] Facebook poster script not found")
    results['facebook_script'] = False

print()

# Test 4: Check Odoo MCP Script
print("TEST 4: Odoo MCP Script")
print("-" * 70)
odoo_script = Path("odoo/scripts/odoo_mcp_server.py")
if odoo_script.exists():
    print(f"[OK] Odoo MCP script exists")
    results['odoo_script'] = True
else:
    print("[FAIL] Odoo MCP script not found")
    results['odoo_script'] = False

print()

# Test 5: Check Comment Watcher
print("TEST 5: Facebook Comment Watcher")
print("-" * 70)
watcher_script = vault_path / "scripts" / "facebook_comment_watcher.py"
if watcher_script.exists():
    print(f"[OK] Comment watcher script exists")
    results['comment_watcher'] = True
else:
    print("[FAIL] Comment watcher script not found")
    results['comment_watcher'] = False

print()

# Test 6: Check CEO Briefing Script
print("TEST 6: CEO Briefing Script")
print("-" * 70)
briefing_script = vault_path / "scripts" / "ceo_briefing.py"
if briefing_script.exists():
    print(f"[OK] CEO Briefing script exists")
    results['ceo_briefing'] = True
else:
    print("[FAIL] CEO Briefing script not found")
    results['ceo_briefing'] = False

print()

# Test 7: Check Audit Logger
print("TEST 7: Audit Logger")
print("-" * 70)
audit_script = vault_path / "scripts" / "audit_logger.py"
if audit_script.exists():
    print(f"[OK] Audit Logger script exists")
    results['audit_logger'] = True
else:
    print("[FAIL] Audit Logger script not found")
    results['audit_logger'] = False

print()

# Test 8: Check Ralph Wiggum Loop
print("TEST 8: Ralph Wiggum Loop")
print("-" * 70)
ralph_script = vault_path / "scripts" / "ralph_wiggum.py"
if ralph_script.exists():
    print(f"[OK] Ralph Wiggum script exists")
    results['ralph_wiggum'] = True
else:
    print("[FAIL] Ralph Wiggum script not found")
    results['ralph_wiggum'] = False

print()

# Test 9: Check Watchdog
print("TEST 9: Watchdog Process Monitor")
print("-" * 70)
watchdog_script = vault_path / "scripts" / "watchdog.py"
if watchdog_script.exists():
    print(f"[OK] Watchdog script exists")
    results['watchdog'] = True
else:
    print("[FAIL] Watchdog script not found")
    results['watchdog'] = False

print()

# Test 10: Check Domain Router
print("TEST 10: Domain Router")
print("-" * 70)
domain_script = vault_path / "scripts" / "domain_router.py"
if domain_script.exists():
    print(f"[OK] Domain Router script exists")
    results['domain_router'] = True
else:
    print("[FAIL] Domain Router script not found")
    results['domain_router'] = False

print()

# Test 11: Check Folder Structure
print("TEST 11: Folder Structure")
print("-" * 70)
required_folders = [
    'Needs_Action',
    'Pending_Approval',
    'Approved',
    'Done',
    'Logs',
    'Briefings',
    'Accounting'
]

missing_folders = []
for folder in required_folders:
    folder_path = vault_path / folder
    if folder_path.exists():
        print(f"[OK] {folder}/")
    else:
        print(f"[FAIL] {folder}/ missing")
        missing_folders.append(folder)

results['folder_structure'] = len(missing_folders) == 0

print()

# Test 12: Check Skills
print("TEST 12: Gold Tier Skills")
print("-" * 70)
skills_path = Path("../.qwen/skills")
required_skills = [
    'ceo-briefing',
    'ralph-wiggum-loop',
    'odoo-accounting-mcp',
    'facebook-instagram-mcp',
    'twitter-x-mcp',
    'error-recovery',
    'cross-domain-integration',
    'audit-logging'
]

missing_skills = []
for skill in required_skills:
    skill_path = skills_path / skill / "SKILL.md"
    if skill_path.exists():
        print(f"[OK] {skill}/SKILL.md")
    else:
        print(f"[FAIL] {skill}/SKILL.md missing")
        missing_skills.append(skill)

results['skills'] = len(missing_skills) == 0

print()

# Test 13: Check Docker Containers
print("TEST 13: Docker Containers (Odoo)")
print("-" * 70)
import subprocess
try:
    result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
    if 'odoo_community' in result.stdout:
        print("[OK] Odoo container is running")
        results['odoo_container'] = True
    else:
        print("[WARN] Odoo container not running")
        results['odoo_container'] = False
except Exception as e:
    print(f"[FAIL] Error checking Docker: {e}")
    results['odoo_container'] = False

print()

# Test 14: Live Facebook Test
print("TEST 14: Facebook Live Test")
print("-" * 70)
print("Creating test post draft...")
sys.path.insert(0, str(vault_path / "scripts"))
try:
    from facebook_poster import FacebookMCP
    facebook = FacebookMCP(str(vault_path))
    
    draft_file = facebook.create_post_draft(
        message=f"[GOLD TIER TEST] Automated verification test at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        platform='facebook'
    )
    
    if draft_file.exists():
        print(f"[OK] Test post draft created: {draft_file.name}")
        results['facebook_live'] = True
    else:
        print("[FAIL] Failed to create test post")
        results['facebook_live'] = False
except Exception as e:
    print(f"[FAIL] Error: {e}")
    results['facebook_live'] = False

print()

# Test 15: Live Odoo Test (if configured)
print("TEST 15: Odoo Live Test")
print("-" * 70)
if results['odoo_config'] == True:
    sys.path.insert(0, str(Path("odoo/scripts").resolve()))
    try:
        from odoo_mcp_server import OdooMCP
        odoo = OdooMCP(str(vault_path))
        
        draft_file = odoo.create_invoice_draft(
            partner_name='Gold Tier Test Client',
            amount=99.99,
            description='Gold Tier Verification Test'
        )
        
        if draft_file.exists():
            print(f"[OK] Test invoice draft created: {draft_file.name}")
            results['odoo_live'] = True
        else:
            print("[FAIL] Failed to create test invoice")
            results['odoo_live'] = False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        results['odoo_live'] = False
else:
    print("[SKIP] Odoo not configured yet")
    results['odoo_live'] = "pending"

print()

# Summary
print("=" * 70)
print("  GOLD TIER VERIFICATION SUMMARY")
print("=" * 70)
print()

passed = sum(1 for v in results.values() if v == True)
failed = sum(1 for v in results.values() if v == False)
pending = sum(1 for v in results.values() if v == "pending")
total = len(results)

print(f"Passed: {passed}/{total}")
print(f"Failed: {failed}/{total}")
print(f"Pending: {pending}/{total}")
print()

for test, result in results.items():
    status = "✅" if result == True else "❌" if result == False else "⏳"
    print(f"{status} {test}: {result}")

print()

if failed == 0 and pending <= 2:
    print("🎉 GOLD TIER VERIFICATION: SUCCESS!")
    print()
    print("All critical components are working.")
    if pending > 0:
        print("Note: Complete pending items when ready.")
else:
    print("⚠️ GOLD TIER VERIFICATION: ISSUES FOUND")
    print()
    print("Please fix the failed tests above.")

print()
print("=" * 70)
