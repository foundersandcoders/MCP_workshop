# Local Database Explorer MCP Server Workshop

## Overview

Build an MCP server that explores SQLite databases with SQL query execution, natural language to SQL conversion, and query optimization analysis. This exercise focuses on **learning core database concepts** and LLM integration for practical database tasks.


## Architecture: 3 Progressive Stages

### Stage 1: Basic Query Execution
- Safe SQL query execution (SELECT only)
- Database schema exploration
- Result formatting and display
- Query type validation

### Stage 2: Natural Language to SQL
- LLM-powered query generation
- Schema-aware prompt engineering
- Natural language query understanding
- Context-aware SQL generation

### Stage 3: Query Optimization
- Execution plan analysis
- Performance bottleneck detection
- Optimization suggestions
- Query complexity assessment

## Sample Databases

The workshop includes two sample SQLite databases:

**sample_ecommerce.db**: E-commerce data with customers, products, and orders
**sample_library.db**: Library system with authors, books, borrowers, and loans

Run `python3 create_sample_db.py` to create these databases.

## Stage 1: Basic Query Execution

### Tool 1: SQL Query Executor

#### `execute_sql_query(database_path: str, query: str)`
**Purpose**: Execute SQL queries safely on SQLite databases

**Your task**: Build a function that:
- Validates database file existence
- Parses and validates SQL queries using sqlparse
- Restricts to safe operations (SELECT, EXPLAIN, PRAGMA only)
- Executes queries with proper error handling
- Returns formatted results with column information

**Expected Output**:
```json
{
  "database_path": "sample_ecommerce.db",
  "query": "SELECT * FROM customers LIMIT 3",
  "columns": ["id", "name", "email", "city", "created_at"],
  "row_count": 3,
  "data": [
    {"id": 1, "name": "Alice Johnson", "email": "alice@email.com", "city": "New York"},
    {"id": 2, "name": "Bob Smith", "email": "bob@email.com", "city": "Los Angeles"},
    {"id": 3, "name": "Charlie Brown", "email": "charlie@email.com", "city": "Chicago"}
  ],
  "truncated": false
}
```

### Tool 2: Schema Explorer

#### `get_database_schema(database_path: str)`
**Purpose**: Extract and display database structure information

**Your task**: Build a function that:
- Connects to SQLite database
- Queries sqlite_master for table information
- Uses PRAGMA table_info() for column details
- Counts rows in each table
- Returns comprehensive schema information

**Expected Output**:
```json
{
  "database_path": "sample_ecommerce.db",
  "tables": {
    "customers": {
      "columns": [
        {"name": "id", "type": "INTEGER", "not_null": false, "primary_key": true},
        {"name": "name", "type": "TEXT", "not_null": true, "primary_key": false},
        {"name": "email", "type": "TEXT", "not_null": true, "primary_key": false}
      ],
      "row_count": 5
    }
  }
}
```

## Stage 2: Natural Language to SQL

### Tool 3: Natural Language Query Generator

#### `natural_language_to_sql(database_path: str, natural_query: str)`
**Goal**: Convert natural language requests into SQL queries using LLM

**Your task**: Build a function that:
1. Gets database schema for context
2. Creates a focused prompt with schema information
3. Calls Claude API to generate SQL
4. Parses the LLM response
5. Returns generated SQL with explanation

**Implementation approach**:
- Extract schema using get_schema() function
- Format schema information for LLM prompt
- Use Claude API with structured prompt
- Handle JSON response parsing with fallbacks
- Provide schema context in response

**Function structure**:
```
1. Get database schema for context
2. Format schema for LLM prompt
3. Create focused prompt with natural language request
4. Call Claude API with prompt
5. Parse JSON response or fallback to raw text
6. Return SQL with explanation and schema context
```

## Stage 3: Query Optimization

### Tool 4: Query Performance Analyzer

#### `analyze_query_optimization(database_path: str, query: str)`
**Goal**: Analyze query performance and suggest optimizations

**Your task**: Build a function that:
1. Executes EXPLAIN QUERY PLAN to get execution details
2. Analyzes the execution plan for optimization opportunities
3. Generates specific optimization suggestions
4. Assesses query complexity

**Implementation approach**:
- Use EXPLAIN QUERY PLAN to get execution details
- Parse execution plan for table scans, index usage
- Generate suggestions based on plan analysis
- Calculate complexity score based on query structure

**Function structure**:
```
1. Execute EXPLAIN QUERY PLAN on the query
2. Parse execution plan results
3. Analyze for optimization opportunities:
   - Table scans vs index usage
   - Missing indexes
   - Complex joins
   - SELECT * usage
4. Generate specific suggestions
5. Calculate complexity score
6. Return analysis with suggestions
```

**Optimization checks to implement**:
- **Table scans**: Flag when SCAN TABLE appears in plan
- **Missing indexes**: Detect lack of index usage
- **Complex queries**: Count JOINs, subqueries, etc.
- **SELECT * usage**: Suggest specifying columns
- **ORDER BY without LIMIT**: Flag potential performance issues

## Testing Your Implementation

Use MCP Inspector to test your tools:

```bash
npx @modelcontextprotocol/inspector python3 server.py
```

Open http://localhost:5173 and test each stage progressively:

1. **Stage 1**: Test with `get_database_schema("sample_ecommerce.db")` and basic SELECT queries
2. **Stage 2**: Try natural language queries like "show me all customers from New York"
3. **Stage 3**: Analyze complex queries for optimization opportunities

## Extension Ideas

Once you complete all 3 stages, consider adding:
- **PostgreSQL support**: Extend beyond SQLite
- **Query history**: Track and analyze past queries
- **Data visualization**: Generate charts from query results
- **Batch operations**: Execute multiple queries
- **Export features**: Save results to CSV/JSON