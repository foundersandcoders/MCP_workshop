# Code Review Helper MCP Server Workshop

Multi-tool MCP server with code analysis, pattern detection, and LLM-powered test generation.

## Test with MCP Inspector

Launch Inspector for local testing:

```bash
npx @modelcontextprotocol/inspector python3 server.py
```

Inspector opens at [http://localhost:5173](http://localhost:5173)

## Configure for Global Use

Install for use across all projects with Claude Code CLI:

```bash
# Install pipx and fastmcp
brew install pipx  # macOS
pipx install fastmcp

# Install required dependencies for LLM features
pipx inject fastmcp anthropic python-dotenv

# Add to Claude Code (replace with your actual path)
claude mcp add code-reviewer --scope user ~/.local/bin/fastmcp run /path/to/your/MCP_workshop/server.py

# Verify connection
claude mcp list
```

## Available Tools

### Code Analysis (Stage 1)
- `analyze_code_file()` - Basic metrics and structure analysis
- `check_code_syntax()` - Syntax validation for Python/JavaScript

### Pattern Detection (Stage 2)
- `detect_code_patterns()` - Find design patterns (Manager, Factory, etc.)
- `check_code_anti_patterns()` - Identify code smells and anti-patterns

### Test Generation & Style (Stage 3)
- `generate_test_cases()` - LLM-powered test generation
- `check_code_style()` - Style guide validation

## Workshop Exercise

See `instructions.md` for complete 3-stage workshop building code review tools from scratch.

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

**"No module named 'anthropic'" error?**
```bash
# Install dependencies in the fastmcp environment
pipx inject fastmcp anthropic python-dotenv

# Or install fastmcp with dependencies
pipx uninstall fastmcp
pipx install fastmcp[anthropic,python-dotenv]
```

**Running locally instead of globally?**
```bash
# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate
pip install -r requirements.txt

# Then test with Inspector
npx @modelcontextprotocol/inspector python3 server.py
```