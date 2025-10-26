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

# from utils.weather_utils import get_weather, get_coordinates
from utils.codebase_utils import list_files, read_file, search_in_files, find_function, find_imports

# ---- register the server ----
mcp = FastMCP("CodebaseNavigator")


@mcp.tool()
def ping() -> dict:
    """Basic liveness check - returns OK status"""
    return {"ok": True, "message": "Server is running"}


# ---- Weather tools (commented out) ----
# @mcp.tool()
# def weather(city: str) -> dict:
#     """Get current weather for a city using Open-Meteo API"""
#     coords = get_coordinates(city)
#     if "error" in coords:
#         return coords
#     return get_weather(coords["latitude"], coords["longitude"])


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


@mcp.tool()
def search_code(pattern: str, directory: str = ".") -> dict:
    """
    Search for text across files

    Args:
        pattern: Text to search for (case-insensitive)
        directory: Relative path from PROJECT_ROOT to search in (default: ".")
    """
    return search_in_files(pattern, directory)


@mcp.tool()
def locate_function(function_name: str, directory: str = ".") -> dict:
    """
    Locate function definitions

    Args:
        function_name: Name of the function to find
        directory: Relative path from PROJECT_ROOT to search in (default: ".")
    """
    return find_function(function_name, directory)


@mcp.tool()
def get_imports(directory: str = ".") -> dict:
    """
    Extract import statements from Python files

    Args:
        directory: Relative path from PROJECT_ROOT to search in (default: ".")
    """
    return find_imports(directory)


if __name__ == "__main__":
    # This starts the JSON-RPC stdio loop and *registers* all decorated tools.
    mcp.run()
