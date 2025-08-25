"""Main server implementation for the Git Commit Generator MCP server."""

from pathlib import Path

import git
from mcp.server import Server
from mcp.server.stdio import stdio_server

from mcp_git_commit_generator.tools.register_tools import register_list_tools


async def serve(repository: Path | None = None) -> None:
    """
    Start the MCP server for Git operations.
    Args:
        repository: Optional path to the Git repository
    """
    if repository is not None:
        try:
            git.Repo(repository)
        except git.InvalidGitRepositoryError:
            return

    server = Server("Git Commit Generator MCP")

    register_list_tools(server)

    # Start the server
    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)


if  __name__ == "__main__":
    import asyncio
    asyncio.run(serve())
