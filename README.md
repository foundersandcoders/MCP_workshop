# 🧰 Developer MCP Server — Pre-Lunch Workshop

## 1️⃣ Choose your server type

Open `config.json` and set:

```json
{
  "server_name": "TeamServer",
  "option": "git_insight",      // or "dep_health" or "proj_map"
  "workdir": "./data/sample_repo"
}
```

* `git_insight` → analyze commits and authors
* `dep_health` → check dependencies & vulnerabilities
* `proj_map` → explore project structure

You can use the provided sample repo (./data/sample_repo)
or point "workdir" to any local project folder on your machine.
For example:

```json
"workdir": "/Users/you/dev/my-project"
```

---

## 2️⃣ Set up your environment

Create and activate a virtual environment in the project folder:

```bash
python -m venv .venv
source .venv/bin/activate
```

* Use `python3` instead of `python` if your system requires it.
* On Windows PowerShell run: `python -m venv .venv; .\.venv\Scripts\Activate`.
* In VS Code select the `.venv` interpreter when prompted.

Install `fastmcp` inside the virtual environment:

```bash
pip install fastmcp
```

---

## 3️⃣ Initialize sample repo (optional)

If you don’t have a repo ready:

```bash
bash scripts/init_sample_repo.sh
```

Then set in `config.json`:

```json
"workdir": "./data/sample_repo"
```

---

## 4️⃣ Run and test in MCP Inspector

### A. Launch Inspector

```bash
npx @modelcontextprotocol/inspector python server.py
```
```bash
npx @modelcontextprotocol/inspector python3 server.py
```

Inspector opens at **[http://localhost:5173](http://localhost:5173)**.
You’ll see your server name and list of tools.


**If the previous Inspector instance gets stuck:**

macOS/Linux:

```pkill -f "@modelcontextprotocol/inspector"```


Windows PowerShell:

```Get-Process | Where-Object { $_.Path -like "*@modelcontextprotocol*" } | Stop-Process```

In the Inspector connection form set **Server Command** to `python` (or `python3`).


### B. Verify connection

1. Run **`ping`** → should return `{ "ok": true, ... }`.
2. Call one of your option tools:

   * **git_insight:** `git_list_commits`, `git_top_authors`
   * **dep_health:** `deps_list_outdated`, `deps_vulnerabilities`
   * **proj_map:** `pm_list_directories`, `pm_count_filetypes`

### C. If Inspector doesn’t auto-launch

Run the server manually:

```bash
python server.py
```

Then in Inspector:

* **Server Command:** `python`
* **Arguments:** `server.py`
* Click **Connect**

---

✅ **Goal:** By lunch, your MCP server returns valid JSON for at least two tools.
Another team should be able to connect and call your tools in Inspector.
