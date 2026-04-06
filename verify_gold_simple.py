"""Gold Tier Verification - Simple"""
from dotenv import load_dotenv
import os
from pathlib import Path

print("=" * 70)
print("  GOLD TIER VERIFICATION")
print("=" * 70)
print()

load_dotenv()

# Check Facebook
print("1. Facebook Configuration")
fb_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
fb_page_id = os.getenv('FACEBOOK_PAGE_ID')
print(f"   Token: {'✅' if fb_token else '❌'}")
print(f"   Page ID: {'✅' if fb_page_id else '❌'}")
print()

# Check Scripts
print("2. Gold Tier Scripts")
scripts = [
    "facebook_poster.py",
    "facebook_comment_watcher.py",
    "twitter_poster.py",
    "ceo_briefing.py",
    "audit_logger.py",
    "ralph_wiggum.py",
    "watchdog.py",
    "domain_router.py",
    "subscription_audit.py"
]

vault = Path("AI_Employee_Vault/scripts")
for script in scripts:
    exists = (vault / script).exists()
    print(f"   {script}: {'✅' if exists else '❌'}")
print()

# Check Odoo Script
print("3. Odoo MCP Script")
odoo_script = Path("odoo/scripts/odoo_mcp_server.py")
print(f"   odoo_mcp_server.py: {'✅' if odoo_script.exists() else '❌'}")
print()

# Check Docker
print("4. Docker Containers")
import subprocess
result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
print(f"   Odoo: {'✅' if 'odoo' in result.stdout else '❌'}")
print(f"   PostgreSQL: {'✅' if 'postgres' in result.stdout else '❌'}")
print()

# Check Folders
print("5. Folder Structure")
folders = ['Needs_Action', 'Pending_Approval', 'Approved', 'Done', 'Logs']
vault = Path("AI_Employee_Vault")
for folder in folders:
    exists = (vault / folder).exists()
    print(f"   {folder}/: {'✅' if exists else '❌'}")
print()

# Check Skills
print("6. Gold Tier Skills")
skills = [
    "ceo-briefing",
    "ralph-wiggum-loop",
    "odoo-accounting-mcp",
    "facebook-instagram-mcp",
    "twitter-x-mcp",
    "error-recovery",
    "cross-domain-integration",
    "audit-logging"
]

skills_path = Path(".qwen/skills")
for skill in skills:
    exists = (skills_path / skill / "SKILL.md").exists()
    print(f"   {skill}: {'✅' if exists else '❌'}")
print()

print("=" * 70)
print("  VERIFICATION COMPLETE")
print("=" * 70)
