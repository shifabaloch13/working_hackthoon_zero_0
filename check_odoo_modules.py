#!/usr/bin/env python3
"""
Check Installed Odoo Modules
"""

import requests
import json

print("=" * 70)
print("  CHECKING INSTALLED ODOO MODULES")
print("=" * 70)
print()

ODOO_URL = 'http://localhost:8069'

# Try to access Odoo modules page
print("Checking Odoo modules...")
print()

# Open Odoo apps page
import webbrowser
webbrowser.open(f'{ODOO_URL}/web#action=base.modules')

print("✅ Odoo Apps page opened in browser!")
print()
print("📋 INSTRUCTIONS:")
print()
print("1. In the Apps page, look at the top menu")
print("2. Click on 'Apps' dropdown (if visible)")
print("3. Look for 'My Apps' or 'Installed Apps'")
print("4. You should see Accounting/Invoicing listed")
print("5. Click on the app name (NOT on 'Upgrade')")
print()
print("💡 ALTERNATIVE:")
print()
print("Go to main dashboard:")
print(f"  {ODOO_URL}/web")
print()
print("Look for Accounting icon on the dashboard")
print("Click on the icon (not on 'Upgrade')")
print()
print("=" * 70)
print()
