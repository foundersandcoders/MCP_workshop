# Stage 04: Deploy to Claude Code

## Starting Point

You begin with the completed Stage 02 tools:
- `list_directory(directory)` - List files and directories
- `read_code_file(file_path)` - Read file contents
- `search_code(pattern, directory)` - Search text across files
- `locate_function(function_name, directory)` - Locate function definitions
- `get_imports(directory)` - Extract import statements
- `parse_file_structure(file_path)` - Parse Python file structure
- `ping()` - Health check

## Goal

Make your MCP server accessible to Claude Code so you can use it in any project directory.

## Step 1: Update for Claude Code integration

In `utils/codebase_utils.py`, change line 16 from:
```python
root = os.getenv("PROJECT_ROOT", ".")
```
to:
```python
root = os.getenv("PROJECT_ROOT", os.getcwd())
```

This ensures the server uses the actual directory where Claude Code is running.

## Step 2: Install fastmcp globally

Use `pipx` to install `fastmcp` in an isolated environment. This prevents dependency conflicts with your system Python and makes the `fastmcp` command globally available:

### macOS
```bash
brew install pipx
pipx install fastmcp
```

### Windows
```powershell
pip install --user pipx
pipx install fastmcp
```

### Windows with WSL / Linux
```bash
sudo apt install pipx  # Ubuntu/Debian
# OR
pip install --user pipx

pipx install fastmcp
```

## Step 3: Add to Claude Code

Use `--scope user` to make the server available globally across all projects:

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

## Step 4: Test the connection

```bash
claude mcp list
```

You should see:
```
codebase-navigator: stdio [fastmcp command] - ✓ Connected
```

## How it works

- The MCP server uses the **current working directory** (where you invoke Claude Code) as the project root
- When you run `claude` from `/path/to/your/project`, the server navigates that project
- You can optionally create a `.env` file in your project with `PROJECT_ROOT=/different/path` to override this behavior

## Configuration files

Claude Code stores MCP settings in:
- **macOS**: `~/.config/claude/claude_desktop_config.json`
- **Windows WSL**: `/home/alex/.config/claude-code/mcp_settings.json`

## Remove if needed

```bash
claude mcp remove codebase-navigator --scope user
```