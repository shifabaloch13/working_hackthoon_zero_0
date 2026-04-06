---
name: odoo-accounting-mcp
description: |
  MCP server for Odoo Community 19 accounting integration.
  Creates invoices, records payments, and syncs with AI Employee vault.
  Use for business accounting automation with Docker-based self-hosted Odoo.
---

# Odoo Accounting MCP Server

Self-hosted Odoo Community 19 integration for AI Employee accounting automation.

## Overview

Integrates Odoo Community 19 (running via Docker Compose) with AI Employee for:
- Invoice creation and management
- Payment recording and reconciliation
- Financial reporting (receivables, payables)
- Partner/customer synchronization
- Bank statement integration

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  AI Employee    │────▶│  Odoo MCP        │────▶│  Odoo Community │
│  (Obsidian)     │     │  (odoo_mcp.py)   │────▶│  19 (Docker)    │
└─────────────────┘     └──────────────────┘     │  + PostgreSQL   │
                                                  └─────────────────┘
```

## Prerequisites

1. **Docker Desktop** (Windows/Mac) or **Docker + Docker Compose** (Linux)
2. **Python 3.10+**
3. **Python Libraries**:
   ```bash
   pip install requests
   ```

## Installation

### Step 1: Start Odoo with Docker Compose

```bash
cd odoo
docker-compose up -d
```

This starts:
- **Odoo Community 19** on http://localhost:8069
- **PostgreSQL 15** on localhost:5432
- **PGAdmin** on http://localhost:8080

### Step 2: Initial Odoo Setup

1. Open http://localhost:8069 in your browser
2. Create database:
   - Database Name: `ai_employee_db`
   - Email: `admin@example.com`
   - Password: Choose secure password
3. Install **Accounting** module from Apps menu
4. Go to Settings → Users & Companies → Users
5. Create API user for AI Employee:
   - Name: `AI Employee`
   - Email: `ai.employee@local`
   - Access Rights: Accounting / Administrator

### Step 3: Create Odoo Config

Create `odoo_config.json` in your project root:

```json
{
  "odoo_url": "http://localhost:8069",
  "database": "ai_employee_db",
  "username": "ai.employee@local",
  "password": "your_secure_password",
  "api_key": null
}
```

## Usage

### Create Invoice Draft

```bash
python odoo_mcp_server.py "../AI_Employee_Vault" --create-invoice --partner "Client A" --amount 1500.00 --description "Consulting Services - January"
```

Creates approval file in `Pending_Approval/`:
```markdown
---
type: odoo_invoice_request
partner: Client A
amount: 1500.00
description: Consulting Services - January
invoice_type: out_invoice
created: 2026-03-07T10:30:00
status: pending
---

# Odoo Invoice Draft

## Invoice Details
- **Customer**: Client A
- **Amount**: $1500.00
- **Description**: Consulting Services - January

## To Approve
Move this file to `/Approved` folder to create invoice in Odoo.
```

### Record Payment

```bash
python odoo_mcp_server.py "../AI_Employee_Vault" --record-payment --invoice-id 123 --amount 1500.00 --reference "Bank Transfer #456"
```

### Get Financial Report

```bash
# Get accounts receivable report
python odoo_mcp_server.py "../AI_Employee_Vault" --report --type receivables

# Get accounts payable report
python odoo_mcp_server.py "../AI_Employee_Vault" --report --type payables
```

### Sync Partners

```bash
python odoo_mcp_server.py "../AI_Employee_Vault" --sync-partners
```

Creates `Accounting/Partners.md` with all customers from Odoo.

### Process Approved Invoices

```bash
python odoo_mcp_server.py "../AI_Employee_Vault" --process-approved
```

Processes all invoices in `Approved/` folder and creates them in Odoo.

## Integration with AI Employee

### Approval Workflow

1. **AI Creates Invoice Draft**: Based on completed work or time tracking
2. **Human Review**: Draft appears in `Pending_Approval/ODOO_INVOICE_*.md`
3. **Human Approval**: Move file to `Approved/` folder
4. **MCP Creates Invoice**: Run `--process-approved` to create in Odoo
5. **Logging**: Action logged to `Logs/odoo_YYYY-MM-DD.json`

### Invoice to Payment Flow

```
1. WhatsApp message: "Can you send invoice for January?"
   ↓
2. Gmail Watcher creates: Needs_Action/WHATSAPP_*.md
   ↓
3. AI Employee creates: Pending_Approval/ODOO_INVOICE_*.md
   ↓
4. Human moves to: Approved/
   ↓
5. Run: odoo_mcp_server.py --process-approved
   ↓
6. Invoice created in Odoo, PDF generated
   ↓
7. AI sends email with invoice PDF
   ↓
8. Client pays
   ↓
9. AI records payment: --record-payment --invoice-id 123 --amount 1500
   ↓
10. Task moved to: Done/
```

### CEO Briefing Integration

The Odoo MCP integrates with CEO Briefing:

```markdown
## Financial Summary (This Week)

### Revenue
- **Invoices Sent**: $4,500
- **Payments Received**: $3,200
- **Outstanding**: $8,750

### Accounts Receivable
- **Total**: $8,750
- **Overdue**: $1,200 (Client B - Invoice #456)

### Accounts Payable
- **Total**: $2,100
- **Due This Week**: $800
```

## Docker Commands

```bash
# Start Odoo
cd odoo
docker-compose up -d

# Stop Odoo
docker-compose down

# View Odoo logs
docker-compose logs -f odoo

# Restart Odoo
docker-compose restart odoo

# Backup database
docker-compose exec postgres pg_dump -U odoo ai_employee_db > odoo-backup.sql

# Restore database
docker-compose exec -T postgres psql -U odoo -d ai_employee_db < odoo-backup.sql

# Reset (destroy all data)
docker-compose down -v
docker-compose up -d
```

## Odoo JSON-RPC API Reference

The MCP uses Odoo's external JSON-RPC API:

### Authentication

```python
POST /web/dataset/call
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "common",
    "method": "authenticate",
    "args": ["database", "username", "password", {}]
  },
  "id": "unique_id"
}
```

### Create Invoice

```python
POST /web/dataset/call_kw
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "model": "account.move",
    "method": "create",
    "args": [{
      "move_type": "out_invoice",
      "partner_id": 123,
      "invoice_line_ids": [(0, 0, {
        "name": "Services",
        "quantity": 1,
        "price_unit": 1500.00
      })]
    }]
  }
}
```

### Record Payment

```python
POST /web/dataset/call_kw
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "model": "account.payment.register",
    "method": "create",
    "args": [{
      "amount": 1500.00,
      "payment_date": "2026-03-07",
      "payment_reference": "Bank Transfer #456"
    }]
  }
}
```

## OdooMCP Class Reference

```python
class OdooMCP:
    def create_invoice_draft(partner_name: str, amount: float, 
                            description: str, invoice_type: str) -> Path
    def create_invoice(partner_name: str, amount: float,
                      description: str, invoice_type: str) -> dict
    def record_payment(invoice_id: int, amount: float,
                      payment_date: str, payment_reference: str) -> dict
    def get_financial_report(report_type: str) -> dict
    def sync_partners() -> dict
    def process_approved_invoices() -> int
```

## Best Practices

1. **Always Require Approval**: Invoices over $500 need human approval
2. **Regular Sync**: Sync partners weekly to keep vault updated
3. **Backup Daily**: Use cron job for daily database backups
4. **Reconcile Monthly**: Review bank statements and reconcile accounts
5. **Audit Trail**: All actions logged to `Logs/odoo_*.json`

## Troubleshooting

### Odoo Not Starting

```
ERROR: for odoo  Cannot start service odoo: failed to create task for container
```

**Solution**: Check Docker logs and ensure ports 8069, 5432 are not in use

### Database Connection Failed

```
[WARN] Could not connect to Odoo: Connection refused
```

**Solution**: 
```bash
docker-compose logs postgres
docker-compose restart postgres
```

### Authentication Failed

```
[WARN] Odoo authentication failed
```

**Solution**: Verify credentials in `odoo_config.json` match Odoo user

### Module Not Installed

```
[ERROR] Model 'account.move' not found
```

**Solution**: Install Accounting module in Odoo Apps menu

## Security

- **Never commit** `odoo_config.json` to version control
- Use strong passwords for Odoo admin and database
- Enable HTTPS for production deployments
- Regular security updates: `docker-compose pull && docker-compose up -d`
- Limit API user permissions to necessary modules only

## Production Deployment

For 24/7 operation, deploy on cloud VM:

```bash
# On Oracle Cloud / AWS / GCP
git clone <your-repo>
cd odoo

# Configure HTTPS with nginx reverse proxy
# Set up automated backups
# Configure monitoring

docker-compose up -d
```

### nginx Configuration

```nginx
server {
    listen 443 ssl;
    server_name odoo.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/odoo.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/odoo.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Example: Complete Invoice Flow

```bash
# 1. AI detects invoice request from WhatsApp
# Gmail Watcher creates: Needs_Action/WHATSAPP_client_request.md

# 2. AI creates invoice draft
python odoo_mcp_server.py "../AI_Employee_Vault" \
  --create-invoice \
  --partner "Client A" \
  --amount 1500.00 \
  --description "Consulting Services - January 2026"

# 3. Human reviews and approves (moves to Approved/)

# 4. Create invoice in Odoo
python odoo_mcp_server.py "../AI_Employee_Vault" --process-approved

# Output:
# ======================================================================
#   INVOICES PROCESSED: 1
# ======================================================================

# 5. Client pays via bank transfer

# 6. AI records payment
python odoo_mcp_server.py "../AI_Employee_Vault" \
  --record-payment \
  --invoice-id 123 \
  --amount 1500.00 \
  --reference "Bank Transfer #456"

# 7. Weekly CEO Briefing includes:
# - Invoice sent: $1500
# - Payment received: $1500
# - Outstanding: $0
```

## Resources

- [Odoo 19 Documentation](https://www.odoo.com/documentation/19.0/)
- [Odoo External JSON-RPC API](https://www.odoo.com/documentation/19.0/developer/reference/external_api.html)
- [Odoo Accounting Documentation](https://www.odoo.com/documentation/19.0/applications/finance/accounting.html)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Odoo GitHub](https://github.com/odoo/odoo)
