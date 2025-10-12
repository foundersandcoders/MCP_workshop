import json, subprocess, os
from pathlib import Path

def _read_package_json(workdir: Path):
    pj = workdir / "package.json"
    return json.loads(pj.read_text()) if pj.exists() else None

def _read_requirements(workdir: Path):
    req = workdir / "requirements.txt"
    return req.read_text().splitlines() if req.exists() else None

def list_outdated(workdir: Path):
    # TODO: If npm project, run `npm outdated --json`; if Python, try `pip list --outdated --format=json`
    pj = _read_package_json(workdir)
    if pj:
        try:
            out = subprocess.check_output(["npm", "outdated", "--json"], cwd=workdir, text=True)
            data = json.loads(out) if out.strip() else {}
            return [{"name": k, "current": v.get("current"), "latest": v.get("latest")} for k, v in data.items()]
        except subprocess.CalledProcessError:
            return []
    req = _read_requirements(workdir)
    if req:
        try:
            out = subprocess.check_output(["pip", "list", "--outdated", "--format=json"], cwd=workdir, text=True)
            data = json.loads(out)
            return [{"name": d["name"], "current": d["version"], "latest": d["latest_version"]} for d in data]
        except Exception:
            return []
    return []

def check_vulnerabilities(workdir: Path):
    # TODO (research): use `npm audit --json` or `pip-audit -f json` or OSV API (offline fallback: return [])
    pj = _read_package_json(workdir)
    if pj:
        try:
            out = subprocess.check_output(["npm", "audit", "--json"], cwd=workdir, text=True)
            data = json.loads(out)
            # TODO: normalize to [{name, severity, via, fix_available}]
            advisories = []
            for v in data.get("vulnerabilities", {}).values():
                advisories.append({"name": v.get("name"), "severity": v.get("severity"), "fix": v.get("fixAvailable")})
            return advisories
        except Exception:
            return []
    return []

def deps_summary(workdir: Path):
    return {
        "outdated": list_outdated(workdir),
        "vulnerabilities": check_vulnerabilities(workdir)
    }
