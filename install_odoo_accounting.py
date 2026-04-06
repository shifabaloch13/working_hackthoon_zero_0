#!/usr/bin/env python3
"""
Install Odoo Accounting Module

This script helps you install the Accounting module in Odoo.
"""

import requests
import webbrowser

print("=" * 70)
print("  ODOO ACCOUNTING MODULE INSTALLATION")
print("=" * 70)
print()

# Odoo Configuration
ODOO_URL = 'http://localhost:8069'
ODOO_USERNAME = 'admin@example.com'
ODOO_PASSWORD = 'Admin@123'

print("📋 INSTALLATION STEPS:")
print()
print("Step 1: Open Odoo Apps")
print(f"  URL: {ODOO_URL}/web#action=base.modules")
print()
print("Step 2: Search for 'Accounting'")
print()
print("Step 3: Click 'Install' on the Accounting app")
print()
print("Step 4: Wait 2-3 minutes for installation")
print()
print("Step 5: Click on Accounting app to access interface")
print()
print("=" * 70)
print()

# Open Odoo Apps in browser
print("🌐 Opening Odoo Apps in your browser...")
webbrowser.open(f'{ODOO_URL}/web#action=base.modules')

print()
print("✅ Browser opened!")
print()
print("📝 INSTRUCTIONS:")
print()
print("1. In the Apps page, use the search box at the top")
print("2. Type: Accounting")
print("3. Look for 'Accounting' by Odoo")
print("4. Click the [INSTALL] button")
print("5. Wait for installation to complete")
print("6. After installation, click on Accounting app")
print()
print("💡 ALTERNATIVE: Install 'Invoicing' (simpler version)")
print("   Search for: Invoicing")
print("   Click [INSTALL]")
print()
print("=" * 70)
print()
print("Need help? Let me know what you see!")
print()
