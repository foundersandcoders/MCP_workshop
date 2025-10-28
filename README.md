# Local Database Explorer MCP Server Workshop

Multi-tool MCP server for exploring SQLite databases with natural language to SQL conversion and query optimization.

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

# Install required dependencies for database and LLM features
pipx inject fastmcp anthropic python-dotenv psycopg2-binary sqlparse

# Add to Claude Code (replace with your actual path)
claude mcp add db-explorer --scope user ~/.local/bin/fastmcp run /path/to/your/MCP_workshop/server.py

# Verify connection
claude mcp list
```

## Sample Databases

Create sample databases for testing:

```bash
python3 create_sample_db.py
```

## Workshop Exercise

See `instructions.md` for complete 3-stage workshop building database exploration tools from scratch.

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
pipx inject fastmcp anthropic python-dotenv psycopg2-binary sqlparse

# Or install fastmcp with dependencies
pipx uninstall fastmcp
pipx install fastmcp[anthropic,python-dotenv]
```

**Database not found errors?**
- Ensure sample databases are created with `python3 create_sample_db.py`
- Use relative paths from project root (e.g., "sample_ecommerce.db")
- Verify database files exist in the project directory

**Running locally instead of globally?**
```bash
# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate
pip install -r requirements.txt

# Create sample databases
python3 create_sample_db.py

# Then test with Inspector
npx @modelcontextprotocol/inspector python3 server.py
```