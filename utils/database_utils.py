import os
import sqlite3
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
import sqlparse


def get_project_root() -> Path:
    """Get the project root directory (where tools are invoked)"""
    return Path(os.getcwd()).resolve()


# ---- Stage 1: Basic Query Execution ----


def execute_query(database_path: str, query: str) -> Dict[str, Any]:
    """
    Execute SQL query on SQLite database

    Args:
        database_path: Relative path to SQLite database file
        query: SQL query to execute

    Returns:
        Dictionary with query results or error
    """
    project_root = get_project_root()
    db_file = (project_root / database_path).resolve()

    if not db_file.exists():
        return {"error": f"Database not found: {database_path}"}

    try:
        # Parse and validate query
        parsed = sqlparse.parse(query)
        if not parsed:
            return {"error": "Invalid SQL query"}

        # Check if it's a safe read-only query
        query_type = get_query_type(query)
        if query_type not in ['SELECT', 'EXPLAIN', 'PRAGMA']:
            return {"error": f"Only SELECT, EXPLAIN, and PRAGMA queries allowed. Got: {query_type}"}

        with sqlite3.connect(db_file) as conn:
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()

            cursor.execute(query)

            if query_type == 'SELECT':
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                data = [dict(row) for row in rows]

                return {
                    "database_path": database_path,
                    "query": query,
                    "columns": columns,
                    "row_count": len(data),
                    "data": data[:100],  # Limit to first 100 rows
                    "truncated": len(data) > 100
                }
            else:
                # For EXPLAIN and PRAGMA queries
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                data = [dict(row) for row in rows]

                return {
                    "database_path": database_path,
                    "query": query,
                    "query_type": query_type,
                    "result": data
                }

    except sqlite3.Error as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Query execution failed: {str(e)}"}


def get_schema(database_path: str) -> Dict[str, Any]:
    """
    Get database schema information

    Args:
        database_path: Relative path to SQLite database file

    Returns:
        Dictionary with schema information
    """
    project_root = get_project_root()
    db_file = (project_root / database_path).resolve()

    if not db_file.exists():
        return {"error": f"Database not found: {database_path}"}

    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            schema_info = {"database_path": database_path, "tables": {}}

            for table in tables:
                # Get table info
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()

                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = cursor.fetchone()[0]

                schema_info["tables"][table] = {
                    "columns": [
                        {
                            "name": col[1],
                            "type": col[2],
                            "not_null": bool(col[3]),
                            "primary_key": bool(col[5])
                        }
                        for col in columns
                    ],
                    "row_count": row_count
                }

            return schema_info

    except sqlite3.Error as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Schema extraction failed: {str(e)}"}


# ---- Stage 2: Natural Language to SQL ----


def generate_sql_from_text(database_path: str, natural_query: str) -> Dict[str, Any]:
    """
    Generate SQL query from natural language using LLM

    Args:
        database_path: Relative path to SQLite database file
        natural_query: Natural language description of desired query

    Returns:
        Dictionary with generated SQL and explanation
    """
    # First get schema to provide context to LLM
    schema_info = get_schema(database_path)
    if "error" in schema_info:
        return schema_info

    try:
        import os
        from anthropic import Anthropic
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return {"error": "ANTHROPIC_API_KEY not found"}

        client = Anthropic(api_key=api_key)

        # Create schema description for prompt
        schema_desc = format_schema_for_prompt(schema_info)

        prompt = f"""Given this SQLite database schema:

{schema_desc}

Generate a SQL query for this request: "{natural_query}"

Requirements:
- Return only SELECT queries (no INSERT, UPDATE, DELETE)
- Use proper SQLite syntax
- Include helpful comments
- Return JSON format: {{"sql": "query here", "explanation": "what this query does"}}"""

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )

        # Try to extract JSON from response
        import json
        try:
            result = json.loads(response.content[0].text)
            return {
                "database_path": database_path,
                "natural_query": natural_query,
                "generated_sql": result.get("sql", ""),
                "explanation": result.get("explanation", ""),
                "schema_context": schema_info
            }
        except json.JSONDecodeError:
            # Fallback if LLM doesn't return proper JSON
            return {
                "database_path": database_path,
                "natural_query": natural_query,
                "generated_sql": response.content[0].text,
                "explanation": "SQL generated from natural language",
                "schema_context": schema_info
            }

    except Exception as e:
        return {"error": f"Could not generate SQL: {str(e)}"}


# ---- Stage 3: Query Optimization ----


def analyze_query_performance(database_path: str, query: str) -> Dict[str, Any]:
    """
    Analyze query performance and suggest optimizations

    Args:
        database_path: Relative path to SQLite database file
        query: SQL query to analyze

    Returns:
        Dictionary with performance analysis and suggestions
    """
    project_root = get_project_root()
    db_file = (project_root / database_path).resolve()

    if not db_file.exists():
        return {"error": f"Database not found: {database_path}"}

    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            # Get query execution plan
            explain_query = f"EXPLAIN QUERY PLAN {query}"
            cursor.execute(explain_query)
            plan_rows = cursor.fetchall()

            # Analyze the plan for optimization opportunities
            suggestions = analyze_execution_plan(plan_rows, query)

            return {
                "database_path": database_path,
                "query": query,
                "execution_plan": [
                    {
                        "selectid": row[0],
                        "order": row[1],
                        "from": row[2],
                        "detail": row[3]
                    }
                    for row in plan_rows
                ],
                "optimization_suggestions": suggestions,
                "query_complexity": get_query_complexity(query)
            }

    except sqlite3.Error as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"Performance analysis failed: {str(e)}"}


# ---- Helper Functions ----


def get_query_type(query: str) -> str:
    """Extract the type of SQL query"""
    query = query.strip().upper()
    if query.startswith('SELECT'):
        return 'SELECT'
    elif query.startswith('EXPLAIN'):
        return 'EXPLAIN'
    elif query.startswith('PRAGMA'):
        return 'PRAGMA'
    elif query.startswith('INSERT'):
        return 'INSERT'
    elif query.startswith('UPDATE'):
        return 'UPDATE'
    elif query.startswith('DELETE'):
        return 'DELETE'
    else:
        return 'UNKNOWN'


def format_schema_for_prompt(schema_info: Dict[str, Any]) -> str:
    """Format schema information for LLM prompt"""
    schema_lines = []

    for table_name, table_info in schema_info["tables"].items():
        schema_lines.append(f"Table: {table_name} ({table_info['row_count']} rows)")
        for col in table_info["columns"]:
            pk_marker = " (PRIMARY KEY)" if col["primary_key"] else ""
            null_marker = " NOT NULL" if col["not_null"] else ""
            schema_lines.append(f"  - {col['name']}: {col['type']}{pk_marker}{null_marker}")
        schema_lines.append("")

    return "\n".join(schema_lines)


def analyze_execution_plan(plan_rows: List, query: str) -> List[str]:
    """Analyze execution plan and generate optimization suggestions"""
    suggestions = []

    # Convert plan rows to strings for analysis
    plan_text = " ".join([str(row[3]) for row in plan_rows])

    # Check for table scans
    if "SCAN TABLE" in plan_text:
        suggestions.append("Consider adding indexes - query is doing table scans")

    # Check for missing indexes
    if "USING INDEX" not in plan_text and "SCAN TABLE" in plan_text:
        suggestions.append("No indexes detected in execution plan - consider creating indexes on frequently queried columns")

    # Check for complex joins
    if query.upper().count("JOIN") > 2:
        suggestions.append("Complex query with multiple joins - consider breaking into smaller queries or using views")

    # Check for SELECT *
    if "SELECT *" in query.upper():
        suggestions.append("Avoid SELECT * - specify only needed columns for better performance")

    # Check for ORDER BY without LIMIT
    if "ORDER BY" in query.upper() and "LIMIT" not in query.upper():
        suggestions.append("ORDER BY without LIMIT can be expensive - consider adding LIMIT if possible")

    if not suggestions:
        suggestions.append("Query appears to be well-optimized")

    return suggestions


def get_query_complexity(query: str) -> str:
    """Assess query complexity"""
    query_upper = query.upper()

    complexity_score = 0
    complexity_score += query_upper.count("JOIN") * 2
    complexity_score += query_upper.count("SUBQUERY") * 3
    complexity_score += query_upper.count("UNION") * 2
    complexity_score += query_upper.count("GROUP BY") * 1
    complexity_score += query_upper.count("ORDER BY") * 1
    complexity_score += query_upper.count("HAVING") * 2

    if complexity_score == 0:
        return "Simple"
    elif complexity_score <= 3:
        return "Moderate"
    elif complexity_score <= 8:
        return "Complex"
    else:
        return "Very Complex"