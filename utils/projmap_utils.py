from pathlib import Path
from collections import Counter

def list_directories(root: Path, depth: int):
    # TODO: enforce depth: only include paths up to depth levels
    root = Path(root)
    tree = []
    for p in root.rglob("*"):
        if p.is_dir():
            rel = p.relative_to(root)
            if len(rel.parts) <= depth:
                tree.append(str(rel))
    return tree

def count_filetypes(root: Path):
    exts = Counter()
    for p in Path(root).rglob("*.*"):
        if p.is_file():
            exts[p.suffix.lower()] += 1
    return [{"ext": k, "count": v} for k, v in exts.most_common()]

def find_readmes(root: Path):
    names = {"readme", "readme.md", "readme.rst", "contributing.md"}
    hits = []
    for p in Path(root).rglob("*"):
        if p.is_file() and p.name.lower() in names:
            hits.append(str(p.relative_to(root)))
    return hits
