"""
MCP Server Scaffold (works for 3 options)
-----------------------------------------
"Registering a server" = creating a FastMCP instance and decorating
functions as tools/resources. When mcp.run() executes, the server
announces these tools to any MCP client (Inspector, Claude Desktop, etc.)
over JSON-RPC (stdio). Clients can discover and call them immediately.

Pick your option in config.json: git_insight | dep_health | proj_map
"""

import json, os
from pathlib import Path
from fastmcp import FastMCP

from utils.git_utils import (
    list_recent_commits,          # TODOs inside utils
    top_authors,
    hot_files,
)
from utils.deps_utils import (
    list_outdated,
    check_vulnerabilities,
    deps_summary,
)
from utils.projmap_utils import (
    list_directories,
    count_filetypes,
    find_readmes,
)

# ---- load config ----
CONFIG = json.loads(Path("config.json").read_text())
OPTION = CONFIG.get("option", "git_insight")
SERVER_NAME = CONFIG.get("server_name", "TeamServer")
WORKDIR = Path(CONFIG.get("workdir", ".")).resolve()

# ---- register the server ----
mcp = FastMCP(SERVER_NAME)

@mcp.tool()
def ping() -> dict:
    """Basic liveness check"""
    return {"ok": True, "cwd": str(WORKDIR), "option": OPTION}

# ---------- Option 1: Git Insight ----------
@mcp.tool()
def git_list_commits(limit: int = 10) -> dict:
    """Return last N commits (author, message, date)"""
    if OPTION != "git_insight":
        return {"error": "Set option=git_insight in config.json"}
    return {"commits": list_recent_commits(WORKDIR, limit)}

@mcp.tool()
def git_top_authors() -> dict:
    """Rank contributors by commit count"""
    if OPTION != "git_insight":
        return {"error": "Set option=git_insight in config.json"}
    return {"authors": top_authors(WORKDIR)}

@mcp.tool()
def git_hot_files(top: int = 10) -> dict:
    """Most frequently changed files"""
    if OPTION != "git_insight":
        return {"error": "Set option=git_insight in config.json"}
    return {"hot_files": hot_files(WORKDIR, top)}

# ---------- Option 2: Dependency Health ----------
@mcp.tool()
def deps_list_outdated() -> dict:
    """Outdated deps from package.json or requirements.txt"""
    if OPTION != "dep_health":
        return {"error": "Set option=dep_health in config.json"}
    return {"outdated": list_outdated(WORKDIR)}

@mcp.tool()
def deps_vulnerabilities() -> dict:
    """Known vulnerabilities via npm/pip/OSV"""
    if OPTION != "dep_health":
        return {"error": "Set option=dep_health in config.json"}
    return {"vulns": check_vulnerabilities(WORKDIR)}

@mcp.tool()
def deps_summary_tool() -> dict:
    """Compact health summary"""
    if OPTION != "dep_health":
        return {"error": "Set option=dep_health in config.json"}
    return deps_summary(WORKDIR)

# ---------- Option 3: Project Knowledge Map ----------
@mcp.tool()
def pm_list_directories(depth: int = 2) -> dict:
    """Folder tree up to depth"""
    if OPTION != "proj_map":
        return {"error": "Set option=proj_map in config.json"}
    return {"tree": list_directories(WORKDIR, depth)}

@mcp.tool()
def pm_count_filetypes() -> dict:
    """Counts by extension (.js, .ts, .py, etc.)"""
    if OPTION != "proj_map":
        return {"error": "Set option=proj_map in config.json"}
    return {"filetypes": count_filetypes(WORKDIR)}

@mcp.tool()
def pm_find_readmes() -> dict:
    """Find README-like docs"""
    if OPTION != "proj_map":
        return {"error": "Set option=proj_map in config.json"}
    return {"readmes": find_readmes(WORKDIR)}

# Optional shared resource (teams can customize)
@mcp.resource("team://summary")
def team_summary():
    return json.dumps({"server": SERVER_NAME, "option": OPTION, "workdir": str(WORKDIR)})

if __name__ == "__main__":
    # This starts the JSON-RPC stdio loop and *registers* all decorated tools.
    mcp.run()
