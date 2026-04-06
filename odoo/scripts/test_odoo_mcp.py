"""
Test Script for Odoo MCP Server - Gold Tier

Tests all Odoo MCP functionality:
- Invoice creation
- Payment recording
- Financial reporting
- Partner sync
- Approval workflow

Usage:
    python test_odoo_mcp.py "../AI_Employee_Vault"
"""

import sys
import json
from pathlib import Path
from datetime import datetime


def test_odoo_mcp(vault_path: str):
    """Test all Odoo MCP functions."""
    
    print('=' * 70)
    print('  ODOO MCP SERVER - TEST SUITE')
    print('=' * 70)
    print()
    
    # Import the MCP class
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from odoo_mcp_server import OdooMCP
        print('[OK] OdooMCP module imported')
    except ImportError as e:
        print(f'[ERROR] Failed to import OdooMCP: {e}')
        return False
    
    # Initialize MCP
    print()
    print('Initializing Odoo MCP...')
    odoo = OdooMCP(vault_path)
    print(f'[OK] Odoo MCP initialized')
    print(f'     Vault: {odoo.vault}')
    print(f'     Config: {odoo.config_path}')
    print()
    
    # Test results
    results = {
        'test_create_invoice_draft': False,
        'test_record_payment': False,
        'test_financial_report': False,
        'test_sync_partners': False,
        'test_process_approved': False
    }
    
    # Test 1: Create Invoice Draft
    print('-' * 70)
    print('TEST 1: Create Invoice Draft')
    print('-' * 70)
    try:
        draft_file = odoo.create_invoice_draft(
            partner_name='Test Client LLC',
            amount=2500.00,
            description='Testing Services - March 2026',
            invoice_type='out_invoice'
        )
        
        if draft_file.exists():
            print(f'[PASS] Invoice draft created: {draft_file.name}')
            results['test_create_invoice_draft'] = True
            
            # Show draft content
            print()
            print('Draft Content Preview:')
            content = draft_file.read_text()
            for line in content.split('\n')[:15]:
                print(f'  {line}')
        else:
            print(f'[FAIL] Invoice draft file not created')
    except Exception as e:
        print(f'[FAIL] Error creating invoice draft: {e}')
    
    print()
    
    # Test 2: Financial Report
    print('-' * 70)
    print('TEST 2: Financial Report (Receivables)')
    print('-' * 70)
    try:
        report = odoo.get_financial_report(report_type='receivables')
        
        if report.get('success'):
            print(f'[PASS] Financial report generated')
            print(f'     Simulated: {report.get("simulated", False)}')
            if report.get('data'):
                data = report['data']
                if 'total_receivables' in data:
                    print(f'     Total Receivables: ${data["total_receivables"]:.2f}')
                if 'count' in data:
                    print(f'     Invoice Count: {data["count"]}')
            results['test_financial_report'] = True
        else:
            print(f'[FAIL] Financial report failed: {report.get("error")}')
    except Exception as e:
        print(f'[FAIL] Error generating report: {e}')
    
    print()
    
    # Test 3: Sync Partners
    print('-' * 70)
    print('TEST 3: Sync Partners')
    print('-' * 70)
    try:
        sync_result = odoo.sync_partners()
        
        if sync_result.get('success'):
            print(f'[PASS] Partners synced')
            print(f'     Simulated: {sync_result.get("simulated", False)}')
            print(f'     Partner Count: {sync_result.get("count", 0)}')
            
            # Check if Partners.md was created
            partners_file = odoo.accounting_folder / 'Partners.md'
            if partners_file.exists():
                print(f'[OK] Partners file created: {partners_file}')
            results['test_sync_partners'] = True
        else:
            print(f'[FAIL] Partner sync failed: {sync_result.get("error")}')
    except Exception as e:
        print(f'[FAIL] Error syncing partners: {e}')
    
    print()
    
    # Test 4: Record Payment (Simulated)
    print('-' * 70)
    print('TEST 4: Record Payment')
    print('-' * 70)
    try:
        payment_result = odoo.record_payment(
            invoice_id=123,
            amount=1500.00,
            payment_date=datetime.now().strftime('%Y-%m-%d'),
            payment_reference='Test Payment #001'
        )
        
        if payment_result.get('success'):
            print(f'[PASS] Payment recorded')
            print(f'     Simulated: {payment_result.get("simulated", False)}')
            print(f'     Invoice ID: {payment_result.get("invoice_id")}')
            print(f'     Amount: ${payment_result.get("amount", 0):.2f}')
            results['test_record_payment'] = True
        else:
            print(f'[FAIL] Payment recording failed: {payment_result.get("error")}')
    except Exception as e:
        print(f'[FAIL] Error recording payment: {e}')
    
    print()
    
    # Test 5: Process Approved Invoices
    print('-' * 70)
    print('TEST 5: Process Approved Invoices')
    print('-' * 70)
    try:
        # First create a test approved invoice
        draft_file = odoo.create_invoice_draft(
            partner_name='Approved Test Client',
            amount=999.00,
            description='Auto-test Invoice'
        )
        
        # Move to approved
        approved_file = odoo.approved / draft_file.name
        draft_file.rename(approved_file)
        print(f'[INFO] Created test approved invoice: {approved_file.name}')
        
        # Process approved
        processed = odoo.process_approved_invoices()
        
        print(f'[PASS] Processed {processed} approved invoice(s)')
        results['test_process_approved'] = True
    except Exception as e:
        print(f'[FAIL] Error processing approved invoices: {e}')
    
    print()
    
    # Summary
    print('=' * 70)
    print('  TEST SUMMARY')
    print('=' * 70)
    print()
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = '[PASS]' if result else '[FAIL]'
        print(f'  {status} - {test_name}')
    
    print()
    print(f'Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)')
    print()
    
    if passed == total:
        print('[SUCCESS] ALL TESTS PASSED! Odoo MCP is working correctly.')
        return True
    else:
        print('[WARNING] Some tests failed. Check the output above for details.')
        return False


def main():
    if len(sys.argv) < 2:
        print('Usage: python test_odoo_mcp.py <vault_path>')
        print()
        print('Example:')
        print('  python test_odoo_mcp.py "../AI_Employee_Vault"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    success = test_odoo_mcp(vault_path)
    
    print()
    print('=' * 70)
    print('  NEXT STEPS')
    print('=' * 70)
    print()
    print('1. Start Odoo with Docker Compose:')
    print('   cd odoo')
    print('   docker-compose up -d')
    print()
    print('2. Configure Odoo:')
    print('   - Open http://localhost:8069')
    print('   - Create database and install Accounting module')
    print('   - Create odoo_config.json with credentials')
    print()
    print('3. Run tests again with real Odoo connection')
    print()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
