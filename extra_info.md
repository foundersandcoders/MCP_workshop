
### **Where the MCP server is created**

```python
mcp = FastMCP("WorkshopServer")
```

This **creates the MCP server instance**.
At this moment:

* A `FastMCP` object is instantiated.
* Internally, it prepares:

  * A registry (like a dictionary) where all tools will be stored.
  * Metadata (the name `"WorkshopServer"`, protocol version, etc.).
  * The server logic that later listens to JSON-RPC requests over stdin/stdout.

So this line **initialises** the server but does **not yet start it**.
Think of it as creating a web server object but not calling `.listen()` yet.

---

### **Where tools are added to the server**

Each function decorated with `@mcp.tool()` is **automatically registered** as a tool in that server’s internal registry.

Example:

```python
@mcp.tool()
def ping() -> dict:
    return {"ok": True, "message": "Server is running"}
```

What happens here:

* The decorator `@mcp.tool()` wraps the `ping()` function.
* During that wrapping, it calls something like `mcp.register_tool(name="ping", fn=ping, schema=...)`.
* The function signature and docstring are inspected to build an **input/output schema** (so the client knows what parameters the tool accepts and what it returns).
* The resulting metadata and reference to the function are stored inside `mcp.tools`, something like:

  ```python
  mcp.tools = {
      "ping": <function ping>,
      "weather": <function weather>,
  }
  ```

So when you decorate, you’re *registering* it into the MCP server instance.

---

### **What happens when you call `mcp.run()`**

```python
if __name__ == "__main__":
    mcp.run()
```

This is where the server **starts running**.

Here’s what happens under the hood:

1. `FastMCP.run()` starts an event loop that listens to **stdin/stdout** (standard input/output).
2. It begins a **JSON-RPC session**, where each message is a request from the MCP client (for example, Claude Desktop or any MCP-compatible LLM client).
3. When the client sends `"list_tools"`, the server responds with the metadata of all registered tools (ping, weather, etc.).
4. When the client calls `"ping"` or `"weather"`, the server:

   * Looks up the tool in its internal registry.
   * Parses the JSON parameters.
   * Executes the corresponding Python function.
   * Returns the result as a JSON-RPC response.

So, calling `mcp.run()` turns your Python script into an **active MCP server process**, ready to receive and handle tool requests.

---

###  **Inside the server: how things are registered**

When you do:

```python 
@mcp.tool()
def ping() -> dict:
    return {"ok": True, "message": "Server is running"}
```

the decorator expands roughly like this under the hood:

```python
def tool(self):
    def decorator(fn):
        # extract function name and docstring
        name = fn.__name__                # "ping"
        description = fn.__doc__          # "Basic liveness check - returns OK status"

        # inspect the function signature to build a schema
        schema = make_json_schema(fn)     # describes input args & return type

        # register it in the internal dictionary
        self.tools[name] = {
            "function": fn,
            "description": description,
            "schema": schema,
        }

        return fn
    return decorator
```

So after registering both ping() and weather(), your MCP instance has this in memory:

```python
mcp.tools = {
  "ping": {
    "function": <function ping at 0x...>,
    "description": "Basic liveness check - returns OK status",
    "schema": {
      "input": {},  # no params
      "output": {"type": "object", "properties": {"ok": ..., "message": ...}}
    }
  },
  "weather": {
    "function": <function weather at 0x...>,
    "description": "Get current weather for a city using Open-Meteo API",
    "schema": {
      "input": {"city": "string"},
      "output": {...}  # depends on what get_weather returns
    }
  }
}
```

This registry is what the client sees when it calls "list_tools".