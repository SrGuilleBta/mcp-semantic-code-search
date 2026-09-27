# 🔍 MCP Semantic Code Search

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![MCP](https://img.shields.io/badge/Model_Context_Protocol-supported-green.svg)

> A local **Model Context Protocol (MCP)** server that empowers AI assistants (like Claude) to intelligently navigate and understand large repositories. 

Instead of dumping entire codebases into the LLM context window, this server implements a **Retrieval-Augmented Generation (RAG)** pipeline using **AST parsing**, **local vector embeddings**, and **ChromaDB** to deliver highly precise code snippets on demand.

---

## ✨ Why this exists?

When working with large codebases, LLMs face strict context limits and keyword-search limitations. This server acts as a "smart librarian" for your AI assistant:

* 🚀 **Zero-Context Bloat:** Feeds the LLM only the exact functions or classes it needs to solve the problem, saving tokens and reducing hallucinations.
* 🧩 **AST-Aware Parsing:** Reads code by its structural logic (functions, classes) rather than arbitrary text chunks.
* 🧠 **Semantic Precision:** Finds code based on *meaning* rather than exact regex matches.
* 🐳 **100% Local:** Runs entirely on your machine via Docker. No code is sent to third-party embedding APIs.

---

## 🚀 Getting started

**1. Build and start the container:**

```bash
docker compose up -d --build
```

Everything (Python, ChromaDB, sentence-transformers) already runs inside the container; your local `./data` folder is mounted in so embeddings persist across restarts.

**2. Connect an MCP client.**

This repo ships a project-scoped [`.mcp.json`](.mcp.json) that tells an MCP client (e.g. Claude Code) to launch the server through the running container:

```json
{
  "mcpServers": {
    "mcp-semantic-code-search": {
      "command": "docker",
      "args": ["compose", "exec", "-T", "mcp-server", "python", "src/server.py"]
    }
  }
}
```

With the container up, start (or restart) a Claude Code session in this project folder and accept the project's MCP configuration when prompted. Any other MCP client that supports launching a local server over stdio can be pointed at the same command.

## 🛠️ Available tools

| Tool | Argument | What it does |
|---|---|---|
| `indexar_repositorio` | `ruta` (path to scan, e.g. `"src"`) | Walks the given directory, extracts every function/class/method with `ast`, and stores them as embeddings in ChromaDB. |
| `buscar_codigo` | `pregunta` (natural-language question) | Runs a semantic search over the indexed code and returns the closest matches with their file, location, and source. |

## 🧪 Running the pieces manually

Each module can also be run directly inside the container, without an MCP client:

```bash
docker compose exec mcp-server python src/parser.py       # parse src/ and print the chunks found
docker compose exec mcp-server python src/vector_db.py     # index + query a small demo file
```

## 🏗️ How it works

1. **`src/parser.py`** — uses Python's built-in `ast` module to extract functions, classes, and methods as intact code chunks (never a snippet cut mid-function), tagged with their file, name, type, and line range.
2. **`src/vector_db.py`** — embeds each chunk with `sentence-transformers` (`all-MiniLM-L6-v2`) and stores it in a persistent ChromaDB collection, keyed by `file_path::name::start_line`. Re-indexing a file updates its chunks and deletes any that no longer exist in the source (renamed/removed functions don't leave stale entries behind).
3. **`src/server.py`** — exposes both steps as MCP tools over stdio, the standard transport for a local, single-user MCP server.

## ⚠️ Known limitations

* Only `.py` files are parsed; `.git`, `__pycache__`, `venv`, `.venv`, `node_modules`, and `data` are skipped when walking a directory.
