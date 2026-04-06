---
name: email-mcp-server
description: |
  MCP server for sending, drafting, and searching emails via Gmail API.
  Provides tools for AI Employee to take email actions after human approval.
  Use for automated email responses, invoice delivery, and client communication.
---

# Email MCP Server Skill

Model Context Protocol (MCP) server for Gmail operations.

## Prerequisites

1. **Node.js 18+**
2. **Gmail API credentials** (same as Gmail Watcher)
3. **MCP SDK**: `npm install @modelcontextprotocol/sdk`

## Installation

```bash
# Create MCP server directory
mkdir -p ~/mcp-servers/email-mcp
cd ~/mcp-servers/email-mcp

# Initialize npm project
npm init -y

# Install dependencies
npm install @modelcontextprotocol/sdk express
npm install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Usage

### Configure in Qwen Code

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json",
        "GMAIL_TOKEN": "/path/to/token.json"
      }
    }
  }
}
```

### Start the Server

```bash
node index.js
```

## Available Tools

### `send_email`

Send an email via Gmail API.

**Parameters:**
- `to` (string, required): Recipient email address
- `subject` (string, required): Email subject
- `body` (string, required): Email body (plain text or HTML)
- `cc` (string, optional): CC recipients
- `bcc` (string, optional): BCC recipients
- `attachment` (string, optional): Path to attachment

**Example:**
```json
{
  "to": "client@example.com",
  "subject": "Invoice #1234",
  "body": "Please find attached your invoice.",
  "attachment": "/path/to/invoice.pdf"
}
```

### `draft_email`

Create a draft email (requires approval before sending).

**Parameters:** Same as `send_email`

**Returns:** Draft ID for later sending

### `search_emails`

Search Gmail for messages.

**Parameters:**
- `query` (string, required): Gmail search query
- `max_results` (number, optional): Max results (default: 10)

**Example:**
```json
{
  "query": "from:client@example.com is:unread",
  "max_results": 5
}
```

### `mark_read`

Mark emails as read.

**Parameters:**
- `email_ids` (array, required): List of Gmail message IDs

### `reply_to_email`

Reply to an existing email thread.

**Parameters:**
- `original_id` (string, required): Original email ID
- `body` (string, required): Reply body
- `send` (boolean, optional): Send immediately or save as draft

## Human-in-the-Loop Pattern

For sensitive actions, use approval workflow:

1. **AI creates approval request** in `Pending_Approval/`
2. **Human reviews** and moves to `Approved/`
3. **MCP server executes** the approved action

Example approval file:
```markdown
---
type: approval_request
action: send_email
to: client@example.com
subject: Invoice #1234
created: 2026-02-26T10:30:00Z
status: pending
---

## Email Details
- To: client@example.com
- Subject: Invoice #1234
- Attachment: invoice_1234.pdf

## To Approve
Move this file to /Approved folder.
```

## Security Notes

- **Never expose** credentials in code
- **Use environment variables** for sensitive data
- **Implement rate limiting** (max emails per hour)
- **Log all sent emails** for audit trail
- **Require approval** for emails to new recipients

## Integration with AI Employee

```python
# Example: Send approved email
def send_approved_email(approval_file):
    # Parse approval file
    # Call MCP send_email tool
    # Log result
    # Move file to Done/
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication failed | Refresh OAuth token |
| Rate limit exceeded | Implement exponential backoff |
| Attachment too large | Gmail limit is 25MB |
| Permission denied | Grant Gmail send permissions |
