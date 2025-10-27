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
from utils.weather_utils import get_weather, get_coordinates
from utils.security_utils import list_outdated, check_vulnerabilities, summary

# ---- register the server ----
mcp = FastMCP("WorkshopServer")


@mcp.tool()
def ping() -> dict:
    """Basic liveness check - returns OK status"""
    return {"ok": True, "message": "Server is running"}


@mcp.tool()
def weather(city: str) -> dict:
    """Get current weather for a city using Open-Meteo API"""

    coords = get_coordinates(city)
    if "error" in coords:
        return coords
    return get_weather(coords["latitude"], coords["longitude"])


# ---- Security/Dependency Auditing tools ----
@mcp.tool()
def list_outdated_packages() -> dict:
    """Compare package versions against latest available versions"""
    return list_outdated()


@mcp.tool()
def check_security_vulnerabilities() -> dict:
    """Check for known vulnerabilities using npm audit and OSV API"""
    return check_vulnerabilities()


@mcp.tool()
def security_summary() -> dict:
    """Return simplified health report combining outdated packages and vulnerabilities"""
    return summary()


if __name__ == "__main__":
    # This starts the JSON-RPC stdio loop and *registers* all decorated tools.
    mcp.run()
