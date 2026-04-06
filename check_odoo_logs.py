"""Check Odoo logs"""
import subprocess

result = subprocess.run(['docker', 'logs', 'odoo_community_19'], capture_output=True, text=True)
lines = result.stdout.split('\n')
print("Last 50 lines of Odoo logs:")
print("=" * 60)
for line in lines[-50:]:
    print(line)
print("=" * 60)
