import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()


def get_project_root() -> Path:
    """
    Get the project root directory from environment variable or use current directory

    Returns:
        Path object pointing to the project root
    """
    root = os.getenv("PROJECT_ROOT", ".")
    return Path(root).resolve()


def list_files(directory: str = ".") -> dict:
    """
    List directory contents

    Args:
        directory: Relative path from PROJECT_ROOT (default: ".")

    Returns:
        Dictionary with files and directories lists
    """
    project_root = get_project_root()
    target_dir = (project_root / directory).resolve()

    # Security check: ensure we stay within project root
    try:
        target_dir.relative_to(project_root)
    except ValueError:
        return {"error": "Access denied: path outside project root"}

    if not target_dir.exists():
        return {"error": f"Directory not found: {directory}"}

    if not target_dir.is_dir():
        return {"error": f"Not a directory: {directory}"}

    files = []
    directories = []

    try:
        for item in sorted(target_dir.iterdir()):
            if item.is_file():
                files.append(item.name)
            elif item.is_dir():
                directories.append(item.name)

        return {
            "directory": str(directory),
            "absolute_path": str(target_dir),
            "project_root": str(project_root),
            "files": files,
            "directories": directories,
            "total_files": len(files),
            "total_directories": len(directories),
        }
    except PermissionError:
        return {"error": f"Permission denied: {directory}"}


def read_file(file_path: str) -> dict:
    """
    Read file contents

    Args:
        file_path: Relative path to file from PROJECT_ROOT

    Returns:
        Dictionary with file contents and metadata
    """
    project_root = get_project_root()
    target_file = (project_root / file_path).resolve()

    # Security check: ensure we stay within project root
    try:
        target_file.relative_to(project_root)
    except ValueError:
        return {"error": "Access denied: path outside project root"}

    if not target_file.exists():
        return {"error": f"File not found: {file_path}"}

    if not target_file.is_file():
        return {"error": f"Not a file: {file_path}"}

    try:
        content = target_file.read_text()
        return {
            "file_path": str(file_path),
            "absolute_path": str(target_file),
            "content": content,
            "size": len(content),
            "lines": len(content.splitlines())
        }
    except PermissionError:
        return {"error": f"Permission denied: {file_path}"}
    except UnicodeDecodeError:
        return {"error": f"Cannot read file (not text): {file_path}"}


def search_in_files(pattern: str, directory: str = ".") -> dict:
    """
    Search for text across files

    Args:
        pattern: Text to search for (case-insensitive)
        directory: Relative path from PROJECT_ROOT to search in (default: ".")

    Returns:
        Dictionary with search results
    """
    project_root = get_project_root()
    search_dir = (project_root / directory).resolve()

    # Security check: ensure we stay within project root
    try:
        search_dir.relative_to(project_root)
    except ValueError:
        return {"error": "Access denied: path outside project root"}

    if not search_dir.exists():
        return {"error": f"Directory not found: {directory}"}

    if not search_dir.is_dir():
        return {"error": f"Not a directory: {directory}"}

    matches = []

    # Search through all files recursively
    for file_path in search_dir.rglob("*"):
        if not file_path.is_file():
            continue

        try:
            content = file_path.read_text()
            file_matches = []

            # Search each line
            for line_num, line in enumerate(content.splitlines(), 1):
                if pattern.lower() in line.lower():
                    file_matches.append({
                        "line": line_num,
                        "content": line.strip()
                    })

            if file_matches:
                relative_path = file_path.relative_to(project_root)
                matches.append({
                    "file": str(relative_path),
                    "matches": file_matches
                })

        except (UnicodeDecodeError, PermissionError):
            # Skip binary files and files we can't read
            continue

    return {
        "pattern": pattern,
        "directory": str(directory),
        "files_with_matches": len(matches),
        "results": matches
    }


def find_function(function_name: str, directory: str = ".") -> dict:
    """
    Locate function definitions

    Args:
        function_name: Name of the function to find
        directory: Relative path from PROJECT_ROOT to search in (default: ".")

    Returns:
        Dictionary with locations where function is defined
    """
    project_root = get_project_root()
    search_dir = (project_root / directory).resolve()

    # Security check
    try:
        search_dir.relative_to(project_root)
    except ValueError:
        return {"error": "Access denied: path outside project root"}

    if not search_dir.exists():
        return {"error": f"Directory not found: {directory}"}

    if not search_dir.is_dir():
        return {"error": f"Not a directory: {directory}"}

    matches = []

    # Search for function definitions
    for file_path in search_dir.rglob("*.py"):
        if not file_path.is_file():
            continue

        try:
            content = file_path.read_text()

            for line_num, line in enumerate(content.splitlines(), 1):
                # Simple pattern: "def function_name("
                if f"def {function_name}(" in line:
                    relative_path = file_path.relative_to(project_root)
                    matches.append({
                        "file": str(relative_path),
                        "line": line_num,
                        "content": line.strip()
                    })

        except (UnicodeDecodeError, PermissionError):
            continue

    return {
        "function_name": function_name,
        "directory": str(directory),
        "matches": matches,
        "found": len(matches) > 0
    }


def find_imports(directory: str = ".") -> dict:
    """
    Extract import statements from Python files

    Args:
        directory: Relative path from PROJECT_ROOT to search in (default: ".")

    Returns:
        Dictionary with all import statements found
    """
    project_root = get_project_root()
    search_dir = (project_root / directory).resolve()

    # Security check
    try:
        search_dir.relative_to(project_root)
    except ValueError:
        return {"error": "Access denied: path outside project root"}

    if not search_dir.exists():
        return {"error": f"Directory not found: {directory}"}

    if not search_dir.is_dir():
        return {"error": f"Not a directory: {directory}"}

    results = []

    # Search for import statements
    for file_path in search_dir.rglob("*.py"):
        if not file_path.is_file():
            continue

        try:
            content = file_path.read_text()
            imports = []

            for line_num, line in enumerate(content.splitlines(), 1):
                stripped = line.strip()
                # Find import and from...import statements
                if stripped.startswith("import ") or stripped.startswith("from "):
                    imports.append({
                        "line": line_num,
                        "statement": stripped
                    })

            if imports:
                relative_path = file_path.relative_to(project_root)
                results.append({
                    "file": str(relative_path),
                    "imports": imports,
                    "import_count": len(imports)
                })

        except (UnicodeDecodeError, PermissionError):
            continue

    return {
        "directory": str(directory),
        "files_with_imports": len(results),
        "total_imports": sum(r["import_count"] for r in results),
        "results": results
    }
