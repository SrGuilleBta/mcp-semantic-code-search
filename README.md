# 🔍 MCP Semantic Code Search

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![MCP](https://img.shields.io/badge/Model_Context_Protocol-supported-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

> A local **Model Context Protocol (MCP)** server that empowers AI assistants (like Claude) to intelligently navigate and understand large repositories. 

Instead of dumping entire codebases into the LLM context window, this server implements a **Retrieval-Augmented Generation (RAG)** pipeline using **AST parsing**, **local vector embeddings**, and **ChromaDB** to deliver highly precise code snippets on demand.

---

## ✨ Why this exists?

When working with large codebases, LLMs face strict context limits and keyword-search limitations. This server acts as a "smart librarian" for your AI assistant:

* 🚀 **Zero-Context Bloat:** Feeds the LLM only the exact functions or classes it needs to solve the problem, saving tokens and reducing hallucinations.
* 🧩 **AST-Aware Parsing:** Reads code by its structural logic (functions, classes) rather than arbitrary text chunks.
* 🧠 **Semantic Precision:** Finds code based on *meaning* rather than exact regex matches.
* 🐳 **100% Local:** Runs entirely on your machine via Docker. No code is sent to third-party embedding APIs.
