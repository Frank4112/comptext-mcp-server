# Quick Start Guide

## Installation

```bash
# Clone repository
git clone https://github.com/ProfRandom92/comptext-mcp-server.git
cd comptext-mcp-server

# Run setup
bash setup.sh  # macOS/Linux
# or: setup.bat  # Windows

# Configure
cp .env.example .env
# Edit .env and add your NOTION_API_TOKEN
```

## Test Installation

```bash
# Test Notion connection
python -c "from comptext_mcp.notion_client import get_all_modules; print(f'Loaded {len(get_all_modules())} modules')"

# Run tests
pytest tests/ -v
```

## Start Server

```bash
# MCP Server (for Claude, Cursor, etc.)
python -m comptext_mcp.server

# REST API (for Perplexity, ChatGPT, etc.)
python rest_api_wrapper.py
```

## Platform Setup

### Claude Desktop

Edit `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "comptext-codex": {
      "command": "python3",
      "args": ["-m", "comptext_mcp.server"],
      "cwd": "/path/to/comptext-mcp-server",
      "env": {
        "PYTHONPATH": "/path/to/comptext-mcp-server/src",
        "NOTION_API_TOKEN": "your_token",
        "COMPTEXT_DATABASE_ID": "0e038c9b52c5466694dbac288280dd93"
      }
    }
  }
}
```

Restart Claude Desktop.

### Perplexity (REST API)

```bash
# Start API
python rest_api_wrapper.py

# Get public URL
ngrok http 8000

# Use generated URL in Perplexity
```

## Next Steps

- Read [Platform Setup Guide](PLATFORM_SETUP.md)
- See [API Documentation](API.md)
- Check [Deployment Guide](DEPLOYMENT.md)
