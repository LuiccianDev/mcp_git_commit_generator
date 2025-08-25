# MCP Git Commit Generator - Available Tools

This document lists all the Git tools available in the MCP Git Commit Generator project.

## Basic Git Operations

### `git_status`

- **Description**: Shows the working tree status
- **Input Schema**:

  ```json
  {
    "repo_path": "string"
  }
  ```

### `git_diff_unstaged`

- **Description**: Shows changes in the working directory that are not yet staged
- **Input Schema**:

  ```json
  {
    "repo_path": "string",
    "context_lines": 3
  }
  ```

### `git_diff_staged`

- **Description**: Shows changes that are staged for commit
- **Input Schema**:

  ```json
  {
    "repo_path": "string",
    "context_lines": 3
  }
  ```

### `git_diff`

- **Description**: Shows differences between branches or commits
- **Input Schema**:

  ```json
  {
    "repo_path": "string",
    "target": "string",
    "context_lines": 3
  }
  ```

### `git_commit`

- **Description**: Records changes to the repository
- **Input Schema**:

  ```json
  {
    "repo_path": "string",
    "message": "string"
  }
  ```

### `git_add`

- **Description**: Adds file contents to the staging area
- **Input Schema**:

  ```json
  {
    "repo_path": "string",
    "files": ["string"]
  }
  ```

### `git_reset`

- **Description**: Unstages all staged changes
- **Input Schema**:

  ```json
  {
    "repo_path": "string"
  }
  ```

### `git_log`

- **Description**: Shows the commit logs
- **Input Schema**:

  ```json
  {
    "repo_path": "string",
    "max_count": 10
  }
  ```

### `git_create_branch`

- **Description**: Creates a new branch from an optional base branch
- **Input Schema**:

  ```json
  {
    "repo_path": "string",
    "branch_name": "string",
    "base_branch": "string"
  }
  ```

### `git_checkout`

- **Description**: Switches branches
- **Input Schema**:

  ```json
  {
    "repo_path": "string",
    "branch_name": "string"
  }
  ```

### `git_show`

- **Description**: Shows the contents of a commit
- **Input Schema**:

  ```json
  {
    "repo_path": "string",
    "revision": "string"
  }
  ```

### `git_init`

- **Description**: Initialize a new Git repository
- **Input Schema**:

  ```json
  {
    "repo_path": "string"
  }
  ```

### `git_branch`

- **Description**: List Git branches
- **Input Schema**:

  ```json
  {
    "repo_path": "string",
    "branch_type": "local|remote|all",
    "contains": "string",
    "not_contains": "string"
  }
  ```

## Optimized Tools

### `generate_commit_message`

- **Description**: Generate conventional commit message analysis (optimized)
- **Input Schema**:

  ```json
  {
    "repo_path": "string",
    "commit_type": "string",
    "scope": "string",
    "lite_mode": false
  }
  ```

### `optimized_status`

- **Description**: Fast git status check using GitPython (optimized)
- **Input Schema**:

  ```json
  {
    "repo_path": "string"
  }
  ```

## Usage Example

To use any of these tools, you can call them through the MCP server interface. Here's an example of how to get the repository status:

```python
from mcp.server import Server
from mcp.types import TextContent

server = Server("Git Commit Generator MCP")

# Call the git_status tool
response = await server.call_tool("git_status", {
    "repo_path": "/path/to/your/repository"
})

# Process the response
for content in response:
    if isinstance(content, TextContent):
        print(content.text)
```

## Notes

- All file paths should be absolute paths
- The `repo_path` parameter is required for all tools except `git_init`
- For tools that accept a `context_lines` parameter, it defaults to 3 if not specified
- The `lite_mode` parameter in `generate_commit_message` provides faster but less detailed analysis when set to `true`
