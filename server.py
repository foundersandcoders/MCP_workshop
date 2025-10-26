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
from utils.codebase_utils import list_files

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


if __name__ == "__main__":
    # This starts the JSON-RPC stdio loop and *registers* all decorated tools.
    mcp.run()
