# MCP Workshop Instructions

## Setup

1. **Environment Configuration**

   Copy `.env.example` to `.env` and configure your project root:
   ```
   PROJECT_ROOT=.
   ```
   All paths in tools are relative to this root.

2. **Dependencies**

   Make sure you have Python 3.x and Node.js installed. The MCP inspector will be automatically downloaded when using `npx`.


## Stage 01: Implement Codebase Navigation Tools

Build these two tools and add them to the server:

- `list_directory(directory)` - List files and directories in a given path
  - `directory` parameter: relative path from PROJECT_ROOT (defaults to "." for root)
- `read_code_file(file_path)` - Read and return the contents of a code file
  - `file_path` parameter: relative path from PROJECT_ROOT to the file

Both tools should:
- Use `PROJECT_ROOT` from `.env` file as the base directory
- Treat all path parameters as relative to PROJECT_ROOT
- Include safety checks for path validation
- Return structured responses with metadata
- Be registered with the MCP server using the `@mcp.tool()` decorator

 
## Tool Responses

Tool responses include:
- `directory`: The relative path you passed in
- `absolute_path`: The actual full path being processed
- `project_root`: The PROJECT_ROOT from `.env` file
- `files` and `directories`: Contents found
- Additional metadata depending on the tool

## Safety and Security

All tools implement safety checks:
- Path validation to prevent directory traversal attacks
- Respect for PROJECT_ROOT boundaries
- File size limits for reading operations
- Error handling for invalid operations