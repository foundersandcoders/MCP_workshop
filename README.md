# MCP Server Workshop

Multi-tool MCP server with codebase navigation, security scanning, and API integration examples.

## Test with MCP Inspector

Launch Inspector for local testing:

```bash
npx @modelcontextprotocol/inspector python server.py
```

Inspector opens at [http://localhost:5173](http://localhost:5173)

## Configure for Global Use

Install for use across all projects with Claude Code CLI:

```bash
# Install pipx and fastmcp
brew install pipx  # macOS
pipx install fastmcp

# Add to Claude Code (replace with your actual path)
claude mcp add codebase-navigator --scope user ~/.local/bin/fastmcp run /path/to/your/MCP_workshop/server.py

# Verify connection
claude mcp list
```

## Available Tools

### Codebase Navigation
- `list_directory()` - Browse project structure
- `read_code_file()` - Read file contents
- `search_code()` - Search across files
- `locate_function()` - Find function definitions
- `get_imports()` - Extract import statements

### Security Scanning
- `list_outdated_packages()` - Find outdated dependencies
- `check_security_vulnerabilities()` - Scan for known CVEs
- `security_summary()` - Generate health reports with risk scores

### Utilities
- `ping()` - Server health check
- `weather()` - Example API integration

## Workshop Exercise

See `instructions.md` for a complete exercise on building the dependency security scanner from scratch.

## Troubleshooting

**Inspector stuck?**
```bash
# macOS/Linux
pkill -f "@modelcontextprotocol/inspector"

# Windows
Get-Process | Where-Object { $_.Path -like "*@modelcontextprotocol*" } | Stop-Process
```

**MCP server not connecting?**
- Ensure `--scope user` flag is used for global access
- Check that fastmcp is installed via pipx
- Verify the server path in the configuration