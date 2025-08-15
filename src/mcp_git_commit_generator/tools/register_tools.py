from pathlib import Path

import git
from mcp.server import Server
from mcp.types import TextContent, Tool

from mcp_git_commit_generator.core import models

from .commit_analysis import generate_commit_analysis, optimized_git_status
from .git_operations import (
    git_add,
    git_branch,
    git_checkout,
    git_commit,
    git_create_branch,
    git_diff,
    git_diff_staged,
    git_diff_unstaged,
    git_init,
    git_log,
    git_reset,
    git_show,
    git_status,
)


def register_list_tools(server: Server) -> None:

    @server.list_tools()  # type: ignore[misc]
    async def list_tools() -> list[Tool]:
        """List all available Git tools."""
        return [
            # Basic Git tools
            Tool(
                name=models.GitTools.STATUS,
                description="Shows the working tree status",
                inputSchema=models.GitStatus.model_json_schema(),
            ),
            Tool(
                name=models.GitTools.DIFF_UNSTAGED,
                description="Shows changes in the working directory that are not yet staged",
                inputSchema=models.GitDiffUnstaged.model_json_schema(),
            ),
            Tool(
                name=models.GitTools.DIFF_STAGED,
                description="Shows changes that are staged for commit",
                inputSchema=models.GitDiffStaged.model_json_schema(),
            ),
            Tool(
                name=models.GitTools.DIFF,
                description="Shows differences between branches or commits",
                inputSchema=models.GitDiff.model_json_schema(),
            ),
            Tool(
                name=models.GitTools.COMMIT,
                description="Records changes to the repository",
                inputSchema=models.GitCommit.model_json_schema(),
            ),
            Tool(
                name=models.GitTools.ADD,
                description="Adds file contents to the staging area",
                inputSchema=models.GitAdd.model_json_schema(),
            ),
            Tool(
                name=models.GitTools.RESET,
                description="Unstages all staged changes",
                inputSchema=models.GitReset.model_json_schema(),
            ),
            Tool(
                name=models.GitTools.LOG,
                description="Shows the commit logs",
                inputSchema=models.GitLog.model_json_schema(),
            ),
            Tool(
                name=models.GitTools.CREATE_BRANCH,
                description="Creates a new branch from an optional base branch",
                inputSchema=models.GitCreateBranch.model_json_schema(),
            ),
            Tool(
                name=models.GitTools.CHECKOUT,
                description="Switches branches",
                inputSchema=models.GitCheckout.model_json_schema(),
            ),
            Tool(
                name=models.GitTools.SHOW,
                description="Shows the contents of a commit",
                inputSchema=models.GitShow.model_json_schema(),
            ),
            Tool(
                name=models.GitTools.INIT,
                description="Initialize a new Git repository",
                inputSchema=models.GitInit.model_json_schema(),
            ),
            Tool(
                name=models.GitTools.BRANCH,
                description="List Git branches",
                inputSchema=models.GitBranch.model_json_schema(),
            ),
            # Optimized tools
            Tool(
                name=models.GitTools.GENERATE_COMMIT_MESSAGE,
                description="Generate conventional commit message analysis (optimized)",
                inputSchema=models.GitCommitMessage.model_json_schema(),
            ),
            Tool(
                name=models.GitTools.OPTIMIZED_STATUS,
                description="Fast git status check using GitPython (optimized)",
                inputSchema=models.GitOptimizedStatus.model_json_schema(),
            ),
        ]

    @server.call_tool()  # type: ignore[misc]
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Handle tool calls and route to the appropriate function."""
        repo_path = Path(arguments["repo_path"])

        # Handle git init separately since it doesn't require an existing repo
        if name == models.GitTools.INIT:
            result = git_init(str(repo_path))
            return [TextContent(type="text", text=result)]

        # For all other commands, we need an existing repo
        try:
            repo = git.Repo(repo_path)
        except git.InvalidGitRepositoryError:
            return [
                TextContent(
                    type="text", text=f"'{repo_path}' is not a valid Git repository"
                )
            ]

        # Route to the appropriate handler based on the tool name
        match name:
            # Basic Git tools
            case models.GitTools.STATUS:
                status = git_status(repo)
                return [TextContent(type="text", text=f"Repository status:\n{status}")]

            case models.GitTools.DIFF_UNSTAGED:
                diff = git_diff_unstaged(
                    repo, arguments.get("context_lines", models.DEFAULT_CONTEXT_LINES)
                )
                return [TextContent(type="text", text=f"Unstaged changes:\n{diff}")]

            case models.GitTools.DIFF_STAGED:
                diff = git_diff_staged(
                    repo, arguments.get("context_lines", models.DEFAULT_CONTEXT_LINES)
                )
                return [TextContent(type="text", text=f"Staged changes:\n{diff}")]

            case models.GitTools.DIFF:
                diff = git_diff(
                    repo,
                    arguments["target"],
                    arguments.get("context_lines", models.DEFAULT_CONTEXT_LINES),
                )
                return [
                    TextContent(
                        type="text", text=f"Diff with {arguments['target']}:\n{diff}"
                    )
                ]

            case models.GitTools.COMMIT:
                result = git_commit(repo, arguments["message"])
                return [TextContent(type="text", text=result)]

            case models.GitTools.ADD:
                result = git_add(repo, arguments["files"])
                return [TextContent(type="text", text=result)]

            case models.GitTools.RESET:
                result = git_reset(repo)
                return [TextContent(type="text", text=result)]

            case models.GitTools.LOG:
                log = git_log(repo, arguments.get("max_count", 10))
                return [
                    TextContent(type="text", text="Commit history:\n" + "\n".join(log))
                ]

            case models.GitTools.CREATE_BRANCH:
                result = git_create_branch(
                    repo, arguments["branch_name"], arguments.get("base_branch")
                )
                return [TextContent(type="text", text=result)]

            case models.GitTools.CHECKOUT:
                result = git_checkout(repo, arguments["branch_name"])
                return [TextContent(type="text", text=result)]

            case models.GitTools.SHOW:
                result = git_show(repo, arguments["revision"])
                return [TextContent(type="text", text=result)]

            case models.GitTools.BRANCH:
                result = git_branch(
                    repo,
                    arguments.get("branch_type", "local"),
                    arguments.get("contains", None),
                    arguments.get("not_contains", None),
                )
                return [TextContent(type="text", text=result)]

            # Optimized tools
            case models.GitTools.GENERATE_COMMIT_MESSAGE:
                result = generate_commit_analysis(
                    repo,
                    arguments.get("commit_type"),
                    arguments.get("scope"),
                    arguments.get("lite_mode", False),
                )
                return [TextContent(type="text", text=result)]

            case models.GitTools.OPTIMIZED_STATUS:
                result = optimized_git_status(repo)
                return [TextContent(type="text", text=result)]

            case _:
                raise ValueError(f"Unknown tool: {name}")
