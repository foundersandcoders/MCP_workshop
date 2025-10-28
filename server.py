"""
MCP Server Scaffold
-----------------------------------------
"Registering a server" = creating a FastMCP instance and decorating
functions as tools/resources. When mcp.run() executes, the server
announces these tools to any MCP client (Inspector, Claude Desktop, etc.)
over JSON-RPC (stdio). Clients can discover and call them immediately.
"""

import os
from fastmcp import FastMCP

from utils.codebase_utils import list_files, read_file

# ---- register the server ----
mcp = FastMCP("CodebaseNavigator")


@mcp.tool()
def ping() -> dict:
    """Basic liveness check - returns OK status"""
    return {"ok": True, "message": "Server is running"}


# ---- Codebase Navigator tools ----
@mcp.tool()
def list_directory(directory: str = ".") -> dict:
    """
    List directory contents

    Args:
        directory: Relative path from PROJECT_ROOT (default: ".")
    """
    return list_files(directory)


@mcp.tool()
def read_code_file(file_path: str) -> dict:
    """
    Read file contents

    Args:
        file_path: Relative path to file from PROJECT_ROOT
    """
    return read_file(file_path)


if __name__ == "__main__":
    # This starts the JSON-RPC stdio loop and *registers* all decorated tools.
    mcp.run()
