import os
import json
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Any
from packaging import version


def get_project_root() -> Path:
    """Get the project root directory (where tools are invoked)"""
    return Path(os.getcwd()).resolve()


def list_outdated() -> Dict[str, Any]:
    """
    Compare package versions against latest available versions

    Returns:
        Dictionary with outdated packages information
    """
    project_root = get_project_root()
    results = {
        "python_packages": [],
        "node_packages": [],
        "summary": {"total_outdated": 0, "python_count": 0, "node_count": 0}
    }

    # Check Python packages (requirements.txt)
    requirements_file = project_root / "requirements.txt"
    if requirements_file.exists():
        try:
            # Run pip list --outdated --format=json
            result = subprocess.run(
                ["pip", "list", "--outdated", "--format=json"],
                capture_output=True,
                text=True,
                check=True
            )
            outdated_packages = json.loads(result.stdout)

            for pkg in outdated_packages:
                results["python_packages"].append({
                    "name": pkg["name"],
                    "current_version": pkg["version"],
                    "latest_version": pkg["latest_version"],
                    "type": pkg.get("latest_filetype", "wheel")
                })

            results["summary"]["python_count"] = len(outdated_packages)

        except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
            results["python_packages"] = [{"error": "Could not check Python packages"}]

    # Check Node packages (package.json)
    package_json = project_root / "package.json"
    if package_json.exists():
        try:
            # Run npm outdated --json
            result = subprocess.run(
                ["npm", "outdated", "--json"],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            # npm outdated returns exit code 1 when packages are outdated, so don't check=True
            if result.stdout:
                outdated_packages = json.loads(result.stdout)

                for pkg_name, pkg_info in outdated_packages.items():
                    results["node_packages"].append({
                        "name": pkg_name,
                        "current_version": pkg_info.get("current", "unknown"),
                        "wanted_version": pkg_info.get("wanted", "unknown"),
                        "latest_version": pkg_info.get("latest", "unknown"),
                        "location": pkg_info.get("location", "unknown")
                    })

                results["summary"]["node_count"] = len(outdated_packages)

        except (json.JSONDecodeError, FileNotFoundError):
            results["node_packages"] = [{"error": "Could not check Node packages"}]

    results["summary"]["total_outdated"] = (
        results["summary"]["python_count"] + results["summary"]["node_count"]
    )

    return results


def check_vulnerabilities() -> Dict[str, Any]:
    """
    Check for known vulnerabilities using npm audit and OSV API

    Returns:
        Dictionary with vulnerability information
    """
    project_root = get_project_root()
    results = {
        "python_vulnerabilities": [],
        "node_vulnerabilities": [],
        "summary": {"total_vulnerabilities": 0, "critical": 0, "high": 0, "moderate": 0, "low": 0}
    }

    # Check Python vulnerabilities using OSV API
    requirements_file = project_root / "requirements.txt"
    if requirements_file.exists():
        try:
            with open(requirements_file, 'r') as f:
                requirements = f.read().splitlines()

            for req in requirements:
                if req.strip() and not req.startswith('#'):
                    # Parse package name (handle formats like "package==1.0.0" or "package>=1.0.0")
                    pkg_name = req.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0].strip()

                    # Query OSV API
                    try:
                        osv_response = requests.post(
                            "https://api.osv.dev/v1/query",
                            json={"package": {"name": pkg_name, "ecosystem": "PyPI"}},
                            timeout=5
                        )

                        if osv_response.status_code == 200:
                            vuln_data = osv_response.json()
                            if vuln_data.get("vulns"):
                                for vuln in vuln_data["vulns"][:3]:  # Limit to 3 most recent
                                    results["python_vulnerabilities"].append({
                                        "package": pkg_name,
                                        "vulnerability_id": vuln.get("id", "unknown"),
                                        "summary": vuln.get("summary", "No summary available"),
                                        "severity": "unknown",  # OSV doesn't always provide severity
                                        "published": vuln.get("published", "unknown")
                                    })
                    except requests.RequestException:
                        continue  # Skip if API is unavailable

        except Exception as e:
            results["python_vulnerabilities"] = [{"error": f"Could not check Python vulnerabilities: {str(e)}"}]

    # Check Node vulnerabilities using npm audit
    package_json = project_root / "package.json"
    if package_json.exists():
        try:
            result = subprocess.run(
                ["npm", "audit", "--json"],
                capture_output=True,
                text=True,
                cwd=project_root
            )

            if result.stdout:
                audit_data = json.loads(result.stdout)

                # Parse npm audit output (format varies by npm version)
                if "vulnerabilities" in audit_data:
                    for vuln_name, vuln_info in audit_data["vulnerabilities"].items():
                        severity = vuln_info.get("severity", "unknown")
                        results["node_vulnerabilities"].append({
                            "package": vuln_name,
                            "severity": severity,
                            "title": vuln_info.get("title", "No title"),
                            "url": vuln_info.get("url", ""),
                            "via": vuln_info.get("via", [])
                        })

                        # Count by severity
                        if severity in results["summary"]:
                            results["summary"][severity] += 1

        except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
            results["node_vulnerabilities"] = [{"error": "Could not run npm audit"}]

    # Calculate total vulnerabilities
    results["summary"]["total_vulnerabilities"] = (
        len([v for v in results["python_vulnerabilities"] if "error" not in v]) +
        len([v for v in results["node_vulnerabilities"] if "error" not in v])
    )

    return results


def summary() -> Dict[str, Any]:
    """
    Return simplified health report combining outdated packages and vulnerabilities

    Returns:
        Dictionary with overall project health summary
    """
    outdated = list_outdated()
    vulnerabilities = check_vulnerabilities()

    # Calculate health score (0-100)
    total_packages = outdated["summary"]["total_outdated"]
    total_vulns = vulnerabilities["summary"]["total_vulnerabilities"]
    critical_vulns = vulnerabilities["summary"]["critical"]
    high_vulns = vulnerabilities["summary"]["high"]

    # Scoring algorithm
    health_score = 100
    health_score -= min(total_packages * 2, 30)  # Max 30 points for outdated packages
    health_score -= min(total_vulns * 5, 40)     # Max 40 points for vulnerabilities
    health_score -= critical_vulns * 15          # Extra penalty for critical
    health_score -= high_vulns * 10              # Extra penalty for high
    health_score = max(health_score, 0)          # Don't go below 0

    # Determine risk level
    if health_score >= 80:
        risk_level = "low"
        status = "healthy"
    elif health_score >= 60:
        risk_level = "moderate"
        status = "attention_needed"
    elif health_score >= 40:
        risk_level = "high"
        status = "needs_action"
    else:
        risk_level = "critical"
        status = "immediate_action_required"

    # Generate recommendations
    recommendations = []
    if total_packages > 0:
        recommendations.append(f"Update {total_packages} outdated packages")
    if critical_vulns > 0:
        recommendations.append(f"URGENT: Fix {critical_vulns} critical vulnerabilities")
    if high_vulns > 0:
        recommendations.append(f"Fix {high_vulns} high-severity vulnerabilities")
    if not recommendations:
        recommendations.append("All dependencies are up to date and secure")

    return {
        "health_score": health_score,
        "risk_level": risk_level,
        "status": status,
        "summary": {
            "outdated_packages": total_packages,
            "total_vulnerabilities": total_vulns,
            "critical_vulnerabilities": critical_vulns,
            "high_vulnerabilities": high_vulns,
            "moderate_vulnerabilities": vulnerabilities["summary"]["moderate"],
            "low_vulnerabilities": vulnerabilities["summary"]["low"]
        },
        "recommendations": recommendations,
        "last_checked": "now"
    }