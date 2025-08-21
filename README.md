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

A Python package that implements the Model Context Protocol (MCP) to generate meaningful Git commit messages by analyzing repository changes.
</div>

## 🚀 Features

- 🔍 **Smart Change Analysis**: Analyzes Git repository changes to suggest meaningful commit messages
- 📝 **Conventional Commits**: Follows the Conventional Commits specification
- 🛠️ **Git Integration**: Built with GitPython for seamless Git operations
- 🚀 **MCP Server**: Implements the Model Context Protocol for extensibility

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/LuiccianDev/mcp_git_commit_generator.git
   cd mcp_git_commit_generator
   ```

2. Install in development mode:

   ```bash
   pip install -e .
   ```

## 📋 Requirements

- Python 3.13+
- GitPython 3.1.45+
- MCP (Model Context Protocol) 1.12.3+

## 🛠️ Usage

### Running the Server

```bash
python -m mcp_git_commit_generator
```

### Available Options

- `--lite`: Run in lite mode (faster but less detailed analysis)
- `--type`: Specify commit type (feat, fix, docs, etc.)
- `--scope`: Specify commit scope
- `--lite`: Run in lite mode (faster but less detailed analysis)

## 📂 Project Structure

```text
mcp_git_commit_generator/
├── core/                  # Core functionality
│   └── __init__.py
├── tools/                 # MCP tools
│   ├── __init__.py
│   ├── commit_analysis.py  # Commit message generation
│   ├── git_operations.py   # Git operations
│   └── register_tools.py   # Tool registration
├── __init__.py            # Package metadata
├── __main__.py            # CLI entry point
└── server.py              # MCP server implementation
```

## 🧪 Development

### Setup Development Environment

1. Clone the repository and navigate to the project directory
2. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks:

   ```bash
   pre-commit install
   ```

### Code Quality Tools

- **Black**: Code formatting
- **isort**: Import sorting
- **mypy**: Static type checking
- **Ruff**: Linting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

Made with ❤️ for better Git workflows
