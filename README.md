# MCP Server Workshop

## Test with MCP Inspector

Launch Inspector:

```bash
npx @modelcontextprotocol/inspector python server.py
```

Inspector automatically opens at [http://localhost:5173](http://localhost:5173)

Test the tools:
1. Run `ping` → returns `{"ok": true, "message": "Server is running"}`
2. Run `weather` with a city name (e.g., "London")

## Troubleshooting

If Inspector gets stuck:

```bash
# macOS/Linux
pkill -f "@modelcontextprotocol/inspector"

# Windows
Get-Process | Where-Object { $_.Path -like "*@modelcontextprotocol*" } | Stop-Process
```