<div align="center">
   <h1>MCP Git Commit Generator</h1>

   <p>
      <em>Powerful Git commit message generator using the Model Context Protocol (MCP)</em>
   </p>

   [![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
   [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
   [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
   [![Type checking: mypy](https://img.shields.io/badge/mypy-checked-blue.svg)](http://mypy-lang.org/)
   [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
   [![GitPython](https://img.shields.io/badge/GitPython-3.1%2B-orange)](https://gitpython.readthedocs.io/en/stable/)
   [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
   [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Python package implementing the Model Context Protocol (MCP) to generate meaningful Git commit messages by analyzing repository changes.
</div>

---

## 🚀 Overview

MCP Git Commit Generator is a Python package that leverages the Model Context Protocol (MCP) to analyze your Git repository and generate conventional, context-aware commit messages. It supports multiple deployment modes and integrates seamlessly with DXT and MCP environments.

---

## 🛠️ Tool Reference

For a complete list of available tools and their input schemas, see [TOOLS.md](./TOOLS.md).

---

## 📦 Installation

### Prerequisites

- **Python 3.11+** (with type hints)
- **UV Package Manager** ([Install UV](https://docs.astral.sh/uv/getting-started/installation/)) or use pip
- **Git** (for repository operations)
- **Desktop Extensions (DXT)** ([Install DXT](https://github.com/anthropics/dxt)) for packaging .dxt files for Claude Desktop

### Clone the Repository

```bash
git clone https://github.com/LuiccianDev/mcp_git_commit_generator.git
cd mcp_git_commit_generator
```

### Install in Development Mode

```bash
pip install -e .
```

---

## 📂 Project Structure

```text
mcp_git_commit_generator/
├── src/
│   ├── core/                  # Core logic and utilities
│   │   └── __init__.py
│   ├── tools/                 # MCP tool implementations
│   │   ├── __init__.py
│   │   ├── commit_analysis.py  # Commit message generation logic
│   │   ├── git_operations.py   # Git repository operations
│   │   └── register_tools.py   # Tool registration for MCP
│   ├── __init__.py            # Package metadata
│   ├── __main__.py            # CLI entry point
│   └── server.py              # MCP server implementation
├── tests/                     # Unit and integration tests
│   └── test_commit_analysis.py
├── manifest.json              # DXT packaging manifest
├── TOOLS.md                   # Tool reference documentation
└──README.md                  # Project documentation
```

---

## 🧪 Development

### Setup Development Environment

1. Clone the repository and navigate to the project directory.
2. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks:

   ```bash
   pre-commit install
   ```

---

## ⚙️ Deployment Modes

MCP Git Commit Generator Server supports three deployment modes to fit different workflows and environments:

### DXT Package Deployment

**Recommended for:** Users in the DXT ecosystem who want seamless configuration management.

1. **Package the project:**

   ```bash
   dxt pack
   ```

2. **Usage:** Once packaged, the tool integrates directly with DXT-compatible clients with automatic user configuration variable substitution.

3. **Server Configuration:** This project includes [manifest.json](./manifest.json) for building the .dxt package.

For more details, see [DXT Package Documentation](https://github.com/anthropics/dxt).

### Traditional MCP Server

**Recommended for:** Standard MCP server deployments with existing MCP infrastructure.

Add to your MCP configuration file (e.g., Claude Desktop's `mcp_config.json`):

```bash
# Build packages
uv build
# Install packages
pip install dist/your_package*.whl
```

Then configure MCP:

```json
{
  "mcpServers": {
    "mcp_git_commit": {
      "command": "uv",
      "args": ["run", "mcp_git_commit"]
    }
  }
}
```

Or use this configuration (less recommended):

```json
{
   "mcp-word": {
      "command": "/Users/user/to/repo/.venv/Scripts/python",
      "args": [
        "/Users/user/to/repo/src/mcp_git_commit_generator/server.py"
      ]
   }
}
```

---

## 🤝 Contributing

Contributions are welcome! Please read the contribution guidelines before submitting pull requests.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <p><strong>MCP Git Commit Generator Server</strong></p>
  <p>Empowering AI assistants with comprehensive Git commit generation capabilities</p>
  <p>
    <a href="https://github.com/LuiccianDev/mcp_git_commit_generator">🏠 GitHub</a> •
    <a href="https://modelcontextprotocol.io">🔗 MCP Protocol</a> •
    <a href="https://github.com/LuiccianDev/mcp_git_commit_generator/blob/main/TOOLS.md">📚 Tool Documentation</a>
  </p>
  <p><em>Created by LuiccianDev</em></p>
</div>
