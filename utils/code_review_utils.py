import os
import ast
import re
from pathlib import Path
from typing import Dict, Any


def get_project_root() -> Path:
    """Get the project root directory (where tools are invoked)"""
    return Path(os.getcwd()).resolve()


# ---- Stage 1: Basic Analysis ----


def analyze_file(file_path: str) -> Dict[str, Any]:
    """
    Simple code analysis with basic metrics

    Args:
        file_path: Relative path to file from project root

    Returns:
        Dictionary with analysis results
    """
    project_root = get_project_root()
    target_file = (project_root / file_path).resolve()

    # Basic validation
    if not target_file.exists():
        return {"error": f"File not found: {file_path}"}

    try:
        content = target_file.read_text(encoding="utf-8")
        lines = content.splitlines()

        # Basic line counting
        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if not line.strip())
        comment_lines = count_comment_lines(lines, target_file.suffix)
        code_lines = total_lines - blank_lines - comment_lines

        # Structure analysis based on file type
        if target_file.suffix == ".py":
            structure = analyze_python_structure(content)
        elif target_file.suffix in [".js", ".ts"]:
            structure = analyze_js_structure(content)
        else:
            structure = {"functions": 0, "classes": 0, "complexity": 1}

        return {
            "file_path": file_path,
            "language": get_language(target_file.suffix),
            "metrics": {
                "total_lines": total_lines,
                "code_lines": code_lines,
                "comment_lines": comment_lines,
                "blank_lines": blank_lines,
            },
            "structure": structure,
            "quality_score": calculate_simple_quality_score(
                code_lines, comment_lines, structure["complexity"]
            ),
        }

    except Exception as e:
        return {"error": f"Could not analyze file: {str(e)}"}


def check_syntax(file_path: str) -> Dict[str, Any]:
    """
    Simple syntax validation

    Args:
        file_path: Relative path to file from project root

    Returns:
        Dictionary with syntax check results
    """
    project_root = get_project_root()
    target_file = (project_root / file_path).resolve()

    if not target_file.exists():
        return {"error": f"File not found: {file_path}"}

    try:
        content = target_file.read_text(encoding="utf-8")

        if target_file.suffix == ".py":
            return check_python_syntax(content, file_path)
        elif target_file.suffix in [".js", ".ts"]:
            return check_js_syntax(content, file_path)
        else:
            return {
                "file_path": file_path,
                "syntax_valid": True,
                "message": f"Syntax checking not supported for {target_file.suffix}",
            }

    except Exception as e:
        return {"error": f"Could not check syntax: {str(e)}"}


# ---- Helper Functions ----


def count_comment_lines(lines, file_extension):
    """Count comment lines based on file type"""
    if file_extension == ".py":
        return sum(1 for line in lines if line.strip().startswith("#"))
    elif file_extension in [".js", ".ts"]:
        return sum(1 for line in lines if line.strip().startswith("//"))
    return 0


def analyze_python_structure(content):
    """Simple Python structure analysis using AST"""
    try:
        tree = ast.parse(content)
        functions = sum(
            1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
        )
        classes = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))

        # Simple complexity: count decision points
        complexity = 1 + sum(
            1
            for node in ast.walk(tree)
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try))
        )

        return {"functions": functions, "classes": classes, "complexity": complexity}
    except SyntaxError:
        return {"functions": 0, "classes": 0, "complexity": 1}


def analyze_js_structure(content):
    """Simple JavaScript structure analysis using regex"""
    # Count functions (basic patterns)
    functions = len(re.findall(r"function\s+\w+|const\s+\w+\s*=\s*\(", content))
    classes = len(re.findall(r"class\s+\w+", content))

    # Simple complexity: count if/while/for
    complexity = 1 + len(re.findall(r"\b(if|while|for)\s*\(", content))

    return {"functions": functions, "classes": classes, "complexity": complexity}


def check_python_syntax(content, file_path):
    """Check Python syntax using AST"""
    try:
        ast.parse(content)
        return {
            "file_path": file_path,
            "syntax_valid": True,
            "language": "python",
            "message": "No syntax errors found",
        }
    except SyntaxError as e:
        return {
            "file_path": file_path,
            "syntax_valid": False,
            "language": "python",
            "error": {"message": str(e), "line": e.lineno, "column": e.offset},
        }


def check_js_syntax(content, file_path):
    """Basic JavaScript syntax checks"""
    errors = []
    lines = content.splitlines()

    for i, line in enumerate(lines, 1):
        # Simple checks for common issues
        if line.count("(") != line.count(")"):
            errors.append(f"Line {i}: Unmatched parentheses")
        if line.count("{") != line.count("}"):
            errors.append(f"Line {i}: Unmatched braces")

    return {
        "file_path": file_path,
        "syntax_valid": len(errors) == 0,
        "language": "javascript",
        "message": "Basic syntax check (install Node.js for full validation)",
        "errors": errors[:5],  # Limit to first 5 errors
    }


def calculate_simple_quality_score(code_lines, comment_lines, complexity):
    """Calculate a simple quality score (0-100)"""
    score = 100

    # Penalty for high complexity
    if complexity > 10:
        score -= min((complexity - 10) * 5, 30)

    # Bonus for comments
    if code_lines > 0:
        comment_ratio = comment_lines / code_lines
        score += min(comment_ratio * 20, 20)

    return max(int(score), 0)


def get_language(extension):
    """Get language name from file extension"""
    mapping = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "javascript",
        ".tsx": "typescript",
    }
    return mapping.get(extension, "unknown")


# ---- Stage 2: Pattern Detection (Simplified) ----


def detect_patterns(file_path: str) -> Dict[str, Any]:
    """
    Simple pattern detection
    """
    project_root = get_project_root()
    target_file = (project_root / file_path).resolve()

    if not target_file.exists():
        return {"error": f"File not found: {file_path}"}

    try:
        content = target_file.read_text(encoding="utf-8")
        patterns = []

        # Simple pattern detection examples
        if "class" in content and "Manager" in content:
            patterns.append(
                {
                    "pattern": "Manager Pattern",
                    "description": "Class name suggests it manages other objects",
                }
            )

        if content.count("if") > 5:
            patterns.append(
                {
                    "pattern": "Complex Conditional Logic",
                    "description": "Many if statements - consider refactoring",
                }
            )

        return {
            "file_path": file_path,
            "patterns_detected": patterns,
            "message": "Simple pattern detection - expand in Stage 2",
        }

    except Exception as e:
        return {"error": f"Could not analyze patterns: {str(e)}"}


def check_anti_patterns(file_path: str) -> Dict[str, Any]:
    """
    Simple anti-pattern detection
    """
    project_root = get_project_root()
    target_file = (project_root / file_path).resolve()

    if not target_file.exists():
        return {"error": f"File not found: {file_path}"}

    try:
        content = target_file.read_text(encoding="utf-8")
        lines = content.splitlines()
        anti_patterns = []

        # Check for long functions (simple heuristic)
        if target_file.suffix == ".py":
            current_function = None
            function_length = 0

            for line in lines:
                if line.strip().startswith("def "):
                    if current_function and function_length > 20:
                        anti_patterns.append(
                            {
                                "anti_pattern": "Long Function",
                                "function": current_function,
                                "lines": function_length,
                                "suggestion": "Consider breaking into smaller functions",
                            }
                        )
                    current_function = line.strip().split("(")[0].replace("def ", "")
                    function_length = 1
                elif current_function and line.strip():
                    function_length += 1

        # Check for long lines
        long_lines = [
            (i + 1, len(line)) for i, line in enumerate(lines) if len(line) > 100
        ]
        if long_lines:
            anti_patterns.append(
                {
                    "anti_pattern": "Long Lines",
                    "count": len(long_lines),
                    "suggestion": "Break long lines for better readability",
                }
            )

        return {
            "file_path": file_path,
            "anti_patterns": anti_patterns,
            "message": "Simple anti-pattern detection - expand in Stage 2",
        }

    except Exception as e:
        return {"error": f"Could not check anti-patterns: {str(e)}"}


# ---- Stage 3: Test Generation & Style (Simplified) ----


def generate_tests(file_path: str) -> Dict[str, Any]:
    """
    Generate test cases using LLM
    """
    project_root = get_project_root()
    target_file = (project_root / file_path).resolve()

    if not target_file.exists():
        return {"error": f"File not found: {file_path}"}

    try:
        content = target_file.read_text(encoding="utf-8")

        # Find function definitions (Python and JavaScript)
        import re
        py_functions = re.findall(r'def\s+(\w+)\s*\([^)]*\):', content)
        js_functions = re.findall(r'function\s+(\w+)\s*\(|const\s+(\w+)\s*=.*=>|(\w+)\s*:\s*function', content)

        # Flatten JS matches and remove empty strings
        js_functions = [f for match in js_functions for f in match if f]

        all_functions = py_functions + js_functions

        if not all_functions:
            return {"error": "No functions found"}

        # Generate test using LLM
        import os
        from anthropic import Anthropic
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return {"error": "ANTHROPIC_API_KEY not found"}

        client = Anthropic(api_key=api_key)

        # Determine language and appropriate test framework
        if target_file.suffix == ".py":
            prompt = f"Generate pytest tests for these Python functions:\n\n{content}\n\nReturn only the test code."
        else:
            prompt = f"Generate JavaScript/Jest tests for these functions:\n\n{content}\n\nReturn only the test code."

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "file_path": file_path,
            "test_code": response.content[0].text
        }

    except Exception as e:
        return {"error": f"Could not generate tests: {str(e)}"}


def check_style_guide(file_path: str, style: str = "auto") -> Dict[str, Any]:
    """
    Simple style checking
    """
    return {
        "file_path": file_path,
        "style_guide": style,
        "message": "Style guide checking - implement in Stage 3",
        "example_violations": [
            "Line 15: Line too long (>100 characters)",
            "Line 23: Missing docstring",
        ],
        "todo": [
            "Integrate with flake8/eslint",
            "Check naming conventions",
            "Validate formatting rules",
        ],
    }
