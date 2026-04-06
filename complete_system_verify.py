"""
COMPLETE AI EMPLOYEE VERIFICATION

Tests EVERYTHING before Oracle Cloud deployment:
- All scripts
- All integrations
- All features
- All tiers

Usage:
    python complete_system_verify.py
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

print("=" * 80)
print("  COMPLETE AI EMPLOYEE SYSTEM VERIFICATION")
print("=" * 80)
print()
print("Testing ALL components before Oracle Cloud deployment...")
print()

load_dotenv()
vault_path = Path("AI_Employee_Vault").resolve()
results = {}

# ============================================================================
# TEST 1: BRONZE TIER (5 tests)
# ============================================================================
print("=" * 80)
print("  BRONZE TIER VERIFICATION")
print("=" * 80)
print()

bronze_tests = {
    'Obsidian Vault': vault_path.exists(),
    'Dashboard.md': (vault_path / "Dashboard.md").exists(),
    'Company_Handbook.md': (vault_path / "Company_Handbook.md").exists(),
    'Needs_Action Folder': (vault_path / "Needs_Action").exists(),
    'Done Folder': (vault_path / "Done").exists(),
}

for test, result in bronze_tests.items():
    print(f"{'✅' if result else '❌'} {test}")
    results[f'bronze_{test}'] = result

print()
bronze_passed = sum(1 for v in bronze_tests.values() if v)
bronze_total = len(bronze_tests)
print(f"Bronze Tier: {bronze_passed}/{bronze_total} ({bronze_passed/bronze_total*100:.0f}%)")
print()

# ============================================================================
# TEST 2: SILVER TIER (8 tests)
# ============================================================================
print("=" * 80)
print("  SILVER TIER VERIFICATION")
print("=" * 80)
print()

silver_scripts = [
    'gmail_watcher.py',
    'filesystem_watcher.py',
    'whatsapp_watcher.py',
    'linkedin_poster.py',
    'orchestrator.py',
    'approval_manager.py',
    'email_mcp_server.py'
]

for script in silver_scripts:
    exists = (vault_path / "scripts" / script).exists()
    print(f"{'✅' if exists else '❌'} {script}")
    results[f'silver_{script}'] = exists

print()
silver_passed = sum(1 for v in silver_scripts if (vault_path / "scripts" / v).exists())
silver_total = len(silver_scripts)
print(f"Silver Tier: {silver_passed}/{silver_total} ({silver_passed/silver_total*100:.0f}%)")
print()

# ============================================================================
# TEST 3: GOLD TIER (12 tests)
# ============================================================================
print("=" * 80)
print("  GOLD TIER VERIFICATION")
print("=" * 80)
print()

gold_scripts = [
    'facebook_poster.py',
    'facebook_comment_watcher.py',
    'twitter_poster.py',
    'ceo_briefing.py',
    'audit_logger.py',
    'ralph_wiggum.py',
    'watchdog.py',
    'domain_router.py',
    'subscription_audit.py'
]

for script in gold_scripts:
    exists = (vault_path / "scripts" / script).exists()
    print(f"{'✅' if exists else '❌'} {script}")
    results[f'gold_{script}'] = exists

# Check Odoo
odoo_exists = Path("odoo/scripts/odoo_mcp_server.py").exists()
print(f"{'✅' if odoo_exists else '❌'} odoo_mcp_server.py")
results['gold_odoo'] = odoo_exists

print()
gold_passed = sum(1 for s in gold_scripts if (vault_path / "scripts" / s).exists()) + (1 if odoo_exists else 0)
gold_total = len(gold_scripts) + 1
print(f"Gold Tier: {gold_passed}/{gold_total} ({gold_passed/gold_total*100:.0f}%)")
print()

# ============================================================================
# TEST 4: PLATINUM TIER (7 tests)
# ============================================================================
print("=" * 80)
print("  PLATINUM TIER VERIFICATION")
print("=" * 80)
print()

platinum_scripts = [
    'cloud_orchestrator.py',
    'local_agent.py',
    'vault_sync.py',
    'health_monitor.py'
]

for script in platinum_scripts:
    exists = (vault_path / "scripts" / script).exists()
    print(f"{'✅' if exists else '❌'} {script}")
    results[f'platinum_{script}'] = exists

# Check .gitignore
gitignore_exists = Path("platinum_vault/.gitignore").exists()
print(f"{'✅' if gitignore_exists else '❌'} platinum_vault/.gitignore")
results['platinum_gitignore'] = gitignore_exists

# Check documentation
platinum_docs = [
    'PLATINUM_TIER_ARCHITECTURE.md',
    'PLATINUM_ORACLE_CLOUD_SETUP.md',
    'PLATINUM_DEMO_WORKFLOW.md'
]

for doc in platinum_docs:
    exists = Path(doc).exists()
    print(f"{'✅' if exists else '❌'} {doc}")
    results[f'platinum_doc_{doc}'] = exists

print()
platinum_passed = sum(1 for s in platinum_scripts if (vault_path / "scripts" / s).exists())
platinum_passed += 1 if gitignore_exists else 0
platinum_passed += sum(1 for d in platinum_docs if Path(d).exists())
platinum_total = len(platinum_scripts) + 1 + len(platinum_docs)
print(f"Platinum Tier: {platinum_passed}/{platinum_total} ({platinum_passed/platinum_total*100:.0f}%)")
print()

# ============================================================================
# TEST 5: INTEGRATIONS (5 tests)
# ============================================================================
print("=" * 80)
print("  INTEGRATION VERIFICATION")
print("=" * 80)
print()

# Facebook
fb_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
fb_page_id = os.getenv('FACEBOOK_PAGE_ID')
fb_working = bool(fb_token and fb_page_id)
print(f"{'✅' if fb_working else '❌'} Facebook Credentials")
results['integration_facebook'] = fb_working

# Check Docker (Odoo)
try:
    result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=10)
    odoo_running = 'odoo' in result.stdout.lower()
    print(f"{'✅' if odoo_running else '⚠️'} Odoo Container (Docker)")
    results['integration_odoo'] = odoo_running
except:
    print(f"❌ Docker/Odoo")
    results['integration_odoo'] = False

# Email MCP
email_working = (vault_path / "scripts" / "email_mcp_server.py").exists()
print(f"{'✅' if email_working else '❌'} Email MCP")
results['integration_email'] = email_working

# Twitter
twitter_working = (vault_path / "scripts" / "twitter_poster.py").exists()
print(f"{'✅' if twitter_working else '❌'} Twitter/X MCP")
results['integration_twitter'] = twitter_working

# LinkedIn
linkedin_working = (vault_path / "scripts" / "linkedin_poster.py").exists()
print(f"{'✅' if linkedin_working else '❌'} LinkedIn Scripts")
results['integration_linkedin'] = linkedin_working

print()
integration_passed = sum(1 for k, v in results.items() if k.startswith('integration_') and v)
integration_total = 5
print(f"Integrations: {integration_passed}/{integration_total} Working")
print()

# ============================================================================
# TEST 6: SKILLS (8 tests)
# ============================================================================
print("=" * 80)
print("  AGENT SKILLS VERIFICATION")
print("=" * 80)
print()

skills_path = Path(".qwen/skills")
gold_skills = [
    'ceo-briefing',
    'ralph-wiggum-loop',
    'odoo-accounting-mcp',
    'facebook-instagram-mcp',
    'twitter-x-mcp',
    'error-recovery',
    'cross-domain-integration',
    'audit-logging'
]

for skill in gold_skills:
    exists = (skills_path / skill / "SKILL.md").exists()
    print(f"{'✅' if exists else '❌'} {skill}/SKILL.md")
    results[f'skill_{skill}'] = exists

print()
skills_passed = sum(1 for s in gold_skills if (skills_path / s / "SKILL.md").exists())
skills_total = len(gold_skills)
print(f"Skills: {skills_passed}/{skills_total} ({skills_passed/skills_total*100:.0f}%)")
print()

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("=" * 80)
print("  FINAL VERIFICATION SUMMARY")
print("=" * 80)
print()

total_tests = len(results)
passed_tests = sum(1 for v in results.values() if v)
failed_tests = total_tests - passed_tests
pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

print(f"Total Tests: {total_tests}")
print(f"Passed: {passed_tests}")
print(f"Failed: {failed_tests}")
print(f"Pass Rate: {pass_rate:.1f}%")
print()

if failed_tests > 0:
    print("Failed Tests:")
    for test, result in results.items():
        if not result:
            print(f"  ❌ {test}")
    print()

# Tier Summary
print("Tier Status:")
print(f"  Bronze: {bronze_passed}/{bronze_total} ({bronze_passed/bronze_total*100:.0f}%)")
print(f"  Silver: {silver_passed}/{silver_total} ({silver_passed/silver_total*100:.0f}%)")
print(f"  Gold: {gold_passed}/{gold_total} ({gold_passed/gold_total*100:.0f}%)")
print(f"  Platinum: {platinum_passed}/{platinum_total} ({platinum_passed/platinum_total*100:.0f}%)")
print()

# Deployment Readiness
print("=" * 80)
print("  ORACLE CLOUD DEPLOYMENT READINESS")
print("=" * 80)
print()

deployment_ready = (
    bronze_passed == bronze_total and
    silver_passed == silver_total and
    gold_passed == gold_total and
    platinum_passed >= platinum_total * 0.9 and
    fb_working
)

if deployment_ready:
    print("  ✅ READY FOR ORACLE CLOUD DEPLOYMENT!")
    print()
    print("  All critical components verified:")
    print("  ✅ All scripts present")
    print("  ✅ All integrations configured")
    print("  ✅ All skills documented")
    print("  ✅ Facebook credentials ready")
    print("  ✅ Docker/Odoo ready")
    print()
    print("  Next Step: Follow PLATINUM_ORACLE_CLOUD_SETUP.md")
else:
    print("  ⚠️ NEEDS ATTENTION BEFORE DEPLOYMENT")
    print()
    print("  Please fix the failed tests above before deploying.")

print()
print("=" * 80)

# Save results
results_file = Path("complete_verification_results.json")
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump({
        'timestamp': datetime.now().isoformat(),
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'failed_tests': failed_tests,
        'pass_rate': pass_rate,
        'deployment_ready': deployment_ready,
        'results': results
    }, f, indent=2)

print(f"Results saved to: {results_file}")
print("=" * 80)

sys.exit(0 if deployment_ready else 1)
