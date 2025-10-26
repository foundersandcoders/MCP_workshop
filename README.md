# Stage 01: Implement list_directory

## What's implemented

This stage implements the first codebase navigator tool:

- `list_directory(directory=".")` - List files and directories
- Uses `PROJECT_ROOT` from `.env` file (defaults to current directory)

## Test with MCP Inspector

Launch Inspector:

```bash
npx @modelcontextprotocol/inspector python3 server.py
```

Inspector opens at [http://localhost:5173](http://localhost:5173)

**Test the tools:**

1. `ping` → returns `{"ok": true, "message": "Server is running"}`
2. `list_directory()` → lists files in PROJECT_ROOT
3. `list_directory(directory="utils")` → lists files in utils folder

**Understanding the response:**
- `directory`: The relative path you passed in
- `absolute_path`: The actual full path being listed
- `project_root`: The PROJECT_ROOT from `.env` file
- `files` and `directories`: Contents found

## Optional: Configure PROJECT_ROOT

Copy `.env.example` to `.env` and set your project root:

```
PROJECT_ROOT=.
```

All paths in tools are relative to this root.