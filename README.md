# MCP Git Commit Generator

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

A Model Context Protocol (MCP) server that helps generate conventional commit messages by analyzing Git repository changes.

## 🚀 Features

- 🔍 **Smart Change Analysis**: Analyzes staged changes to suggest meaningful commits
- 📝 **Conventional Commits**: Follows the Conventional Commits specification
- 🛠️ **Git Integration**: Seamless integration with Git repositories
- 🚀 **MCP Server**: Implements the Model Context Protocol for extensibility

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mcp-git-commit-generator.git
   cd mcp-git-commit-generator
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

## 🛠️ Usage

### Running the Server

```bash
python -m mcp_git_commit_generator
```

### Available Options

- `--lite`: Run in lite mode (faster but less detailed analysis)
- `--type`: Specify commit type (feat, fix, docs, etc.)
- `--scope`: Specify commit scope

## 📂 Project Structure

```
src/
├── mcp_git_commit_generator/
│   ├── core/              # Core functionality
│   │   ├── __init__.py
│   │   └── models.py      # Data models
│   ├── tools/             # MCP tools
│   │   ├── __init__.py
│   │   ├── commit_analysis.py  # Commit message generation
│   │   ├── git_operations.py   # Git operations
│   │   └── register_tools.py   # Tool registration
│   ├── __init__.py
│   ├── main.py            # Main server implementation
│   └── server.py          # Server configuration
```

## 🧪 Development

### Setup Development Environment

1. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

2. Install pre-commit hooks:
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

## 📝 Todo

- [ ] Add more test cases
- [ ] Implement CI/CD pipeline
- [ ] Add comprehensive documentation

---

Made with ❤️ for better Git workflows
