import subprocess, json
from pathlib import Path
from collections import Counter

def _run(cmd, cwd):
    # TODO: handle errors (non-zero exit), return stdout as text
    out = subprocess.check_output(cmd, cwd=cwd, text=True)
    return out

def list_recent_commits(repo_path: Path, limit: int):
    # TODO: research a good pretty format; include author, date (iso), subject
    fmt = r"%an|%ad|%s"
    log = _run(["git", "log", f"-n{limit}", f"--pretty=format:{fmt}", "--date=iso"], repo_path)
    commits = []
    for line in log.splitlines():
        try:
            author, date, subject = line.split("|", 2)
            commits.append({"author": author, "date": date, "message": subject})
        except ValueError:
            continue
    return commits

def top_authors(repo_path: Path):
    fmt = r"%an"
    log = _run(["git", "log", f"--pretty=format:{fmt}"], repo_path)
    counts = Counter(log.splitlines())
    # TODO: maybe include emails via %ae
    return [{"author": a, "commits": c} for a, c in counts.most_common()]

def hot_files(repo_path: Path, top: int):
    # TODO: try --name-only or --numstat; pick one and parse
    log = _run(["git", "log", "--name-only", "--pretty=format:"], repo_path)
    counts = Counter(p for p in log.splitlines() if p.strip())
    return [{"file": f, "changes": n} for f, n in counts.most_common(top)]
