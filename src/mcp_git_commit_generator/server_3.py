import logging
from enum import Enum
from pathlib import Path
from typing import Optional, cast

import git
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

# Default number of context lines to show in diff output
DEFAULT_CONTEXT_LINES = 3


# Modelos originales del primer código
class GitStatus(BaseModel):
    repo_path: str


class GitDiffUnstaged(BaseModel):
    repo_path: str
    context_lines: int = DEFAULT_CONTEXT_LINES


class GitDiffStaged(BaseModel):
    repo_path: str
    context_lines: int = DEFAULT_CONTEXT_LINES


class GitDiff(BaseModel):
    repo_path: str
    target: str
    context_lines: int = DEFAULT_CONTEXT_LINES


class GitCommit(BaseModel):
    repo_path: str
    message: str


class GitAdd(BaseModel):
    repo_path: str
    files: list[str]


class GitReset(BaseModel):
    repo_path: str


class GitLog(BaseModel):
    repo_path: str
    max_count: int = 10


class GitCreateBranch(BaseModel):
    repo_path: str
    branch_name: str
    base_branch: str | None = None


class GitCheckout(BaseModel):
    repo_path: str
    branch_name: str


class GitShow(BaseModel):
    repo_path: str
    revision: str


class GitInit(BaseModel):
    repo_path: str


class GitBranch(BaseModel):
    repo_path: str = Field(..., description="The path to the Git repository.")
    branch_type: str = Field(
        ...,
        description="Whether to list local branches ('local'), remote branches ('remote') or all branches('all').",
    )
    contains: Optional[str] = Field(
        None, description="The commit sha that branch should contain."
    )
    not_contains: Optional[str] = Field(
        None, description="The commit sha that branch should NOT contain."
    )


# Nuevos modelos para funciones optimizadas
class GitCommitMessage(BaseModel):
    repo_path: str
    commit_type: Optional[str] = None
    scope: Optional[str] = None
    lite_mode: bool = False


class GitOptimizedStatus(BaseModel):
    repo_path: str


class GitTools(str, Enum):
    # Herramientas básicas de Git
    STATUS = "git_status"
    DIFF_UNSTAGED = "git_diff_unstaged"
    DIFF_STAGED = "git_diff_staged"
    DIFF = "git_diff"
    COMMIT = "git_commit"
    ADD = "git_add"
    RESET = "git_reset"
    LOG = "git_log"
    CREATE_BRANCH = "git_create_branch"
    CHECKOUT = "git_checkout"
    SHOW = "git_show"
    INIT = "git_init"
    BRANCH = "git_branch"

    # Herramientas optimizadas
    GENERATE_COMMIT_MESSAGE = "generate_commit_message"
    OPTIMIZED_STATUS = "git_optimized_status"


# Funciones originales del primer código
def git_status(repo: git.Repo) -> str:
    try:
        return cast(str, repo.git.status())
    except Exception as e:
        return f"Error getting status: {str(e)}"


def git_diff_unstaged(
    repo: git.Repo, context_lines: int = DEFAULT_CONTEXT_LINES
) -> str:
    try:
        return cast(str, repo.git.diff(f"--unified={context_lines}"))
    except Exception as e:
        return f"Error getting unstaged diff: {str(e)}"


def git_diff_staged(repo: git.Repo, context_lines: int = DEFAULT_CONTEXT_LINES) -> str:
    try:
        return cast(str, repo.git.diff(f"--unified={context_lines}", "--cached"))
    except Exception as e:
        return f"Error getting staged diff: {str(e)}"


def git_diff(
    repo: git.Repo, target: str, context_lines: int = DEFAULT_CONTEXT_LINES
) -> str:
    try:
        return cast(str, repo.git.diff(f"--unified={context_lines}", target))
    except Exception as e:
        return f"Error getting diff with {target}: {str(e)}"


def git_commit(repo: git.Repo, message: str) -> str:
    try:
        commit = repo.index.commit(message)
        return f"Changes committed successfully with hash {commit.hexsha}"
    except Exception as e:
        return f"Error committing: {str(e)}"


def git_add(repo: git.Repo, files: list[str]) -> str:
    try:
        if files == ["."]:
            repo.git.add(".")
        else:
            repo.index.add(files)
        return "Files staged successfully"
    except Exception as e:
        return f"Error adding files: {str(e)}"


def git_reset(repo: git.Repo) -> str:
    try:
        repo.index.reset()
        return "All staged changes reset"
    except Exception as e:
        return f"Error resetting: {str(e)}"


def git_log(repo: git.Repo, max_count: int = 10) -> list[str]:
    try:
        commits = list(repo.iter_commits(max_count=max_count))
        log = []
        for commit in commits:
            log.append(
                f"Commit: {commit.hexsha}\n"
                f"Author: {str(commit.author)}\n"
                f"Date: {commit.authored_datetime}\n"
                f"Message: {str(commit.message.strip())}\n"
            )
        return log
    except Exception as e:
        return [f"Error getting log: {str(e)}"]


def git_create_branch(
    repo: git.Repo, branch_name: str, base_branch: str | None = None
) -> str:
    try:
        if base_branch:
            base = repo.references[base_branch]
        else:
            base = repo.active_branch
        repo.create_head(branch_name, base)
        return f"Created branch '{branch_name}' from '{base.name}'"
    except Exception as e:
        return f"Error creating branch: {str(e)}"


def git_checkout(repo: git.Repo, branch_name: str) -> str:
    try:
        repo.git.checkout(branch_name)
        return f"Switched to branch '{branch_name}'"
    except Exception as e:
        return f"Error checking out branch: {str(e)}"


def git_init(repo_path: str) -> str:
    try:
        repo = git.Repo.init(path=repo_path, mkdir=True)
        return f"Initialized empty Git repository in {repo.git_dir}"
    except Exception as e:
        return f"Error initializing repository: {str(e)}"


def git_show(repo: git.Repo, revision: str) -> str:
    try:
        commit = repo.commit(revision)
        output = [
            f"Commit: {commit.hexsha}\n"
            f"Author: {str(commit.author)}\n"
            f"Date: {commit.authored_datetime}\n"
            f"Message: {str(commit.message.strip())}\n"
        ]
        if commit.parents:
            parent = commit.parents[0]
            diff = parent.diff(commit, create_patch=True)
        else:
            diff = commit.diff(git.NULL_TREE, create_patch=True)

        for d in diff:
            output.append(f"\n--- {d.a_path}\n+++ {d.b_path}\n")
            if d.diff:
                diff_content = d.diff
                if isinstance(diff_content, bytes):
                    try:
                        output.append(diff_content.decode("utf-8"))
                    except UnicodeDecodeError:
                        output.append(diff_content.decode("utf-8", errors="replace"))
                else:
                    output.append(diff_content)
        return "".join(output)
    except Exception as e:
        return f"Error showing commit: {str(e)}"


def git_branch(
    repo: git.Repo,
    branch_type: str,
    contains: str | None = None,
    not_contains: str | None = None,
) -> str:
    try:
        contains_sha = ("--contains", contains) if contains else (None,)
        not_contains_sha = ("--no-contains", not_contains) if not_contains else (None,)

        match branch_type:
            case "local":
                b_type = None
            case "remote":
                b_type = "-r"
            case "all":
                b_type = "-a"
            case _:
                return f"Invalid branch type: {branch_type}"

        args = [
            arg for arg in (b_type, *contains_sha, *not_contains_sha) if arg is not None
        ]
        branch_info = cast(str, repo.git.branch(*args)) if args else repo.git.branch()
        return branch_info
    except Exception as e:
        return f"Error listing branches: {str(e)}"


# Nuevas funciones optimizadas
def generate_commit_analysis(
    repo: git.Repo,
    commit_type: str | None = None,
    scope: str | None = None,
    lite_mode: bool = False,
) -> str:
    """Genera análisis para commit usando GitPython directamente"""
    try:
        # Obtener archivos staged
        staged_diffs = repo.index.diff("HEAD")
        if not staged_diffs:
            return "No staged changes found. Please stage your changes with 'git add' first."

        # Generar lista de archivos cambiados
        files_status = []
        for diff in staged_diffs:
            change_type = diff.change_type[0] if diff.change_type else "M"
            files_status.append(f"{change_type}\t{diff.a_path or diff.b_path}")

        files_output = "\n".join(files_status)

        # Obtener diff solo si no es lite_mode
        diff_content = "Diff not loaded in lite mode."
        if not lite_mode:
            try:
                diff_output = repo.git.diff("--cached")
                diff_content = (
                    f"### Diff Preview (first 1500 chars):\n{diff_output[:1500]}"
                )
            except Exception:
                diff_content = "Error loading diff preview."

        # Status summary
        unstaged_count = len(list(repo.index.diff(None)))
        untracked_count = len(repo.untracked_files)
        status_info = f"Staged: {len(staged_diffs)}, Unstaged: {unstaged_count}, Untracked: {untracked_count}"

        return f"""## Git Change Analysis for Conventional Commit Message

### Changed Files:
{files_output}

### Repository Status:
{status_info}

{diff_content}

### User Preferences:
- Requested commit type: {commit_type or "auto-detect based on changes"}
- Requested scope: {scope or "auto-detect based on files changed"}

### Instructions:
Please generate a conventional commit message following this format:
`type(scope): description`

**Common types:**
- feat: A new feature
- fix: A bug fix
- docs: Documentation only changes
- style: Changes that don't affect meaning (white-space, formatting, etc)
- refactor: Code change that neither fixes a bug nor adds a feature
- perf: A code change that improves performance
- build: Changes that affect the build system or external dependencies
- ci: Changes to CI configuration files and scripts
- test: Adding missing tests or correcting existing tests
- chore: Changes to build process or auxiliary tools
- revert: Reverts a previous commit

**Guidelines:**
- Use imperative mood in description ("add" not "adds" or "added")
- Don't capitalize first letter of description
- No period at the end of description
- Keep description under 50 characters if possible
- If scope is obvious from files, include it in parentheses"""

    except Exception as e:
        return f"Error generating commit analysis: {str(e)}"


def optimized_git_status(repo: git.Repo) -> str:
    """Status optimizado usando GitPython"""
    try:
        current_branch = repo.active_branch.name

        # Obtener archivos en diferentes estados
        staged_diffs = list(repo.index.diff("HEAD"))
        unstaged_diffs = list(repo.index.diff(None))
        untracked_files = repo.untracked_files

        status_summary = f"Current branch: {current_branch}\n\n"

        if staged_diffs:
            status_summary += "Staged files (ready to commit):\n"
            for diff in staged_diffs:
                filename = diff.a_path or diff.b_path
                change_type = diff.change_type[0] if diff.change_type else "M"
                status_summary += f"  [{change_type}] {filename}\n"
            status_summary += "\n"

        if unstaged_diffs:
            status_summary += "Unstaged files (need to be added):\n"
            for diff in unstaged_diffs:
                filename = diff.a_path or diff.b_path
                change_type = diff.change_type[0] if diff.change_type else "M"
                status_summary += f"  [{change_type}] {filename}\n"
            status_summary += "\n"

        if untracked_files:
            status_summary += "Untracked files:\n"
            for file in untracked_files:
                status_summary += f"  [?] {file}\n"
            status_summary += "\n"

        if staged_diffs:
            status_summary += "✓ Ready to generate commit message!"
        elif unstaged_diffs or untracked_files:
            status_summary += (
                "ℹ Stage files with 'git add' to generate commit messages."
            )
        else:
            status_summary += "✓ Working tree clean"

        return status_summary

    except Exception as e:
        return f"Error checking optimized status: {str(e)}"


async def serve(repository: Path | None = None) -> None:
    logger = logging.getLogger(__name__)

    if repository is not None:
        try:
            git.Repo(repository)
            logger.info(f"Using repository at {repository}")
        except git.InvalidGitRepositoryError:
            logger.error(f"{repository} is not a valid Git repository")
            return

    server = Server("mcp-git-unified")

    @server.list_tools()  # type: ignore[misc]
    async def list_tools() -> list[Tool]:
        return [
            # Herramientas básicas originales
            Tool(
                name=GitTools.STATUS,
                description="Shows the working tree status",
                inputSchema=GitStatus.model_json_schema(),
            ),
            Tool(
                name=GitTools.DIFF_UNSTAGED,
                description="Shows changes in the working directory that are not yet staged",
                inputSchema=GitDiffUnstaged.model_json_schema(),
            ),
            Tool(
                name=GitTools.DIFF_STAGED,
                description="Shows changes that are staged for commit",
                inputSchema=GitDiffStaged.model_json_schema(),
            ),
            Tool(
                name=GitTools.DIFF,
                description="Shows differences between branches or commits",
                inputSchema=GitDiff.model_json_schema(),
            ),
            Tool(
                name=GitTools.COMMIT,
                description="Records changes to the repository",
                inputSchema=GitCommit.model_json_schema(),
            ),
            Tool(
                name=GitTools.ADD,
                description="Adds file contents to the staging area",
                inputSchema=GitAdd.model_json_schema(),
            ),
            Tool(
                name=GitTools.RESET,
                description="Unstages all staged changes",
                inputSchema=GitReset.model_json_schema(),
            ),
            Tool(
                name=GitTools.LOG,
                description="Shows the commit logs",
                inputSchema=GitLog.model_json_schema(),
            ),
            Tool(
                name=GitTools.CREATE_BRANCH,
                description="Creates a new branch from an optional base branch",
                inputSchema=GitCreateBranch.model_json_schema(),
            ),
            Tool(
                name=GitTools.CHECKOUT,
                description="Switches branches",
                inputSchema=GitCheckout.model_json_schema(),
            ),
            Tool(
                name=GitTools.SHOW,
                description="Shows the contents of a commit",
                inputSchema=GitShow.model_json_schema(),
            ),
            Tool(
                name=GitTools.INIT,
                description="Initialize a new Git repository",
                inputSchema=GitInit.model_json_schema(),
            ),
            Tool(
                name=GitTools.BRANCH,
                description="List Git branches",
                inputSchema=GitBranch.model_json_schema(),
            ),
            # Nuevas herramientas optimizadas
            Tool(
                name=GitTools.GENERATE_COMMIT_MESSAGE,
                description="Generate conventional commit message analysis (optimized)",
                inputSchema=GitCommitMessage.model_json_schema(),
            ),
            Tool(
                name=GitTools.OPTIMIZED_STATUS,
                description="Fast git status check using GitPython (optimized)",
                inputSchema=GitOptimizedStatus.model_json_schema(),
            ),
        ]

    @server.call_tool()  # type: ignore[misc]
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        repo_path = Path(arguments["repo_path"])

        # Handle git init separately since it doesn't require an existing repo
        if name == GitTools.INIT:
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

        match name:
            # Herramientas básicas originales
            case GitTools.STATUS:
                status = git_status(repo)
                return [TextContent(type="text", text=f"Repository status:\n{status}")]

            case GitTools.DIFF_UNSTAGED:
                diff = git_diff_unstaged(
                    repo, arguments.get("context_lines", DEFAULT_CONTEXT_LINES)
                )
                return [TextContent(type="text", text=f"Unstaged changes:\n{diff}")]

            case GitTools.DIFF_STAGED:
                diff = git_diff_staged(
                    repo, arguments.get("context_lines", DEFAULT_CONTEXT_LINES)
                )
                return [TextContent(type="text", text=f"Staged changes:\n{diff}")]

            case GitTools.DIFF:
                diff = git_diff(
                    repo,
                    arguments["target"],
                    arguments.get("context_lines", DEFAULT_CONTEXT_LINES),
                )
                return [
                    TextContent(
                        type="text", text=f"Diff with {arguments['target']}:\n{diff}"
                    )
                ]

            case GitTools.COMMIT:
                result = git_commit(repo, arguments["message"])
                return [TextContent(type="text", text=result)]

            case GitTools.ADD:
                result = git_add(repo, arguments["files"])
                return [TextContent(type="text", text=result)]

            case GitTools.RESET:
                result = git_reset(repo)
                return [TextContent(type="text", text=result)]

            case GitTools.LOG:
                log = git_log(repo, arguments.get("max_count", 10))
                return [
                    TextContent(type="text", text="Commit history:\n" + "\n".join(log))
                ]

            case GitTools.CREATE_BRANCH:
                result = git_create_branch(
                    repo, arguments["branch_name"], arguments.get("base_branch")
                )
                return [TextContent(type="text", text=result)]

            case GitTools.CHECKOUT:
                result = git_checkout(repo, arguments["branch_name"])
                return [TextContent(type="text", text=result)]

            case GitTools.SHOW:
                result = git_show(repo, arguments["revision"])
                return [TextContent(type="text", text=result)]

            case GitTools.BRANCH:
                result = git_branch(
                    repo,
                    arguments.get("branch_type", "local"),
                    arguments.get("contains", None),
                    arguments.get("not_contains", None),
                )
                return [TextContent(type="text", text=result)]

            # Nuevas herramientas optimizadas
            case GitTools.GENERATE_COMMIT_MESSAGE:
                result = generate_commit_analysis(
                    repo,
                    arguments.get("commit_type"),
                    arguments.get("scope"),
                    arguments.get("lite_mode", False),
                )
                return [TextContent(type="text", text=result)]

            case GitTools.OPTIMIZED_STATUS:
                result = optimized_git_status(repo)
                return [TextContent(type="text", text=result)]

            case _:
                raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)


if __name__ == "__main__":
    import asyncio

    asyncio.run(serve())
