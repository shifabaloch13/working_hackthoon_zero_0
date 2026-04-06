---
name: twitter-x-mcp
description: |
  MCP server for Twitter/X integration.
  Posts tweets, monitors mentions, and generates engagement summaries.
  Use for Twitter marketing and customer engagement.
---

# Twitter/X MCP Server

Twitter/X integration for AI Employee.

## Overview

Integrates Twitter/X for:
- Automated tweeting
- Mention monitoring
- Engagement tracking
- Thread creation

## Prerequisites

1. **Twitter Developer Account**
2. **Twitter App** with API v2 access
3. **Bearer Token**
4. **API Key & Secret**

## Installation

```bash
# Install Twitter API library
pip install tweepy
```

## Configuration

### twitter_config.json

```json
{
  "api_key": "your_api_key",
  "api_secret": "your_api_secret",
  "bearer_token": "your_bearer_token",
  "access_token": "your_access_token",
  "access_token_secret": "your_token_secret"
}
```

## Usage

### Post Tweet

```bash
python twitter_post.py \
  --text "Exciting news! Our AI Employee just got better. #AI #Automation"
```

### Post Thread

```bash
python twitter_thread.py \
  --tweets "tweet1.txt" "tweet2.txt" "tweet3.txt"
```

### Monitor Mentions

```bash
python twitter_monitor.py \
  --keywords "AI Employee,automation" \
  --interval 60
```

### Generate Summary

```bash
python twitter_summary.py \
  --period week
```

## Integration with AI Employee

### Approval Workflow

1. AI creates tweet draft
2. Moves to Pending_Approval/
3. Human approves
4. MCP posts to Twitter

## Best Practices

1. **Always require approval** before posting
2. **Monitor mentions** hourly
3. **Engage with replies** within 24 hours
4. **Post consistently** (1-3 times per day)
