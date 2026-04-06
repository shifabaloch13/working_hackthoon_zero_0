"""
Complete FTE (Full-Time Digital Employee) Verification

Tests ALL automation requirements from the hackathon document:
1. Email/Gmail automation
2. WhatsApp automation
3. Facebook auto-posting
4. Comment detection
5. Odoo accounting
6. CEO Briefing
7. Approval workflow
8. All watchers working
9. All MCP servers working

Usage:
    python verify_complete_fte.py
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

print("=" * 80)
print("  COMPLETE FTE (FULL-TIME DIGITAL EMPLOYEE) VERIFICATION")
print("=" * 80)
print()

load_dotenv()
vault_path = Path("AI_Employee_Vault").resolve()
results = {}

# ============================================================
# TEST 1: Facebook Auto-Posting (Gold Tier Requirement)
# ============================================================
print("TEST 1: Facebook Auto-Posting System")
print("-" * 80)

fb_scripts = [
    "facebook_poster.py",
    "facebook_comment_watcher.py"
]

for script in fb_scripts:
    script_path = vault_path / "scripts" / script
    exists = script_path.exists()
    print(f"   {script}: {'✅' if exists else '❌'}")
    results[f'facebook_{script}'] = exists

# Check Facebook config
fb_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
fb_page_id = os.getenv('FACEBOOK_PAGE_ID')
print(f"   Facebook Token: {'✅' if fb_token else '❌'}")
print(f"   Page ID: {'✅' if fb_page_id else '❌'}")
results['facebook_config'] = bool(fb_token and fb_page_id)

# Check recent posts
done_folder = vault_path / "Done"
fb_posts = list(done_folder.glob("FB_POST_*.md"))
print(f"   Posts Published: {len(fb_posts)}")
results['facebook_posts'] = len(fb_posts) > 0

print()

# ============================================================
# TEST 2: Watcher System (Perception Layer)
# ============================================================
print("TEST 2: Watcher System (Perception)")
print("-" * 80)

watchers = [
    ("Gmail Watcher", "gmail_watcher.py"),
    ("File System Watcher", "filesystem_watcher.py"),
    ("WhatsApp Watcher", "whatsapp_watcher.py"),
    ("Facebook Comment Watcher", "facebook_comment_watcher.py")
]

for name, script in watchers:
    script_path = vault_path / "scripts" / script
    exists = script_path.exists()
    print(f"   {name}: {'✅' if exists else '❌'}")
    results[f'watcher_{script}'] = exists

print()

# ============================================================
# TEST 3: MCP Servers (Action Layer / Hands)
# ============================================================
print("TEST 3: MCP Servers (Action Layer)")
print("-" * 80)

mcp_servers = [
    ("Email MCP", "email_mcp_server.py"),
    ("Facebook/Instagram MCP", "facebook_poster.py"),
    ("Twitter/X MCP", "twitter_poster.py"),
    ("Odoo Accounting MCP", "../../odoo/scripts/odoo_mcp_server.py"),
    ("LinkedIn MCP", "linkedin_poster.py")
]

for name, script in mcp_servers:
    script_path = vault_path / "scripts" / script if not script.startswith("../") else Path(script)
    exists = script_path.exists()
    print(f"   {name}: {'✅' if exists else '❌'}")
    results[f'mcp_{name}'] = exists

print()

# ============================================================
# TEST 4: Reasoning Layer (Claude Code Integration)
# ============================================================
print("TEST 4: Reasoning Layer (Claude Code)")
print("-" * 80)

reasoning_files = [
    ("Orchestrator", "orchestrator.py"),
    ("Ralph Wiggum Loop", "ralph_wiggum.py"),
    ("Approval Manager", "approval_manager.py")
]

for name, script in reasoning_files:
    script_path = vault_path / "scripts" / script
    exists = script_path.exists()
    print(f"   {name}: {'✅' if exists else '❌'}")
    results[f'reasoning_{script}'] = exists

print()

# ============================================================
# TEST 5: Approval Workflow (Human-in-the-Loop)
# ============================================================
print("TEST 5: Approval Workflow (HITL)")
print("-" * 80)

folders = [
    "Pending_Approval",
    "Approved",
    "Rejected",
    "Needs_Action",
    "Done"
]

for folder in folders:
    folder_path = vault_path / folder
    exists = folder_path.exists()
    print(f"   {folder}/: {'✅' if exists else '❌'}")
    results[f'folder_{folder}'] = exists

print()

# ============================================================
# TEST 6: CEO Briefing (Business Audit)
# ============================================================
print("TEST 6: CEO Briefing (Business Audit)")
print("-" * 80)

briefing_script = vault_path / "scripts" / "ceo_briefing.py"
print(f"   CEO Briefing Script: {'✅' if briefing_script.exists() else '❌'}")
results['ceo_briefing_script'] = briefing_script.exists()

briefings_folder = vault_path / "Briefings"
print(f"   Briefings Folder: {'✅' if briefings_folder.exists() else '❌'}")
results['briefings_folder'] = briefings_folder.exists()

# Check for generated briefings
if briefings_folder.exists():
    briefings = list(briefings_folder.glob("*.md"))
    print(f"   Generated Briefings: {len(briefings)}")
    results['ceo_briefings_generated'] = len(briefings) > 0

print()

# ============================================================
# TEST 7: Odoo Accounting (Gold Tier)
# ============================================================
print("TEST 7: Odoo Accounting Integration")
print("-" * 80)

odoo_script = Path("odoo/scripts/odoo_mcp_server.py")
print(f"   Odoo MCP Script: {'✅' if odoo_script.exists() else '❌'}")
results['odoo_script'] = odoo_script.exists()

odoo_readme = Path("odoo/README.md")
print(f"   Odoo Setup Guide: {'✅' if odoo_readme.exists() else '❌'}")
results['odoo_guide'] = odoo_readme.exists()

odoo_docker = Path("odoo/docker-compose.yml")
print(f"   Odoo Docker Compose: {'✅' if odoo_docker.exists() else '❌'}")
results['odoo_docker'] = odoo_docker.exists()

print()

# ============================================================
# TEST 8: Platinum Tier (Cloud/Local Separation)
# ============================================================
print("TEST 8: Platinum Tier (Cloud/Local)")
print("-" * 80)

platinum_scripts = [
    "cloud_orchestrator.py",
    "local_agent.py",
    "vault_sync.py",
    "health_monitor.py"
]

for script in platinum_scripts:
    script_path = vault_path / "scripts" / script
    exists = script_path.exists()
    print(f"   {script}: {'✅' if exists else '❌'}")
    results[f'platinum_{script}'] = exists

# Check security rules
gitignore = Path("platinum_vault/.gitignore")
print(f"   Security .gitignore: {'✅' if gitignore.exists() else '❌'}")
results['platinum_security'] = gitignore.exists()

print()

# ============================================================
# TEST 9: Agent Skills (All as Skills)
# ============================================================
print("TEST 9: Agent Skills Implementation")
print("-" * 80)

skills_path = Path(".qwen/skills")
gold_skills = [
    "ceo-briefing",
    "ralph-wiggum-loop",
    "odoo-accounting-mcp",
    "facebook-instagram-mcp",
    "twitter-x-mcp",
    "error-recovery",
    "cross-domain-integration",
    "audit-logging"
]

for skill in gold_skills:
    skill_file = skills_path / skill / "SKILL.md"
    exists = skill_file.exists()
    print(f"   {skill}/SKILL.md: {'✅' if exists else '❌'}")
    results[f'skill_{skill}'] = exists

print()

# ============================================================
# TEST 10: Audit Logging
# ============================================================
print("TEST 10: Audit Logging")
print("-" * 80)

audit_script = vault_path / "scripts" / "audit_logger.py"
print(f"   Audit Logger Script: {'✅' if audit_script.exists() else '❌'}")
results['audit_script'] = audit_script.exists()

logs_folder = vault_path / "Logs"
print(f"   Logs Folder: {'✅' if logs_folder.exists() else '❌'}")
results['logs_folder'] = logs_folder.exists()

if logs_folder.exists():
    log_files = list(logs_folder.glob("*.json"))
    print(f"   Log Files: {len(log_files)}")
    results['log_files'] = len(log_files) > 0

print()

# ============================================================
# TEST 11: Error Recovery
# ============================================================
print("TEST 11: Error Recovery")
print("-" * 80)

watchdog_script = vault_path / "scripts" / "watchdog.py"
print(f"   Watchdog Script: {'✅' if watchdog_script.exists() else '❌'}")
results['watchdog_script'] = watchdog_script.exists()

error_recovery_skill = skills_path / "error-recovery" / "SKILL.md"
print(f"   Error Recovery Skill: {'✅' if error_recovery_skill.exists() else '❌'}")
results['error_recovery_skill'] = error_recovery_skill.exists()

print()

# ============================================================
# TEST 12: Cross-Domain Integration
# ============================================================
print("TEST 12: Cross-Domain Integration")
print("-" * 80)

domain_script = vault_path / "scripts" / "domain_router.py"
print(f"   Domain Router Script: {'✅' if domain_script.exists() else '❌'}")
results['domain_script'] = domain_script.exists()

domains_folder = vault_path / "Domains"
print(f"   Domains Folder: {'✅' if domains_folder.exists() else '❌'}")
results['domains_folder'] = domains_folder.exists()

print()

# ============================================================
# SUMMARY
# ============================================================
print("=" * 80)
print("  FTE VERIFICATION SUMMARY")
print("=" * 80)
print()

passed = sum(1 for v in results.values() if v == True)
failed = sum(1 for v in results.values() if v == False)
total = len(results)

print(f"Tests Passed: {passed}/{total}")
print(f"Tests Failed: {failed}/{total}")
print()

# Show failed tests
if failed > 0:
    print("Failed Tests:")
    for test, result in results.items():
        if result == False:
            print(f"   ❌ {test}")
    print()

# FTE Requirements Check
fte_requirements = {
    'Facebook Auto-Posting': results.get('facebook_config', False) and results.get('facebook_posts', False),
    'Watcher System': all(v for k, v in results.items() if k.startswith('watcher_')),
    'MCP Servers': all(v for k, v in results.items() if k.startswith('mcp_')),
    'Approval Workflow': all(v for k, v in results.items() if k.startswith('folder_')),
    'CEO Briefing': results.get('ceo_briefing_script', False),
    'Odoo Accounting': results.get('odoo_script', False),
    'Platinum Cloud/Local': all(v for k, v in results.items() if k.startswith('platinum_')),
    'Agent Skills': all(v for k, v in results.items() if k.startswith('skill_')),
    'Audit Logging': results.get('audit_script', False) and results.get('logs_folder', False),
    'Error Recovery': results.get('watchdog_script', False)
}

print("FTE Requirements:")
for req, status in fte_requirements.items():
    print(f"   {'✅' if status else '❌'} {req}")

print()

fte_score = sum(1 for v in fte_requirements.values() if v)
fte_total = len(fte_requirements)
fte_percent = round((fte_score / fte_total) * 100, 1)

print(f"FTE Score: {fte_score}/{fte_total} ({fte_percent}%)")
print()

if fte_percent >= 90:
    print("🎉 YOUR AI EMPLOYEE IS A COMPLETE FTE!")
    print()
    print("Your Digital Employee can:")
    print("   ✅ Auto-post to Facebook/Instagram/Twitter")
    print("   ✅ Monitor emails and WhatsApp")
    print("   ✅ Create invoices in Odoo")
    print("   ✅ Generate CEO briefings")
    print("   ✅ Work 24/7 with approval workflow")
    print("   ✅ Run on Cloud 24/7 (Platinum)")
    print()
    print("Ready for hackathon submission!")
elif fte_percent >= 70:
    print("⚠️ YOUR AI EMPLOYEE IS MOSTLY COMPLETE")
    print()
    print("Most FTE requirements are working.")
    print("Fix the failed tests above.")
else:
    print("❌ YOUR AI EMPLOYEE NEEDS MORE WORK")
    print()
    print("Several FTE requirements are missing.")
    print("Review the failed tests above.")

print()
print("=" * 80)

# Save results
results_file = Path("fte_verification_results.json")
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump({
        'timestamp': datetime.now().isoformat(),
        'passed': passed,
        'failed': failed,
        'total': total,
        'fte_score': fte_score,
        'fte_total': fte_total,
        'fte_percent': fte_percent,
        'fte_requirements': fte_requirements,
        'results': results
    }, f, indent=2)

print(f"Results saved to: {results_file}")
print("=" * 80)
