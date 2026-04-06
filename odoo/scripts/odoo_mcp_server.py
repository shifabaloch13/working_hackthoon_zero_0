"""
Odoo Accounting MCP Server - Gold Tier Implementation

Integrates with Odoo Community 19 via JSON-RPC API for:
- Invoice creation
- Payment recording
- Financial reporting
- Partner management
- Account reconciliation

Prerequisites:
    - Odoo Community 19 running (see ../docker-compose.yml)
    - requests library: pip install requests
    - Odoo database with Accounting module installed

Usage:
    python odoo_mcp_server.py "D:/path/to/vault" --create-invoice --partner "Client Name" --amount 1500
    python odoo_mcp_server.py "D:/path/to/vault" --record-payment --invoice-id 123 --amount 1500
    python odoo_mcp_server.py "D:/path/to/vault" --report --type receivables
    python odoo_mcp_server.py "D:/path/to/vault" --sync-partners
"""

import sys
import json
import hashlib
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
import uuid

# Try to import requests (optional - for actual Odoo connection)
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print('[WARN] requests library not installed. Odoo integration will be simulated.')
    print('[INFO] Install with: pip install requests')


class OdooMCP:
    """Odoo Accounting MCP Server for AI Employee."""

    def __init__(self, vault_path: str, config_path: str = None):
        self.vault = Path(vault_path).resolve()
        self.config_path = Path(config_path) if config_path else self.vault.parent / 'odoo_config.json'
        self.pending_approval = self.vault / 'Pending_Approval'
        self.approved = self.vault / 'Approved'
        self.done = self.vault / 'Done'
        self.logs_folder = self.vault / 'Logs'
        self.accounting_folder = self.vault / 'Accounting'

        for folder in [self.pending_approval, self.approved, self.done, self.logs_folder, self.accounting_folder]:
            folder.mkdir(parents=True, exist_ok=True)

        # Load config
        self.config = self._load_config()
        self.session = self._create_session() if REQUESTS_AVAILABLE else None

    def _load_config(self) -> dict:
        """Load Odoo API config."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        # Return dummy config for simulation
        return {
            'odoo_url': 'http://localhost:8069',
            'database': 'ai_employee_db',
            'username': 'admin',
            'password': 'admin_password',
            'api_key': None
        }

    def _create_session(self) -> Optional[requests.Session]:
        """Create Odoo JSON-RPC session."""
        if not REQUESTS_AVAILABLE:
            return None

        try:
            session = requests.Session()
            odoo_url = self.config.get('odoo_url', 'http://localhost:8069')
            
            # Authenticate with Odoo
            auth_payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "service": "common",
                    "method": "authenticate",
                    "args": [
                        self.config.get('database'),
                        self.config.get('username'),
                        self.config.get('password'),
                        {}
                    ]
                },
                "id": str(uuid.uuid4())
            }
            
            response = session.post(f"{odoo_url}/web/dataset/call", json=auth_payload, timeout=10)
            result = response.json()
            
            if 'result' in result:
                self.uid = result['result']
                print(f'[OK] Connected to Odoo as user ID: {self.uid}')
                return session
            else:
                print(f'[WARN] Odoo authentication failed: {result}')
                print('[INFO] Running in simulation mode')
                return None
                
        except Exception as e:
            print(f'[WARN] Could not connect to Odoo: {e}')
            print('[INFO] Running in simulation mode')
            return None

    def _json_rpc_call(self, service: str, method: str, args: list = None) -> dict:
        """Make JSON-RPC call to Odoo."""
        if not self.session:
            return {'success': False, 'simulated': True}

        odoo_url = self.config.get('odoo_url', 'http://localhost:8069')
        
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": service,
                "method": method,
                "args": args or []
            },
            "id": str(uuid.uuid4())
        }

        try:
            response = self.session.post(f"{odoo_url}/web/dataset/call", json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result.get('result', {})
        except Exception as e:
            print(f'[ERROR] Odoo JSON-RPC call failed: {e}')
            return {'success': False, 'error': str(e)}

    def _execute_model(self, model: str, method: str, args: list = None, kwargs: dict = None) -> dict:
        """Execute model method in Odoo."""
        if not self.session:
            return {'success': False, 'simulated': True}

        odoo_url = self.config.get('odoo_url', 'http://localhost:8069')
        
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": model,
                "method": method,
                "args": args or [],
                "kwargs": kwargs or {}
            },
            "id": str(uuid.uuid4())
        }

        try:
            response = self.session.post(f"{odoo_url}/web/dataset/call_kw", json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result.get('result', {})
        except Exception as e:
            print(f'[ERROR] Odoo model execution failed: {e}')
            return {'success': False, 'error': str(e)}

    def create_invoice_draft(self, partner_name: str, amount: float, 
                            description: str = 'Services', 
                            invoice_type: str = 'out_invoice') -> Path:
        """Create an invoice draft for approval."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'ODOO_INVOICE_{timestamp}.md'
        draft_file = self.pending_approval / filename

        content = f"""---
type: odoo_invoice_request
partner: {partner_name}
amount: {amount:.2f}
description: {description}
invoice_type: {invoice_type}
created: {datetime.now().isoformat()}
status: pending
---

# Odoo Invoice Draft

## Invoice Details
- **Customer**: {partner_name}
- **Amount**: ${amount:.2f}
- **Description**: {description}
- **Type**: {'Customer Invoice' if invoice_type == 'out_invoice' else 'Vendor Bill'}

## To Approve
Move this file to `/Approved` folder to create invoice in Odoo.

## To Reject
Move this file to `/Rejected` folder with reason.

---
*Created by AI Employee Odoo MCP*
"""
        draft_file.write_text(content, encoding='utf-8')
        print(f'[OK] Invoice draft created: {draft_file.name}')
        return draft_file

    def create_invoice(self, partner_name: str, amount: float, 
                      description: str = 'Services',
                      invoice_type: str = 'out_invoice') -> dict:
        """Create invoice in Odoo."""

        print(f'[INFO] Creating invoice for {partner_name}: ${amount:.2f}')

        # Simulation mode
        if not self.session:
            print('[INFO] Simulation mode - invoice not actually created in Odoo')
            print('[INFO] To enable real integration, ensure Odoo is running and configured')

            # Simulate invoice creation
            invoice_id = int(hashlib.md5(f"{partner_name}{datetime.now()}".encode()).hexdigest()[:8], 16) % 10000
            
            return {
                'success': True,
                'simulated': True,
                'invoice_id': invoice_id,
                'partner': partner_name,
                'amount': amount,
                'description': description,
                'invoice_type': invoice_type,
                'timestamp': datetime.now().isoformat()
            }

        # Real Odoo invoice creation
        try:
            # First, find or create the partner
            partner_id = self._find_or_create_partner(partner_name)
            
            # Create invoice
            invoice_vals = {
                'move_type': invoice_type,
                'partner_id': partner_id,
                'invoice_origin': f'AI Employee - {description}',
                'invoice_line_ids': [(0, 0, {
                    'name': description,
                    'quantity': 1,
                    'price_unit': amount,
                })]
            }

            result = self._execute_model('account.move', 'create', [invoice_vals])
            
            if result and not isinstance(result, dict):
                invoice_id = result
                print(f'[OK] Invoice created in Odoo! ID: {invoice_id}')
                
                return {
                    'success': True,
                    'simulated': False,
                    'invoice_id': invoice_id,
                    'partner': partner_name,
                    'amount': amount,
                    'description': description,
                    'invoice_type': invoice_type,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                raise Exception(f'Unexpected result from Odoo: {result}')
                
        except Exception as e:
            print(f'[ERROR] Failed to create invoice in Odoo: {e}')
            return {'success': False, 'error': str(e)}

    def _find_or_create_partner(self, partner_name: str) -> int:
        """Find existing partner or create new one."""
        # Search for existing partner
        partner_ids = self._execute_model(
            'res.partner', 
            'search', 
            [[('name', '=', partner_name)]]
        )
        
        if partner_ids and len(partner_ids) > 0:
            print(f'[INFO] Found existing partner: {partner_name} (ID: {partner_ids[0]})')
            return partner_ids[0]
        
        # Create new partner
        print(f'[INFO] Creating new partner: {partner_name}')
        partner_id = self._execute_model(
            'res.partner',
            'create',
            [{'name': partner_name}]
        )
        return partner_id if partner_id else 1

    def record_payment(self, invoice_id: int, amount: float, 
                      payment_date: str = None,
                      payment_reference: str = None) -> dict:
        """Record payment for an invoice in Odoo."""

        if not payment_date:
            payment_date = datetime.now().strftime('%Y-%m-%d')

        print(f'[INFO] Recording payment for invoice {invoice_id}: ${amount:.2f}')

        # Simulation mode
        if not self.session:
            print('[INFO] Simulation mode - payment not actually recorded in Odoo')
            
            return {
                'success': True,
                'simulated': True,
                'invoice_id': invoice_id,
                'amount': amount,
                'payment_date': payment_date,
                'payment_reference': payment_reference or f'PMT-{datetime.now().strftime("%Y%m%d")}',
                'timestamp': datetime.now().isoformat()
            }

        # Real Odoo payment recording
        try:
            # Create payment registration
            payment_vals = {
                'amount': amount,
                'payment_date': payment_date,
                'payment_reference': payment_reference or f'Payment for Invoice {invoice_id}',
                'invoice_ids': [(4, invoice_id)],
            }

            result = self._execute_model('account.payment.register', 'create', [payment_vals])
            
            if result:
                print(f'[OK] Payment recorded in Odoo! Registration ID: {result}')
                
                # Confirm payment
                self._execute_model('account.payment.register', 'action_create_payments', [[result]])
                
                return {
                    'success': True,
                    'simulated': False,
                    'invoice_id': invoice_id,
                    'amount': amount,
                    'payment_date': payment_date,
                    'payment_reference': payment_reference or f'PMT-{datetime.now().strftime("%Y%m%d")}',
                    'registration_id': result,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f'[ERROR] Failed to record payment in Odoo: {e}')
            return {'success': False, 'error': str(e)}

    def get_financial_report(self, report_type: str = 'receivables') -> dict:
        """Get financial report from Odoo."""

        print(f'[INFO] Getting {report_type} report from Odoo')

        # Simulation mode
        if not self.session:
            print('[INFO] Simulation mode - generating sample report')
            
            return {
                'success': True,
                'simulated': True,
                'report_type': report_type,
                'data': {
                    'total_receivables': 5000.00,
                    'total_payables': 2000.00,
                    'outstanding_invoices': 3,
                    'overdue_invoices': 1
                },
                'timestamp': datetime.now().isoformat()
            }

        # Real Odoo report
        try:
            if report_type == 'receivables':
                # Get outstanding invoices
                invoices = self._execute_model(
                    'account.move',
                    'search_read',
                    [[
                        ('move_type', '=', 'out_invoice'),
                        ('payment_state', '!=', 'paid'),
                        ('state', '=', 'posted')
                    ]],
                    {'fields': ['id', 'partner_id', 'amount_total', 'amount_residual', 'invoice_date']}
                )
                
                return {
                    'success': True,
                    'simulated': False,
                    'report_type': report_type,
                    'data': {
                        'invoices': invoices,
                        'total_receivables': sum(inv.get('amount_residual', 0) for inv in invoices),
                        'count': len(invoices)
                    },
                    'timestamp': datetime.now().isoformat()
                }
                
            elif report_type == 'payables':
                # Get outstanding bills
                bills = self._execute_model(
                    'account.move',
                    'search_read',
                    [[
                        ('move_type', 'in', ['in_invoice', 'in_refund']),
                        ('payment_state', '!=', 'paid'),
                        ('state', '=', 'posted')
                    ]],
                    {'fields': ['id', 'partner_id', 'amount_total', 'amount_residual', 'invoice_date']}
                )
                
                return {
                    'success': True,
                    'simulated': False,
                    'report_type': report_type,
                    'data': {
                        'bills': bills,
                        'total_payables': sum(bill.get('amount_residual', 0) for bill in bills),
                        'count': len(bills)
                    },
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f'[ERROR] Failed to get report from Odoo: {e}')
            return {'success': False, 'error': str(e)}

    def sync_partners(self) -> dict:
        """Sync partners/customers from Odoo to vault."""

        print('[INFO] Syncing partners from Odoo')

        # Simulation mode
        if not self.session:
            print('[INFO] Simulation mode - generating sample partners')
            
            partners = [
                {'id': 1, 'name': 'Client A', 'email': 'client.a@example.com'},
                {'id': 2, 'name': 'Client B', 'email': 'client.b@example.com'},
                {'id': 3, 'name': 'Vendor X', 'email': 'vendor.x@example.com'}
            ]
            
            partners_file = self.accounting_folder / 'Partners.md'
            content = '# Partners Synced from Odoo\n\n'
            for p in partners:
                content += f"- {p['name']} (ID: {p['id']}, Email: {p['email']})\n"
            partners_file.write_text(content, encoding='utf-8')
            
            return {
                'success': True,
                'simulated': True,
                'partners': partners,
                'count': len(partners)
            }

        # Real Odoo partner sync
        try:
            partners = self._execute_model(
                'res.partner',
                'search_read',
                [[('customer', '=', True)]],
                {'fields': ['id', 'name', 'email', 'phone', 'street', 'city']}
            )
            
            partners_file = self.accounting_folder / 'Partners.md'
            content = '# Partners Synced from Odoo\n\n'
            content += f'*Synced: {datetime.now().isoformat()}*\n\n'
            
            for p in partners:
                content += f"- **{p.get('name', 'Unknown')}** (ID: {p.get('id')})\n"
                if p.get('email'):
                    content += f"  - Email: {p.get('email')}\n"
                if p.get('phone'):
                    content += f"  - Phone: {p.get('phone')}\n"
                if p.get('city'):
                    content += f"  - Location: {p.get('city')}\n"
            
            partners_file.write_text(content, encoding='utf-8')
            print(f'[OK] Synced {len(partners)} partners to vault')
            
            return {
                'success': True,
                'simulated': False,
                'partners': partners,
                'count': len(partners)
            }
            
        except Exception as e:
            print(f'[ERROR] Failed to sync partners from Odoo: {e}')
            return {'success': False, 'error': str(e)}

    def process_approved_invoices(self) -> int:
        """Process all approved invoices."""
        approved_files = [f for f in self.approved.iterdir()
                         if f.suffix == '.md' and 'ODOO_INVOICE' in f.name]

        if not approved_files:
            print('[INFO] No approved invoices to process')
            return 0

        print(f'[INFO] Found {len(approved_files)} approved invoice(s)')

        processed = 0
        for invoice_file in approved_files:
            print()
            print(f'Processing: {invoice_file.name}')

            # Parse invoice content
            content = invoice_file.read_text(encoding='utf-8')
            invoice_data = self._extract_invoice_data(content)

            if invoice_data:
                result = self.create_invoice(
                    invoice_data['partner'],
                    invoice_data['amount'],
                    invoice_data['description'],
                    invoice_data.get('invoice_type', 'out_invoice')
                )

                if result.get('success'):
                    # Move to Done
                    invoice_file.rename(self.done / invoice_file.name)
                    print(f'[OK] Moved to Done: {invoice_file.name}')

                    # Log the action
                    self._log_action(invoice_file, result)
                    processed += 1
                else:
                    print(f'[ERROR] Failed to create invoice: {invoice_file.name}')

        return processed

    def _extract_invoice_data(self, content: str) -> dict:
        """Extract invoice data from approval file."""
        lines = content.split('\n')

        data = {
            'partner': '',
            'amount': 0.0,
            'description': 'Services',
            'invoice_type': 'out_invoice'
        }

        for line in lines:
            if line.startswith('partner:'):
                data['partner'] = line.split(':')[1].strip()
            elif line.startswith('amount:'):
                data['amount'] = float(line.split(':')[1].strip())
            elif line.startswith('description:'):
                data['description'] = line.split(':')[1].strip()
            elif line.startswith('invoice_type:'):
                data['invoice_type'] = line.split(':')[1].strip()

        return data

    def _log_action(self, filepath: Path, result: dict):
        """Log Odoo action."""
        log_file = self.logs_folder / f'odoo_{datetime.now().strftime("%Y-%m-%d")}.json'

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': 'odoo_invoice',
            'file': filepath.name,
            'result': result
        }

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')


def main():
    if len(sys.argv) < 2:
        print('Usage: python odoo_mcp_server.py <vault_path> [OPTIONS]')
        print()
        print('Options:')
        print('  --create-invoice     Create invoice draft for approval')
        print('    --partner "name"   Partner/customer name')
        print('    --amount <float>   Invoice amount')
        print('    --description "text"  Invoice description')
        print('  --record-payment     Record payment for invoice')
        print('    --invoice-id <int> Odoo invoice ID')
        print('    --amount <float>   Payment amount')
        print('  --report             Get financial report')
        print('    --type <type>      Report type: receivables, payables')
        print('  --sync-partners      Sync partners from Odoo')
        print('  --process-approved   Process all approved invoices')
        print()
        print('Examples:')
        print('  python odoo_mcp_server.py "../AI_Employee_Vault" --create-invoice --partner "Client A" --amount 1500')
        print('  python odoo_mcp_server.py "../AI_Employee_Vault" --record-payment --invoice-id 123 --amount 1500')
        print('  python odoo_mcp_server.py "../AI_Employee_Vault" --report --type receivables')
        sys.exit(1)

    vault_path = sys.argv[1]

    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)

    odoo = OdooMCP(vault_path)

    # Parse options
    if '--create-invoice' in sys.argv:
        # Create invoice draft
        partner = None
        amount = 0.0
        description = 'Services'
        
        if '--partner' in sys.argv:
            idx = sys.argv.index('--partner') + 1
            if idx < len(sys.argv):
                partner = sys.argv[idx]
        
        if '--amount' in sys.argv:
            idx = sys.argv.index('--amount') + 1
            if idx < len(sys.argv):
                amount = float(sys.argv[idx])
        
        if '--description' in sys.argv:
            idx = sys.argv.index('--description') + 1
            if idx < len(sys.argv):
                description = sys.argv[idx]

        if partner and amount > 0:
            odoo.create_invoice_draft(partner, amount, description)
        else:
            print('[ERROR] --partner and --amount are required')

    elif '--record-payment' in sys.argv:
        # Record payment
        invoice_id = None
        amount = 0.0
        
        if '--invoice-id' in sys.argv:
            idx = sys.argv.index('--invoice-id') + 1
            if idx < len(sys.argv):
                invoice_id = int(sys.argv[idx])
        
        if '--amount' in sys.argv:
            idx = sys.argv.index('--amount') + 1
            if idx < len(sys.argv):
                amount = float(sys.argv[idx])

        if invoice_id and amount > 0:
            result = odoo.record_payment(invoice_id, amount)
            print(f'[OK] Payment recorded: {result}')
        else:
            print('[ERROR] --invoice-id and --amount are required')

    elif '--report' in sys.argv:
        # Get financial report
        report_type = 'receivables'
        
        if '--type' in sys.argv:
            idx = sys.argv.index('--type') + 1
            if idx < len(sys.argv):
                report_type = sys.argv[idx]

        result = odoo.get_financial_report(report_type)
        print(f'[OK] Report: {json.dumps(result, indent=2)}')

    elif '--sync-partners' in sys.argv:
        # Sync partners
        result = odoo.sync_partners()
        print(f'[OK] Synced {result.get("count", 0)} partners')

    elif '--process-approved' in sys.argv:
        # Process approved invoices
        processed = odoo.process_approved_invoices()
        print()
        print('=' * 70)
        print(f'  INVOICES PROCESSED: {processed}')
        print('=' * 70)


if __name__ == '__main__':
    main()
