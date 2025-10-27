### Dependency Security Scanner MCP Server

## Overview

In this exercise, you'll build an MCP server that examines project dependencies for outdated packages and known security vulnerabilities. This is a practical security tool that developers use to maintain secure codebases.

## Requirements: Build an MCP server with **3 security tools**:

### 1. `list_outdated()` Tool

**Purpose**: Compare installed package versions against latest available versions

**Implementation Requirements**:

- Check Python packages using `pip list --outdated --format=json`
- Check Node.js packages using `npm outdated --json`
- Return structured data showing current vs latest versions
- Handle both `requirements.txt` and `package.json` files

**Expected Output**:

```json
{
  "python_packages": [
    {
      "name": "requests",
      "current_version": "2.25.1",
      "latest_version": "2.31.0",
      "type": "wheel"
    }
  ],
  "node_packages": [
    {
      "name": "lodash",
      "current_version": "4.17.15",
      "latest_version": "4.17.21"
    }
  ],
  "summary": {
    "total_outdated": 2,
    "python_count": 1,
    "node_count": 1
  }
}

```

### 2. `check_vulnerabilities()` Tool

**Purpose**: Check for known security vulnerabilities

**Implementation Requirements**:

- For Python: Use OSV.dev API (`https://api.osv.dev/v1/query`)
- For Node.js: Use `npm audit --json` command
- Parse and categorize vulnerabilities by severity
- Handle API timeouts and errors gracefully

**Expected Output**:

```json
{
  "python_vulnerabilities": [
    {
      "package": "requests",
      "vulnerability_id": "GHSA-j8r2-6x86-q33q",
      "summary": "Unintended leak of Proxy-Authorization header",
      "severity": "medium",
      "published": "2023-05-22T19:04:05Z"
    }
  ],
  "node_vulnerabilities": [
    {
      "package": "lodash",
      "severity": "high",
      "title": "Prototype Pollution",
      "url": "<https://npmjs.com/advisories/1523>"
    }
  ],
  "summary": {
    "total_vulnerabilities": 2,
    "critical": 0,
    "high": 1,
    "moderate": 1,
    "low": 0
  }
}

```

### 3. `summary()` Tool

**Purpose**: Return simplified health report combining outdated packages and vulnerabilities

**Implementation Requirements**:

- Calculate a health score (0-100) based on:
    - Number of outdated packages (deduct 2 points each, max 30)
    - Number of vulnerabilities (deduct 5 points each, max 40)
    - Extra penalties for critical (15 points) and high (10 points) severity
- Determine risk level: low/moderate/high/critical
- Generate actionable recommendations

**Expected Output**:

```json
{
  "health_score": 75,
  "risk_level": "moderate",
  "status": "attention_needed",
  "summary": {
    "outdated_packages": 5,
    "total_vulnerabilities": 2,
    "critical_vulnerabilities": 0,
    "high_vulnerabilities": 1
  },
  "recommendations": [
    "Update 5 outdated packages",
    "Fix 1 high-severity vulnerabilities"
  ],
  "last_checked": "now"
}

```

### Key Technical Challenges

1. **Error Handling**: API calls and subprocess commands can fail
2. **Subprocess Management**: Running `pip` and `npm` commands safely
3. **JSON Parsing**: Different tools return different JSON formats
4. **Rate Limiting**: OSV API has rate limits for security queries
5. **Cross-Platform**: Commands work differently on Windows/Mac/Linux

### Scoring Algorithm

```python
health_score = 100
health_score -= min(outdated_packages * 2, 30)  # Max 30 points deducted
health_score -= min(total_vulnerabilities * 5, 40)  # Max 40 points deducted
health_score -= critical_vulnerabilities * 15  # Extra penalty
health_score -= high_vulnerabilities * 10      # Extra penalty
health_score = max(health_score, 0)            # Floor at 0

```

## Testing Your Implementation

### 1. Use MCP Inspector

```bash
npx @modelcontextprotocol/inspector python server.py

```

Open [http://localhost:5173](http://localhost:5173/) and test each tool.

### 2. Test Data

Create projects with intentionally outdated/vulnerable packages:

**Python (`requirements.txt`)**:

```
requests==2.25.1
urllib3==1.26.5
numpy==1.19.0

```

**Node.js (`package.json`)**:

```json
{
  "dependencies": {
    "lodash": "4.17.15",
    "express": "4.16.1",
    "moment": "2.24.0"
  }
}

```

### 3. Expected Behavior

- `list_outdated()` should find multiple outdated packages
- `check_vulnerabilities()` should find known CVEs in old versions
- `summary()` should return a health score < 80 due to outdated packages

### **4. Data source:**

`package.json`, `requirements.txt`, or both.

---