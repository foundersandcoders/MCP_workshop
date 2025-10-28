"""
Database Explorer MCP Server
-----------------------------------------
Educational MCP server for exploring SQLite databases with natural language to SQL
and query optimization features.
"""

import os
from fastmcp import FastMCP
from utils.database_utils import (
    execute_query,
    get_schema,
    generate_sql_from_text,
    analyze_query_performance,
)

# ---- register the server ----
mcp = FastMCP("DatabaseExplorer")


@mcp.tool()
def ping() -> dict:
    """Basic liveness check - returns OK status"""
    return {"ok": True, "message": "Database Explorer Server is running"}


# ---- Stage 1: Basic Query Execution ----


@mcp.tool()
def execute_sql_query(database_path: str, query: str) -> dict:
    """
    Execute SQL query on SQLite database

    Args:
        database_path: Relative path to SQLite database file
        query: SQL query to execute (SELECT, EXPLAIN, PRAGMA only)

    Returns:
        Query results with columns and data
    """
    return execute_query(database_path, query)


@mcp.tool()
def get_database_schema(database_path: str) -> dict:
    """
    Get database schema information including tables, columns, and row counts

    Args:
        database_path: Relative path to SQLite database file

    Returns:
        Complete schema information for the database
    """
    return get_schema(database_path)


# ---- Stage 2: Natural Language to SQL ----


@mcp.tool()
def natural_language_to_sql(database_path: str, natural_query: str) -> dict:
    """
    Generate SQL query from natural language description using LLM

    Args:
        database_path: Relative path to SQLite database file
        natural_query: Natural language description of desired query

    Returns:
        Generated SQL query with explanation and schema context
    """
    return generate_sql_from_text(database_path, natural_query)


# ---- Stage 3: Query Optimization ----


@mcp.tool()
def analyze_query_optimization(database_path: str, query: str) -> dict:
    """
    Analyze query performance and provide optimization suggestions

    Args:
        database_path: Relative path to SQLite database file
        query: SQL query to analyze

    Returns:
        Execution plan analysis and optimization suggestions
    """
    return analyze_query_performance(database_path, query)


if __name__ == "__main__":
    # This starts the JSON-RPC stdio loop and *registers* all decorated tools.
    mcp.run()