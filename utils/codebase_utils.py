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
