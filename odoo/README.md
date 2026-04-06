# Odoo Community 19 Setup for AI Employee

This directory contains the Docker Compose setup for running Odoo Community 19 locally for the AI Employee Gold Tier integration.

## Quick Start

### 1. Start Odoo

```bash
cd odoo
docker-compose up -d
```

### 2. Access Odoo

- **Odoo Web Interface:** http://localhost:8069
- **PGAdmin:** http://localhost:8080
  - Email: admin@odoo.local
  - Password: admin_password

### 3. Initial Setup

1. Open http://localhost:8069 in your browser
2. Create your database:
   - Database Name: `ai_employee_db`
   - Email: your-email@example.com
   - Password: Choose a secure password
3. Install **Accounting** module from the Apps menu

### 4. Configure AI Employee

Update the Odoo MCP configuration:

```json
{
  "odoo_url": "http://localhost:8069",
  "database": "ai_employee_db",
  "username": "admin",
  "password": "your_password",
  "api_key": "generated_after_login"
}
```

## Directory Structure

```
odoo/
├── docker-compose.yml          # Docker Compose configuration
├── odoo-config/
│   └── odoo.conf              # Odoo server configuration
├── odoo-custom-addons/        # Custom modules (optional)
├── odoo-logs/                 # Odoo logs
├── postgres-backups/          # Database backups
├── scripts/
│   ├── odoo_mcp_server.py     # Odoo MCP server implementation
│   ├── test_odoo.py           # Test script
│   └── setup_odoo_database.py # Database setup helper
└── README.md                  # This file
```

## Default Credentials

| Service | Username | Password | URL |
|---------|----------|----------|-----|
| Odoo | admin | (set on first login) | http://localhost:8069 |
| PostgreSQL | odoo | odoo_password | localhost:5432 |
| PGAdmin | admin@odoo.local | admin_password | http://localhost:8080 |

## Docker Commands

```bash
# Start Odoo
docker-compose up -d

# Stop Odoo
docker-compose down

# View logs
docker-compose logs -f odoo

# Restart Odoo
docker-compose restart odoo

# Backup database
docker-compose exec postgres pg_dump -U odoo ai_employee_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U odoo -d ai_employee_db < backup.sql
```

## AI Employee Integration

Once Odoo is running, use the Odoo MCP server to:

- Create invoices
- Record payments
- Generate financial reports
- Sync with AI Employee vault

```bash
# Example: Create invoice
python scripts/odoo_mcp_server.py create-invoice \
  --partner "Client Name" \
  --amount 1500.00 \
  --description "Consulting Services"
```

## Troubleshooting

### Port Already in Use

If port 8069 is already in use, edit `docker-compose.yml`:

```yaml
ports:
  - "8070:8069"  # Use different host port
```

### Database Connection Issues

Check Odoo logs:

```bash
docker-compose logs odoo
```

### Reset Odoo

```bash
docker-compose down -v  # Remove all volumes
docker-compose up -d    # Start fresh
```

## Next Steps

1. Install Accounting module
2. Configure chart of accounts
3. Set up products and services
4. Add customers and vendors
5. Connect AI Employee MCP server

## Resources

- [Odoo 19 Documentation](https://www.odoo.com/documentation/19.0/)
- [Odoo External API Reference](https://www.odoo.com/documentation/19.0/developer/reference/external_api.html)
- [Odoo JSON-RPC Guide](https://www.odoo.com/documentation/19.0/developer/reference/external_api.html#json-rpc)
