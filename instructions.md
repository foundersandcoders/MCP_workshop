# Code Review Helper MCP Server Workshop

## Overview

Build an MCP server that analyzes code files for issues, suggests improvements, generates test cases, and checks against style guides. This exercise focuses on **learning core concepts** rather than production complexity, making it perfect for understanding AI's code analysis capabilities.

## Prerequisites

To use this MCP server with Claude Code CLI globally, you need to install the dependencies using pipx:

```bash
# Install pipx and fastmcp
brew install pipx  # macOS
pipx install fastmcp

# Install required dependencies for LLM features
pipx inject fastmcp anthropic python-dotenv

# Add to Claude Code (replace with your actual path)
claude mcp add code-reviewer --scope user ~/.local/bin/fastmcp run /path/to/your/MCP_workshop/server.py
```

## Architecture: 3 Progressive Stages

### Stage 1: Basic Analysis
- Simple line counting and structure detection
- Basic AST parsing for Python, regex for JavaScript
- Quality scoring with simple algorithms
- Focus on core concepts, not edge cases

### Stage 2: Pattern Detection
- Simple pattern detection using string matching
- Basic anti-pattern identification with heuristics
- Educational examples students can expand
- Templates for more sophisticated analysis

### Stage 3: Test Generation
- LLM-powered test case generation
- Claude API integration
- Learning-focused implementations
- Extension points for advanced features


## Stage 1: Basic Analysis

### Tool 1: Code Analyzer

#### 1. `analyze_code_file(file_path: str)`
**Purpose**: Simple code analysis focusing on learning core concepts

**Your task**: Build a function that:
- **Line counting**: Total, code, comments, blank lines
- **Structure detection**: Functions, classes (using AST for Python, regex for JS)
- **Simple complexity**: Count decision points (if/while/for/try)
- **Quality score**: Basic 0-100 calculation
- **Multi-language**: Python (.py) and JavaScript (.js/.ts)

**Expected Output**:
```json
{
  "file_path": "sample_code.py",
  "language": "python",
  "metrics": {
    "total_lines": 78,
    "code_lines": 65,
    "comment_lines": 8,
    "blank_lines": 5
  },
  "structure": {
    "functions": 4,
    "classes": 1,
    "complexity": 12
  },
  "quality_score": 85
}
```

### Tool 2: Code Syntax Analyzer

#### 2. `check_code_syntax(file_path: str)`
**Purpose**: Basic syntax validation using simple techniques

**Your task**: Build a function that:
- **Python**: AST parsing (built-in, reliable)
- **JavaScript**: Simple bracket/parentheses matching (educational approach)
- **Error reporting**: Line numbers and basic messages
- **No external dependencies**: Pure Python implementation

**Expected Output**:
```json
{
  "file_path": "sample_code.js",
  "syntax_valid": false,
  "language": "javascript",
  "message": "Basic syntax check",
  "errors": [
    "Line 47: Unmatched parentheses"
  ]
}
```

## Stage 2: Pattern Detection

Create two new functions that analyze code using simple string operations.

### Tool 3: Pattern Detector

#### `detect_code_patterns(file_path: str)`
**Goal**: Find common design patterns by looking for characteristic text patterns.

**Your task**: Build a function that:
1. Reads the file content
2. Searches for pattern indicators using string operations
3. Returns a list of detected patterns

**Patterns to detect**:
- **Manager Pattern**: Look for `'class'` and `'Manager'` in the same file
- **Factory Pattern**: Search for `'def create'` or `'def make'` methods
- **Singleton Pattern**: Find `'_instance'` variables combined with classes
- **Builder Pattern**: Look for `'def build'` or `'Builder'` in class names

**Function structure**:
```
1. Get file content
2. Create empty patterns list
3. For each pattern:
   - Check if pattern indicators exist
   - If found, add to patterns list
4. Return results with file_path and patterns_detected
```

### Tool 4: Anti-Pattern Detector

#### `check_code_anti_patterns(file_path: str)`
**Goal**: Identify code smells by counting and measuring code characteristics.

**Your task**: Build a function that:
1. Reads file content and splits into lines
2. Counts various code characteristics
3. Flags problems when thresholds are exceeded

**Anti-patterns to detect**:
- **Too Many Conditionals**: Count `'if '` occurrences (flag if > 8)
- **Long Lines**: Find lines longer than 100 characters
- **Magic Numbers**: Look for hardcoded values like `'42'`, `'100'`, `'1000'`
- **Too Many Functions**: Count `'def '` occurrences (flag if > 15)

**Function structure**:
```
1. Get file content and lines
2. Create empty anti_patterns list
3. For each check:
   - Count or measure the characteristic
   - If threshold exceeded, add to anti_patterns list
4. Return results with file_path and anti_patterns
```

**Helpful techniques**:
- Use `content.count('text')` to count occurrences
- Use `'text' in content` to check if text exists
- Use `enumerate(lines, 1)` to get line numbers
- Use list comprehensions to find matching lines

## Stage 3: Test Generation

Build an LLM-powered test generator.

### Tool 5: LLM Test Generator

#### `generate_test_cases(file_path: str)`
**Goal**: Use an LLM to generate meaningful test cases for functions.

**Your task**: Build a simple LLM-powered test generator that:
1. Reads the file content
2. Finds function definitions using regex
3. Sends the entire file content to Claude API
4. Returns generated test code

**Implementation approach**:
- Use regex to detect functions (Python and JavaScript)
- Call Claude API with straightforward prompt
- Return the test code directly
- Simple error handling

## Testing Your Implementation

Use MCP Inspector to test your tools:

```bash
npx @modelcontextprotocol/inspector python server.py
```

Open http://localhost:5173 and test each stage progressively with the provided sample files.