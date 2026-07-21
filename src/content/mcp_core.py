"""Model Context Protocol (MCP) subtopics — enriched schema."""

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
            "exact same N×M problem for code editors and language tooling a decade earlier.\n\n"
            "Being an open standard (not a single company's proprietary API) is central to MCP's value "
            "proposition — because the specification is public and the SDKs are open source, any company or "
            "individual can build either side (a client or a server) without needing permission or a "
            "commercial partnership, which is what let an ecosystem of MCP servers grow quickly across many "
            "different tools and companies."
        ),
        deep_dive=(
            "MCP's design borrows deliberately from the Language Server Protocol's key insight: standardizing "
            "the *interface* between two categories of software (editors and language tooling, or AI hosts "
            "and external tools) is far more valuable than any single implementation, because it turns a "
            "combinatorial integration problem into a linear one — each new editor (or AI host) just needs to "
            "implement the client side once, and each new language (or tool) just needs to implement the "
            "server side once.\n\n"
            "MCP is transport-agnostic and language-agnostic by design — official SDKs exist for multiple "
            "programming languages, and the protocol itself is defined independently of any specific "
            "implementation language, which is part of why it was able to gain adoption across different "
            "companies' AI products relatively quickly rather than being tied to one company's specific tech "
            "stack.\n\n"
            "It's worth distinguishing MCP (the protocol for connecting AI applications to tools/data) from "
            "function calling (the mechanism, internal to a specific model API, by which a model requests a "
            "tool be invoked) — MCP standardizes the tool *connection and discovery* layer, while the model "
            "still uses its own internal reasoning and function-calling mechanism to decide when and how to "
            "actually invoke an available MCP tool during a conversation."
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
        advanced_code=dict(
            lang="text",
            label="MCP vs. function calling — different layers",
            src=(
                "Function calling:\n"
                "  A model-specific mechanism for a model to REQUEST a tool call\n"
                "  with specific arguments -- part of a given model API's design\n\n"
                "MCP:\n"
                "  A protocol standardizing how tools are DISCOVERED and CONNECTED\n"
                "  to an AI application in the first place\n\n"
                "Together: MCP exposes a tool to the host; the model's own function-calling\n"
                "capability is what decides, mid-conversation, WHEN to actually call it"
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
            "Understand MCP as the connection/discovery layer, distinct from a model's own function-calling mechanism for deciding when to use a tool.",
        ],
        pitfalls=[
            "Confusing MCP with a specific product — it's an open protocol, and servers exist for it across many vendors, not just Anthropic's.",
            "Assuming MCP replaces function calling entirely; it standardizes how tools are *discovered and connected*, while the model still decides *when* to call them.",
            "Building a tightly coupled, non-standard integration when an existing MCP server for that tool already exists.",
        ],
        glossary=[
            dict(term="N×M problem", definition="The combinatorial integration burden of N AI applications each needing custom code for M different tools, which MCP reduces to an N+M problem."),
            dict(term="LSP (Language Server Protocol)", definition="An earlier open standard solving the same N×M problem for code editors and programming language tooling, which directly inspired MCP's design."),
            dict(term="Function calling", definition="A model-specific mechanism for a model to request a specific tool be invoked with specific arguments, distinct from MCP's connection/discovery layer."),
        ],
        faq=[
            dict(q="How is MCP different from a regular REST API?", a="A REST API is one specific service's interface, requiring custom integration code for each consumer. MCP is a standardized protocol layer sitting on top of (or wrapping) any backend — once a server speaks MCP, any MCP-compatible AI application can discover and use its tools without custom integration code."),
            dict(q="Explain the N×M integration problem MCP solves, with a concrete example.", a="If 5 different AI assistants each want to integrate with 10 different tools, that's potentially 50 separate custom integrations without a standard. With MCP, each tool builds one server (10 total) and each assistant builds one client capability (5 total) — 15 total pieces of integration work instead of 50."),
            dict(q="What's the relationship between MCP and the Language Server Protocol?", a="MCP was deliberately modeled on LSP's core insight — standardize the interface between two categories of software rather than building point-to-point integrations — applied to AI applications and external tools instead of code editors and language tooling."),
        ],
        quiz=[
            dict(
                question="What problem does MCP primarily solve?",
                options=["Making AI models smarter", "The combinatorial cost of custom integrations between many AI apps and many tools", "Reducing the size of AI models", "Encrypting AI conversations"],
                correct=1,
                explanation="MCP standardizes the connection between AI applications and external tools, turning an N×M custom-integration problem into an N+M standardized one.",
            ),
        ],
        prompts=[
            "How is MCP different from a regular REST API?",
            "Explain the N×M integration problem MCP solves, with a concrete example.",
            "What's the relationship between MCP and the Language Server Protocol?",
            "What's the difference between MCP and a model's function-calling mechanism?",
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
            "at once — the host is coordinating multiple independent client-server pairs, not one big connection.\n\n"
            "The initialization handshake, run once when a client first connects to a server, exchanges "
            "protocol version information and capability declarations — the server tells the client which "
            "primitives it supports (tools, resources, prompts, or some combination), and the client "
            "similarly declares what it supports, so both sides know what's actually available before any "
            "real work happens."
        ),
        deep_dive=(
            "Servers are deliberately isolated from each other by design — a GitHub MCP server has no "
            "visibility into, or ability to influence, a separately connected Google Drive MCP server, even "
            "though both are connected to the same host in the same conversation. This isolation is a "
            "security and architectural feature, not a limitation to work around: it means a compromised or "
            "buggy server can't reach into unrelated servers' data or capabilities.\n\n"
            "The host is responsible for aggregating capabilities from all its connected servers and "
            "presenting them to the underlying AI model in a unified way — from the model's perspective "
            "during a conversation, it typically just sees 'available tools,' without needing to know which "
            "specific server or connection each tool came from; that routing is the host's job.\n\n"
            "Capability negotiation during the handshake matters for backward and forward compatibility: as "
            "the MCP specification evolves and adds new primitives or features, a client and server "
            "implementing different versions can still interoperate on whatever capabilities they mutually "
            "support, rather than requiring every part of the ecosystem to upgrade in lockstep."
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
        advanced_code=dict(
            lang="text",
            label="The initialization handshake, conceptually",
            src=(
                "1. Client connects to Server\n"
                "2. Client sends: \"initialize\" with its protocol version + supported capabilities\n"
                "3. Server responds with: its own protocol version + which primitives it supports\n"
                "   (tools? resources? prompts? some combination?)\n"
                "4. Client sends: \"initialized\" to confirm handshake is complete\n"
                "5. Normal operation begins -- client can now call list_tools, call_tool, etc."
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
            "Rely on the host's capability aggregation rather than trying to make servers aware of each other — isolation is deliberate.",
        ],
        pitfalls=[
            "Assuming the server can see or influence other servers connected to the same host — servers are isolated from each other by design.",
            "Building a server that requires a specific client implementation instead of following the spec, breaking compatibility with other hosts.",
            "Skipping proper handshake/capability handling, causing subtle incompatibilities with clients or servers on different protocol versions.",
        ],
        glossary=[
            dict(term="Host", definition="The AI application a person actually uses (like Claude Desktop or an IDE), which coordinates one or more MCP clients."),
            dict(term="Client", definition="The component inside a host managing a 1:1 stateful connection to exactly one MCP server."),
            dict(term="Server", definition="The program exposing tools, resources, and/or prompts to a connected client, wrapping a specific data source or system."),
            dict(term="Capability negotiation", definition="The handshake process where client and server exchange protocol version and supported feature information."),
        ],
        faq=[
            dict(q="Draw out what happens when Claude Desktop connects to two MCP servers at once.", a="Claude Desktop (the host) runs two separate clients, each independently connected to one server — Client 1 to Server A, Client 2 to Server B. Each connection has its own handshake and state; the host aggregates both servers' capabilities into one unified set of tools available in the conversation."),
            dict(q="What's the difference between a host and a client in MCP terms?", a="The host is the overall AI application the user interacts with. A client is a specific component within that host managing one connection to one specific server — a single host commonly runs multiple clients simultaneously, one per connected server."),
            dict(q="Why does MCP keep servers isolated from each other?", a="Isolation is a deliberate security and architectural boundary — it means a bug or compromise in one server can't reach into another server's data or capabilities, even though both are connected to the same host in the same session."),
        ],
        quiz=[
            dict(
                question="Can a GitHub MCP server directly access data from a separately connected Google Drive MCP server in the same host?",
                options=["Yes, they share a common data pool", "No, servers are isolated from each other by design", "Only if explicitly configured to share", "Only the host can decide, per conversation"],
                correct=1,
                explanation="MCP servers are deliberately isolated from one another; the host coordinates multiple independent client-server connections without letting them see or influence each other.",
            ),
        ],
        prompts=[
            "Draw out what happens when Claude Desktop connects to two MCP servers at once.",
            "What's the difference between a host and a client in MCP terms?",
            "Why does MCP keep servers isolated from each other?",
            "Explain what happens during the MCP initialization handshake.",
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
            "prompts put the human in control of triggering a known, curated workflow.\n\n"
            "A single MCP server commonly exposes a mix of all three — a GitHub server might offer "
            "`create_issue` and `merge_pull_request` as tools, expose the contents of a specific file as a "
            "resource, and provide a `/review-pr` prompt template that bundles a well-crafted instruction "
            "together with a reference to the relevant diff resource."
        ),
        deep_dive=(
            "Tool descriptions function as the model's entire understanding of what a tool does and when to "
            "use it — there's no other channel of information, so a vague or misleading description directly "
            "translates into the model calling the wrong tool, or the right tool with wrong arguments, "
            "regardless of how well the underlying function is actually implemented.\n\n"
            "Resources support subscriptions in the MCP spec, letting a client register interest in a "
            "resource and receive notifications when it changes — useful for keeping a host's view of, say, a "
            "frequently-updated log file or dashboard current without needing to poll repeatedly.\n\n"
            "Prompts differ from simply typing a long instruction because they're discoverable and "
            "structured — a host can present a list of a server's available prompts to the user (like a "
            "menu of pre-built workflows), and a prompt template can accept typed parameters, letting the "
            "host build a form-like interface around it rather than requiring the user to remember and "
            "correctly type out a complex instruction from scratch every time."
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
        advanced_code=dict(
            lang="python",
            label="A parameterized prompt template",
            src=(
                "@mcp.prompt()\n"
                "def review_pr(pr_number: int) -> str:\n"
                "    \"\"\"Generate a code review prompt for a specific pull request.\"\"\"\n"
                "    return (\n"
                "        f\"Review pull request #{pr_number}. Check for: \"\n"
                "        f\"1) obvious bugs, 2) missing tests, 3) unclear naming. \"\n"
                "        f\"Be specific and reference line numbers where possible.\"\n"
                "    )\n\n"
                "# A host can present this as a discoverable, parameterized command,\n"
                "# e.g. a \"/review-pr 42\" slash command in a chat interface"
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
            "Use prompts for well-known, repeatable workflows you want to make discoverable and easy to trigger consistently.",
        ],
        pitfalls=[
            "Exposing a tool with a vague name and description ('do_thing') that the model calls incorrectly or never calls at all.",
            "Turning every API endpoint into a tool 1:1 instead of designing tools around tasks the model actually needs to accomplish.",
            "Missing a docstring on a tool function, leaving the model with no description to reason from at all.",
        ],
        glossary=[
            dict(term="Tool", definition="A function an MCP server exposes that the model can decide to call to take an action or fetch computed data."),
            dict(term="Resource", definition="Read-only data an MCP server exposes that a host can attach to context, like a file's contents or a schema."),
            dict(term="Prompt (MCP primitive)", definition="A reusable, discoverable, potentially parameterized instruction template a server exposes for triggering a known workflow."),
        ],
        faq=[
            dict(q="Should this be an MCP tool or an MCP resource: fetching a user's order history?", a="If it's purely informational, read-only context for the model to consider, it fits well as a resource. If the model needs to actively decide, mid-conversation, to fetch it based on the flow of the conversation (rather than it being provided upfront), a tool is often the better fit — the line can be genuinely context-dependent."),
            dict(q="Write a good tool description for a function that searches internal documents.", a="Something like: 'Search the company's internal knowledge base for documents matching a query. Returns titles and short excerpts of the top matches. Use this when the user asks about internal policies, processes, or documentation you don't already have in context.' — specific about what it does and when to use it."),
            dict(q="What makes an MCP prompt different from just typing a long instruction?", a="A prompt is discoverable (a host can list it as an available command) and can accept structured, typed parameters — letting a host build a menu or form-like interface around it, and ensuring the underlying instruction stays consistent every time it's triggered, rather than being retyped and potentially varying each time."),
        ],
        quiz=[
            dict(
                question="What determines when and whether a model calls a specific MCP tool?",
                options=["A fixed schedule", "The tool's name and description, which the model reasons about", "Random selection", "The host always decides for the model"],
                correct=1,
                explanation="The model decides whether to call a tool based entirely on its name, description, and parameter schema — there's no other channel telling the model what a tool does or when it's appropriate.",
            ),
        ],
        prompts=[
            "Should this be an MCP tool or an MCP resource: fetching a user's order history?",
            "Write a good tool description for a function that searches internal documents.",
            "What makes an MCP prompt different from just typing a long instruction?",
            "Design the tools, resources, and prompts for an MCP server wrapping a calendar app.",
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
            "model's perspective; tools, resources, and prompts look identical either way.\n\n"
            "Choosing between them is mostly determined by where the server needs to run: if it only ever "
            "needs to run on the same machine as the host application (reading local files, running local "
            "commands), stdio is simpler and inherently more secure since there's no network attack surface. "
            "If the server needs to be shared across multiple users or machines, or wraps a resource that "
            "genuinely lives remotely (a cloud database, a SaaS API), HTTP is the appropriate choice."
        ),
        deep_dive=(
            "stdio's simplicity comes from piggybacking on the operating system's process management — the "
            "host launches the server as a child process, and the OS handles cleanup automatically if either "
            "side exits, without MCP needing to implement its own connection lifecycle management for that "
            "case.\n\n"
            "For remote HTTP-based servers, authentication becomes the host application and server's "
            "responsibility to implement correctly (MCP itself doesn't mandate one specific auth scheme) — "
            "common approaches include API keys, OAuth tokens, or session-based authentication, layered at "
            "the HTTP transport level rather than being part of the MCP message format itself.\n\n"
            "Server-Sent Events (SSE), used for streaming responses over HTTP, let a server send a sequence of "
            "incremental updates over a single long-lived HTTP connection — useful for tool calls that produce "
            "output progressively (like a long-running search or computation) rather than a single, complete "
            "response returned all at once."
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
        advanced_code=dict(
            lang="text",
            label="Deciding stdio vs. HTTP for a new server",
            src=(
                "Does the server ONLY need to run on the same machine as the host?\n"
                "  YES -> stdio (simpler, no network exposure, OS handles lifecycle)\n"
                "  NO  -> HTTP (streamable-http), and now you must also handle:\n"
                "         - authentication (API keys, OAuth, ...)\n"
                "         - authorization (who can call which tools)\n"
                "         - network security (TLS, rate limiting)"
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
            "Use SSE-based streaming for tool calls that produce output progressively, rather than making the client wait for one large final response.",
        ],
        pitfalls=[
            "Exposing a remote MCP server without any authentication, letting anyone who finds the URL call its tools.",
            "Choosing HTTP for a purely local tool, adding unnecessary complexity (ports, CORS) for no benefit.",
            "Forgetting that MCP itself doesn't mandate a specific auth scheme for HTTP — it's the implementer's responsibility to add appropriate security.",
        ],
        glossary=[
            dict(term="stdio transport", definition="Carrying MCP JSON-RPC messages over a local subprocess's standard input/output, used for servers running on the same machine as the host."),
            dict(term="Streamable HTTP transport", definition="Carrying MCP messages over HTTP, optionally using Server-Sent Events for streaming, used for remotely hosted servers."),
            dict(term="JSON-RPC 2.0", definition="The message format MCP uses for requests and responses, independent of which transport carries those messages."),
        ],
        faq=[
            dict(q="When would I choose stdio over HTTP for an MCP server I'm building?", a="Whenever the server only needs to run on the same machine as the host application — reading local files, running local scripts, accessing local hardware. It's simpler to implement and has no network attack surface to secure."),
            dict(q="How does authentication typically work for a remote MCP server?", a="MCP itself doesn't mandate a specific scheme — it's implemented at the HTTP transport layer using standard approaches like API keys, OAuth tokens, or session-based authentication, the same as securing any other HTTP API."),
            dict(q="Explain JSON-RPC 2.0 in the context of MCP messages.", a="JSON-RPC 2.0 is a lightweight, standardized format for requests and responses (a method name, parameters, and an ID for matching responses to requests). MCP uses this format for its messages regardless of which transport (stdio or HTTP) actually carries them."),
        ],
        quiz=[
            dict(
                question="Which transport is generally preferred for an MCP server that only ever runs on the user's own machine?",
                options=["HTTP with OAuth", "stdio", "FTP", "WebSockets exclusively"],
                correct=1,
                explanation="stdio avoids network exposure entirely and relies on the OS's process management, making it the simpler and inherently more secure choice for purely local servers.",
            ),
        ],
        prompts=[
            "When would I choose stdio over HTTP for an MCP server I'm building?",
            "How does authentication typically work for a remote MCP server?",
            "Explain JSON-RPC 2.0 in the context of MCP messages.",
            "What security considerations apply specifically to an HTTP-based MCP server?",
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
            "required on the model side.\n\n"
            "Testing a server before wiring it into a full host application is straightforward since the "
            "underlying functions are just plain Python — call them directly in a script or test file to "
            "verify the logic works correctly, entirely separate from testing the actual MCP protocol "
            "handling, which the SDK is responsible for and doesn't need to be re-tested by every server "
            "author."
        ),
        deep_dive=(
            "Error handling inside a tool matters more than in typical application code, because an unhandled "
            "exception doesn't just fail silently in a log file — it can crash the server process entirely, "
            "taking down every other tool that server exposes for the rest of the conversation. Wrapping risky "
            "operations in try/except and returning a clear, model-readable error message keeps a single "
            "failed operation from becoming a total outage for that server.\n\n"
            "Return values from tools should generally be plain text or simply structured data (like JSON) "
            "that a model can straightforwardly interpret and reason about — returning something like a raw "
            "binary object or an overly deeply nested structure makes it harder for the model to extract the "
            "actually relevant information.\n\n"
            "As a server grows beyond a handful of tools, organizing them into logical groups (multiple "
            "smaller, focused servers rather than one large one covering many unrelated systems) tends to "
            "produce clearer tool descriptions and an easier mental model for both the developer and, "
            "ultimately, the AI model deciding which tool to call for a given task."
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
        advanced_code=dict(
            lang="python",
            label="Adding error handling so one bad call doesn't crash the server",
            src=(
                "@mcp.tool()\n"
                "def get_forecast(city: str) -> str:\n"
                "    \"\"\"Get today's weather forecast for a city.\"\"\"\n"
                "    try:\n"
                "        resp = requests.get(\n"
                "            f\"https://api.example-weather.com/{city}\", timeout=10\n"
                "        )\n"
                "        resp.raise_for_status()\n"
                "        data = resp.json()\n"
                "        return f\"{city}: {data['summary']}, {data['temp_c']}C\"\n"
                "    except requests.exceptions.RequestException as e:\n"
                "        return f\"Couldn't fetch weather for {city}: {e}\"   # readable, doesn't crash"
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
            "Split a growing server into multiple smaller, logically grouped servers rather than one large server covering many unrelated systems.",
        ],
        pitfalls=[
            "Forgetting a docstring on a tool function — the SDK uses it as the tool's description, and a missing one means the model has no idea what the tool does.",
            "Blocking on slow network calls inside a tool without a timeout, freezing the whole conversation while the host waits for a response.",
            "Letting an unhandled exception inside one tool crash the entire server process, taking down every other tool it exposes.",
        ],
        glossary=[
            dict(term="FastMCP", definition="A high-level class in the official Python MCP SDK that handles protocol details automatically, letting you define tools/resources as plain decorated functions."),
            dict(term="Tool schema", definition="The structured description (name, parameters, types) of a tool, automatically derived from a Python function's type hints and docstring in FastMCP."),
        ],
        faq=[
            dict(q="Walk me through registering this MCP server in Claude Desktop's config.", a="Add an entry to Claude Desktop's config file (typically claude_desktop_config.json) under mcpServers, specifying a name and the command to launch your server (e.g. python weather_server.py). Restart Claude Desktop, and the server's tools become available in conversation."),
            dict(q="How do I add error handling to an MCP tool without crashing the server?", a="Wrap the risky logic (network calls, file I/O, anything that could raise) in a try/except inside the tool function, and return a clear, readable error message string on failure instead of letting the exception propagate up and potentially crash the whole server process."),
            dict(q="What does the MCP Python SDK generate automatically from my function signature?", a="FastMCP derives the tool's parameter schema from your function's type hints, and uses your docstring as the tool's description — both of which the AI model relies on to understand what the tool does and how to call it correctly."),
        ],
        quiz=[
            dict(
                question="Why is error handling especially important inside an MCP tool function?",
                options=["It's not actually important", "An unhandled exception can crash the entire server process, taking down every tool it exposes", "It only affects that one tool call's response time", "MCP automatically retries failed tools"],
                correct=1,
                explanation="Unlike typical application code where an error might just fail one request, an unhandled exception in a tool can crash the whole server process, disabling every tool it provides for the remainder of the session.",
            ),
        ],
        prompts=[
            "Walk me through registering this MCP server in Claude Desktop's config.",
            "How do I add error handling to an MCP tool without crashing the server?",
            "What does the MCP Python SDK generate automatically from my function signature?",
            "Help me split this large MCP server into smaller, focused ones.",
        ],
    ),
]