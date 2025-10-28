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
from utils.code_review_utils import (
    analyze_file, check_syntax, detect_patterns,
    check_anti_patterns, generate_tests, check_style_guide
)

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


# ---- Code Review Helper tools ----
@mcp.tool()
def analyze_code_file(file_path: str) -> dict:
    """Analyze a code file and provide basic metrics, complexity, and quality indicators"""
    return analyze_file(file_path)


@mcp.tool()
def check_code_syntax(file_path: str) -> dict:
    """Validate syntax and find basic errors in code files"""
    return check_syntax(file_path)


@mcp.tool()
def detect_code_patterns(file_path: str) -> dict:
    """Find common design patterns and code structures"""
    return detect_patterns(file_path)


@mcp.tool()
def check_code_anti_patterns(file_path: str) -> dict:
    """Identify problematic code structures and anti-patterns"""
    return check_anti_patterns(file_path)


@mcp.tool()
def generate_test_cases(file_path: str) -> dict:
    """Generate test cases for functions and classes in the file"""
    return generate_tests(file_path)


@mcp.tool()
def check_code_style(file_path: str, style: str = "auto") -> dict:
    """Check code against style guides (PEP8, ESLint, etc.)"""
    return check_style_guide(file_path, style)


if __name__ == "__main__":
    # This starts the JSON-RPC stdio loop and *registers* all decorated tools.
    mcp.run()
