"""Model Context Protocol (MCP) subtopics."""

SUBTOPICS = [
    dict(
        id="what-is-mcp",
        title="What Is MCP & Why It Matters",
        hook="MCP is to AI tools what USB-C is to chargers — one standard plug instead of a different, custom integration for every model and every tool.",
        explanation=(
            "The Model Context Protocol, introduced by Anthropic in late 2024, is an open standard that lets AI "
            "applications connect to external data sources and tools through a single, consistent interface. "
            "Before MCP, every AI app that wanted to read your files, query a database, or call an API had to "
            "build a bespoke integration for that specific tool — an N×M problem where N assistants each needed "
            "custom code for M tools.\n\n"
            "MCP flips this into an N+M problem: a tool builder implements one MCP server, and it instantly works "
            "with any MCP-compatible client (Claude, an IDE, a custom agent) without either side knowing the "
            "other's internals. It's deliberately modeled on the Language Server Protocol (LSP), which solved the "
            "exact same N×M problem for code editors and language tooling a decade earlier."
        ),
        code=dict(
            lang="text",
            label="Before and after MCP",
            src=(
                "Before MCP:\n"
                "  Assistant A <-- custom code --> GitHub\n"
                "  Assistant A <-- custom code --> Slack\n"
                "  Assistant B <-- custom code --> GitHub   (rebuilt from scratch)\n"
                "  Assistant B <-- custom code --> Slack     (rebuilt from scratch)\n\n"
                "After MCP:\n"
                "  Assistant A --\\\n"
                "  Assistant B ---> MCP protocol --> GitHub MCP server\n"
                "  Assistant C --/                --> Slack MCP server"
            ),
        ),
        example=(
            "A company builds one MCP server for its internal ticketing system. That single server now lets "
            "Claude, an internal chatbot, and a VS Code extension all query and update tickets — none of them "
            "needed custom integration code, they only needed to speak MCP."
        ),
        best_practices=[
            "Think of MCP as a contract between two roles: a host/client (the AI application) and a server (the tool or data source) — know which one you're building.",
            "Start from the official MCP specification and SDKs (Python, TypeScript) rather than hand-rolling the protocol.",
            "Design MCP servers around capabilities the model genuinely needs, not a 1:1 wrapper of every API endpoint you have.",
        ],
        pitfalls=[
            "Confusing MCP with a specific product — it's an open protocol, and servers exist for it across many vendors, not just Anthropic's.",
            "Assuming MCP replaces function calling entirely; it standardizes how tools are *discovered and connected*, while the model still decides *when* to call them.",
        ],
        prompts=[
            "How is MCP different from a regular REST API?",
            "Explain the N×M integration problem MCP solves, with a concrete example.",
            "What's the relationship between MCP and the Language Server Protocol?",
        ],
    ),
    dict(
        id="mcp-architecture",
        title="MCP Architecture: Hosts, Clients & Servers",
        hook="Three roles, one protocol — understanding who's who is the fastest way to stop being confused by MCP diagrams.",
        explanation=(
            "MCP defines three roles. The Host is the AI application the person actually uses — Claude Desktop, "
            "an IDE, a custom agent. The Client lives inside the host and manages a 1:1 connection to exactly one "
            "server, handling the protocol handshake and message routing. The Server is the program that exposes "
            "tools, data, or prompts — it could wrap a database, a file system, a SaaS API, or anything else.\n\n"
            "A single host can run many clients simultaneously, each one connected to a different server, which "
            "is why you can connect Claude to a GitHub server, a Google Drive server, and a database server all "
            "at once — the host is coordinating multiple independent client-server pairs, not one big connection."
        ),
        code=dict(
            lang="text",
            label="The 1:1 client-server relationship",
            src=(
                "HOST (e.g. Claude Desktop)\n"
                "  |\n"
                "  |-- Client 1 <--MCP--> Server A (filesystem)\n"
                "  |-- Client 2 <--MCP--> Server B (GitHub)\n"
                "  \\-- Client 3 <--MCP--> Server C (Postgres)\n\n"
                "Each client<->server pair is independent and stateful."
            ),
        ),
        example=(
            "When Claude Desktop is configured with both a filesystem MCP server and a GitHub MCP server, the "
            "host maintains two separate client connections — asking about local files never touches the GitHub "
            "client, and vice versa, even though both appear as available tools in the same conversation."
        ),
        best_practices=[
            "Design servers to be stateless where possible — the client manages the session, not the server's internal assumptions about ordering.",
            "Keep one server focused on one system (one server per API/data source) rather than building a monolithic server that does everything.",
            "Read the initialization handshake carefully when debugging — most early MCP bugs are capability negotiation mismatches, not tool logic bugs.",
        ],
        pitfalls=[
            "Assuming the server can see or influence other servers connected to the same host — servers are isolated from each other by design.",
            "Building a server that requires a specific client implementation instead of following the spec, breaking compatibility with other hosts.",
        ],
        prompts=[
            "Draw out what happens when Claude Desktop connects to two MCP servers at once.",
            "What's the difference between a host and a client in MCP terms?",
            "Why does MCP keep servers isolated from each other?",
        ],
    ),
    dict(
        id="mcp-primitives",
        title="MCP Primitives: Tools, Resources & Prompts",
        hook="Everything an MCP server exposes falls into exactly three categories — and picking the right one for the job is the core design decision when building a server.",
        explanation=(
            "Tools are functions the model can call to take an action or fetch computed data — think "
            "`create_ticket(title, priority)` or `run_query(sql)`. The model decides when to call a tool and "
            "with what arguments, based on its description. Resources are data the host can read and attach to "
            "context, like a file's contents or a database schema — they're more like 'here's something to look "
            "at' than 'do something.' Prompts are reusable, often parameterized templates a server exposes, "
            "letting a host offer a pre-built workflow (like '/summarize-pr') without the model inventing it "
            "from scratch each time.\n\n"
            "The distinction matters because it shapes who's in control: tools put the model in the driver's "
            "seat deciding when to act, resources put the host in control of what context to include, and "
            "prompts put the human in control of triggering a known, curated workflow."
        ),
        code=dict(
            lang="python",
            label="Defining an MCP tool with the Python SDK",
            src=(
                "from mcp.server.fastmcp import FastMCP\n\n"
                "mcp = FastMCP(\"ticket-server\")\n\n"
                "@mcp.tool()\n"
                "def create_ticket(title: str, priority: str = \"medium\") -> str:\n"
                "    \"\"\"Create a support ticket and return its ID.\"\"\"\n"
                "    ticket_id = ticketing_system.create(title=title, priority=priority)\n"
                "    return f\"Created ticket {ticket_id}\"\n\n"
                "@mcp.resource(\"tickets://open\")\n"
                "def list_open_tickets() -> str:\n"
                "    \"\"\"Return currently open tickets as text.\"\"\"\n"
                "    return ticketing_system.list_open()"
            ),
        ),
        example=(
            "A code review MCP server exposes a `get_diff` resource (so the model can see what changed), a "
            "`post_comment` tool (so the model can act on a finding), and a `/review-pr` prompt (so a developer "
            "can trigger the whole reviewing workflow with one command instead of typing a long instruction)."
        ),
        best_practices=[
            "Write tool descriptions the way you'd explain the function to a new teammate — the model relies entirely on that description to decide when to call it.",
            "Keep tool arguments minimal and well-typed; ambiguous or overly flexible parameters lead to more model errors, not more flexibility.",
            "Use resources for anything read-only and reference-like, saving tools for genuine actions or computations.",
        ],
        pitfalls=[
            "Exposing a tool with a vague name and description ('do_thing') that the model calls incorrectly or never calls at all.",
            "Turning every API endpoint into a tool 1:1 instead of designing tools around tasks the model actually needs to accomplish.",
        ],
        prompts=[
            "Should this be an MCP tool or an MCP resource: fetching a user's order history?",
            "Write a good tool description for a function that searches internal documents.",
            "What makes an MCP prompt different from just typing a long instruction?",
        ],
    ),
    dict(
        id="mcp-transports",
        title="MCP Transports: stdio vs. HTTP/SSE",
        hook="MCP separates *what* is being said from *how* it travels — the same tool calls can flow over a local pipe or across the internet.",
        explanation=(
            "MCP messages are JSON-RPC 2.0, but the protocol supports more than one transport for carrying those "
            "messages. stdio (standard input/output) is used when the server runs as a local subprocess of the "
            "host — the client writes JSON-RPC messages to the server's stdin and reads responses from its "
            "stdout. This is simple, fast, and has no network exposure, which is why most local MCP servers "
            "(filesystem access, local databases) use it.\n\n"
            "For remote servers, MCP uses Streamable HTTP (which can use Server-Sent Events for streaming "
            "responses), letting a client connect to a server running anywhere on the network — a company's "
            "internal API, a cloud-hosted tool. The transport is effectively an implementation detail from the "
            "model's perspective; tools, resources, and prompts look identical either way."
        ),
        code=dict(
            lang="python",
            label="Running an MCP server over stdio vs. HTTP",
            src=(
                "# stdio (local subprocess) — most common for local tools\n"
                "if __name__ == \"__main__\":\n"
                "    mcp.run(transport=\"stdio\")\n\n"
                "# Streamable HTTP — for a remotely hosted server\n"
                "if __name__ == \"__main__\":\n"
                "    mcp.run(transport=\"streamable-http\", port=8000)"
            ),
        ),
        example=(
            "A personal 'read my local notes' MCP server runs over stdio since it only ever needs to talk to the "
            "AI app on the same machine, while a company's shared 'query our data warehouse' server runs over "
            "HTTP so every employee's AI client can connect to the one centrally hosted instance."
        ),
        best_practices=[
            "Default to stdio for anything that only needs to run on the user's own machine — it avoids network security concerns entirely.",
            "Put authentication and authorization at the HTTP transport layer for remote servers; never assume the network is trusted.",
            "Version your remote server's endpoint so you can evolve the tool surface without silently breaking existing clients.",
        ],
        pitfalls=[
            "Exposing a remote MCP server without any authentication, letting anyone who finds the URL call its tools.",
            "Choosing HTTP for a purely local tool, adding unnecessary complexity (ports, CORS) for no benefit.",
        ],
        prompts=[
            "When would I choose stdio over HTTP for an MCP server I'm building?",
            "How does authentication typically work for a remote MCP server?",
            "Explain JSON-RPC 2.0 in the context of MCP messages.",
        ],
    ),
    dict(
        id="building-mcp-server",
        title="Building a Minimal MCP Server",
        hook="A working MCP server is often under 30 lines — the protocol handles the hard parts so you can focus on the actual tool logic.",
        explanation=(
            "The fastest way to build an MCP server in Python is the official SDK's `FastMCP` class, which "
            "handles the JSON-RPC handshake, capability negotiation, and message routing for you. You declare "
            "tools and resources as plain Python functions decorated with `@mcp.tool()` or `@mcp.resource()`, "
            "and the SDK derives the tool's schema from your function's type hints and docstring.\n\n"
            "Once written, the server is registered with a host (like Claude Desktop) via a small config entry "
            "pointing at the command to run it. The host launches the server as a subprocess, performs the "
            "handshake automatically, and the tools become available in conversation — no additional wiring "
            "required on the model side."
        ),
        code=dict(
            lang="python",
            label="A complete minimal MCP server",
            src=(
                "# weather_server.py\n"
                "from mcp.server.fastmcp import FastMCP\n"
                "import requests\n\n"
                "mcp = FastMCP(\"weather\")\n\n"
                "@mcp.tool()\n"
                "def get_forecast(city: str) -> str:\n"
                "    \"\"\"Get today's weather forecast for a city.\"\"\"\n"
                "    resp = requests.get(f\"https://api.example-weather.com/{city}\")\n"
                "    data = resp.json()\n"
                "    return f\"{city}: {data['summary']}, {data['temp_c']}C\"\n\n"
                "if __name__ == \"__main__\":\n"
                "    mcp.run(transport=\"stdio\")"
            ),
        ),
        example=(
            "Registering `weather_server.py` in Claude Desktop's config file with the command `python "
            "weather_server.py` is enough for the assistant to start offering weather lookups in conversation — "
            "the entire integration is the 15 lines of tool logic above plus one config entry."
        ),
        best_practices=[
            "Return plain, model-readable text or structured JSON from tools — avoid returning raw binary or deeply nested objects the model has to parse itself.",
            "Handle errors inside the tool and return a clear message rather than letting an unhandled exception crash the server process.",
            "Test the server standalone (calling functions directly) before wiring it into a host, to separate protocol issues from logic bugs.",
        ],
        pitfalls=[
            "Forgetting a docstring on a tool function — the SDK uses it as the tool's description, and a missing one means the model has no idea what the tool does.",
            "Blocking on slow network calls inside a tool without a timeout, freezing the whole conversation while the host waits for a response.",
        ],
        prompts=[
            "Walk me through registering this MCP server in Claude Desktop's config.",
            "How do I add error handling to an MCP tool without crashing the server?",
            "What does the MCP Python SDK generate automatically from my function signature?",
        ],
    ),
]
