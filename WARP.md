# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is an **MCP (Model Context Protocol) server** that generates conventional commit messages by analyzing Git repository changes. It's written in Python 3.13+ and implements both basic Git operations and optimized tools for commit message generation.

### Core Architecture

The project follows a clean modular architecture:

- **`src/mcp_git_commit_generator/`**: Main package
    - **`core/models.py`**: Pydantic data models and enums for all Git operations
    - **`tools/`**: MCP tool implementations
        - `git_operations.py`: Basic Git commands (status, diff, commit, etc.)
        - `commit_analysis.py`: Specialized commit message generation and optimized status
        - `register_tools.py`: Tool registration and routing logic
    - **`main.py`**: Clean server implementation using the modular tools
    - **`server.py`**: Legacy unified server (contains duplicate functionality)

### Key Technical Details

- **Dual server implementations**: Both `main.py` (clean/modular) and `server.py` (legacy/unified) provide the same functionality
- **GitPython integration**: Uses GitPython library for Git operations instead of shell commands
- **Conventional commits**: Specialized in generating commit messages following the Conventional Commits specification
- **Performance optimization**: Includes "lite mode" for faster analysis by skipping full diff generation

## Development Commands

### Environment Setup

```bash
# Install in development mode with all dependencies
pip install -e ".[dev,test]"

# Install pre-commit hooks
pre-commit install
```

### Running the Server

```bash
# Main way to run the MCP server
python -m mcp_git_commit_generator

# Alternative direct execution
python src/mcp_git_commit_generator/main.py
python src/mcp_git_commit_generator/server.py
```

### Code Quality & Testing

```bash
# Run pre-commit hooks manually on all files
pre-commit run --all-files

# Clean and update pre-commit
pre-commit clean
pre-commit autoupdate

# Run tests
pytest

# Run a specific test file
pytest tests/test_commit_analysis.py
pytest tests/test_git_operations.py

# Type checking
mypy src

# Linting and formatting
ruff check src
ruff format src
```

### Pre-commit Workflow

This project uses pre-commit hooks extensively. The typical workflow is:

```bash
# Stage your changes
git add .

# Run pre-commit (will auto-fix many issues)
pre-commit run --all-files

# If there were fixes, re-stage
git add .

# Commit your changes
git commit -m "feat: your change description"
```

## MCP Tools Available

The server provides these Git tools via MCP:

### Basic Git Operations

- `git_status`, `git_add`, `git_commit`, `git_reset`
- `git_diff`, `git_diff_staged`, `git_diff_unstaged`
- `git_log`, `git_show`, `git_branch`
- `git_checkout`, `git_create_branch`, `git_init`

### Specialized Tools

- **`generate_commit_message`**: Analyzes staged changes and provides conventional commit guidance
- **`git_optimized_status`**: Fast status check with commit-ready indicators

## Configuration Files

### Code Quality Stack

- **Ruff** (`ruff.toml`): Primary linter and formatter (replaces Black + isort + flake8)
    - Target: Python 3.13
    - Line length: 88 characters
    - Excludes tests from most checks
- **mypy** (`mypy.ini`): Type checking with strict settings
- **pytest** (`pytest.ini`): Test configuration with async support

### Pre-commit Configuration

The `.pre-commit-config.yaml` runs:

1. Ruff for linting and auto-fixes
2. mypy for type checking
3. Basic file cleanup (trailing whitespace, EOF, YAML/JSON validation)

All tools target Python 3.13 and only check `src/` directory files.

## Development Notes

### Architecture Decision

The codebase has two server implementations:

- **`main.py`** (recommended): Uses modular tool architecture from `tools/` package
- **`server.py`** (legacy): Contains all functionality in one file

When making changes, prefer updating the modular version in `main.py` and the `tools/` package.

### Key Dependencies

- **gitpython**: Git operations library
- **mcp**: Model Context Protocol implementation
- **pydantic**: Data validation and models

### Testing Strategy

- Tests are located in `tests/` directory
- Uses pytest with asyncio support
- Test files follow `test_*.py` naming convention
- Configured to find source code via `pythonpath = src`

<citations>
<document>
<document_type>WARP_DRIVE_NOTEBOOK</document_type>
<document_id>etaUSllWB1MSoK6JwHfnbr</document_id>
</document>
<document>
<document_type>WARP_DRIVE_NOTEBOOK</document_type>
<document_id>cr1ZH3ZmThpjb8axAI1HYa</document_id>
</document>
</citations>
