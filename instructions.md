# Stage 02: Advanced Search and Analysis Tools

## Starting Point

You begin with the completed Stage 01 tools:
- `list_directory(directory)` - List files and directories
- `read_code_file(file_path)` - Read file contents
- `ping()` - Health check

## Build These Additional Tools

Add these four new tools to extend the codebase navigator:

- `search_code(pattern, directory)` - Search text across files (case-insensitive)
  - `pattern` parameter: text to search for
  - `directory` parameter: relative path from PROJECT_ROOT (defaults to ".")

- `locate_function(function_name, directory)` - Locate function definitions
  - `function_name` parameter: name of the function to find
  - `directory` parameter: relative path from PROJECT_ROOT (defaults to ".")

- `get_imports(directory)` - Extract import statements from Python files
  - `directory` parameter: relative path from PROJECT_ROOT (defaults to ".")

- `parse_file_structure(file_path)` - Parse Python file structure
  - `file_path` parameter: relative path to Python file from PROJECT_ROOT
  - Returns classes, functions, methods with line numbers

## Requirements

All tools should:
- Use `PROJECT_ROOT` from `.env` file as the base directory
- Treat all path parameters as relative to PROJECT_ROOT
- Include safety checks for path validation
- Return structured responses with metadata
- Be registered with the MCP server using the `@mcp.tool()` decorator

## Testing

Launch the MCP Inspector to test your tools:

```bash
npx @modelcontextprotocol/inspector python3 server.py
```

Inspector opens at [http://localhost:5173](http://localhost:5173)