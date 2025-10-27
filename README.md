# Stage 02: Codebase Navigator Tools

## Tools Overview

- `search_code` - Search text across files
- `locate_function` - Locate function definitions
- `get_imports` - Extract import statements
- `parse_file_structure` - Parse file outline (classes, functions, methods)

---

## 1. search_code

Simple text search (case-insensitive) across all files recursively.

**Test examples:**
```
search_code(pattern="def")
search_code(pattern="tool", directory="utils")
```

---

## 2. locate_function

Locate where a function is defined.

**Test examples:**
```
locate_function(function_name="list_files")
locate_function(function_name="ping", directory=".")
```

---

## 3. get_imports

Extract all import statements from Python files.

**Test examples:**
```
get_imports()
get_imports(directory="utils")
```

---

## 4. parse_file_structure

Parse Python file to extract classes, functions, and methods with their line numbers.

**Test examples:**
```
parse_file_structure(file_path="server.py")
parse_file_structure(file_path="utils/codebase_utils.py")
```

**Response includes:**
- `classes`: Array of classes with their methods
- `functions`: Array of top-level functions
- `class_count` and `function_count`: Summary counts