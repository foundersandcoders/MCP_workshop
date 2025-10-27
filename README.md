# Stage 03: Make it accessible to Claude Code

## Prerequisites

Install fastmcp globally using pipx:

### macOS
```bash
brew install pipx
pipx install fastmcp
```

### Windows
```powershell
# Install pipx via pip
pip install --user pipx
pipx install fastmcp
```

### Windows with WSL / Linux
```bash
# Install pipx via package manager or pip
sudo apt install pipx  # Ubuntu/Debian
# OR
pip install --user pipx

pipx install fastmcp
```

## Add MCP server to user-wide Claude Code configuration

The key is using the `fastmcp` executable instead of direct python, which handles the isolated environment properly.

**Important:** Use `--scope user` to make the MCP server available globally across all projects, not just the current directory.

### macOS
```bash
claude mcp add codebase-navigator --scope user ~/.local/bin/fastmcp run /path/to/your/MCP_workshop/server.py
```

### Windows
```powershell
claude mcp add codebase-navigator --scope user %USERPROFILE%\.local\bin\fastmcp.exe run C:\path\to\your\MCP_workshop\server.py
```

### Windows with WSL / Linux
```bash
claude mcp add codebase-navigator --scope user ~/.local/bin/fastmcp run /path/to/your/MCP_workshop/server.py
```

## Test the connection

```bash
claude mcp list
```

You should see:
```
codebase-navigator: stdio [fastmcp command] - ✓ Connected
```

## Remove if needed

```bash
claude mcp remove codebase-navigator --scope user
```

## Scopes explained

- **local**: Server only available in the current project directory
- **user**: Server available globally across all your projects (recommended)
- **project**: Server shared with the team via `.mcp.json` file

The `--scope user` flag works the same across macOS, Windows, and Linux - it stores the configuration in your user-specific Claude Code settings.

## Why pipx?

- **pipx** creates isolated environments for Python applications
- Prevents dependency conflicts with your system Python
- Makes the `fastmcp` command globally available
- Works consistently across platforms

## How it works

The MCP server automatically uses the **current working directory** (where you invoke Claude Code) as the project root. This means:

- When you run `claude` from `/path/to/your/project`, the MCP server will navigate that project
- You can optionally create a `.env` file in your project with `PROJECT_ROOT=/different/path` to override this behavior

### Key change

In `utils/codebase_utils.py`, change from:
```python
root = os.getenv("PROJECT_ROOT", ".")
```
to:
```python
root = os.getenv("PROJECT_ROOT", os.getcwd())
```

This ensures the server uses the actual current working directory instead of a relative path, making it work correctly when invoked from any project directory.     