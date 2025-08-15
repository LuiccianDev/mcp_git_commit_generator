"""Git operations for the MCP Git Commit Generator."""

from typing import cast

import git

from mcp_git_commit_generator.core.models import DEFAULT_CONTEXT_LINES


def git_status(repo: git.Repo) -> str:
    """Get the working tree status."""
    try:
        return cast(str, repo.git.status())
    except Exception as e:
        return f"Error getting status: {str(e)}"


def git_diff_unstaged(
    repo: git.Repo, context_lines: int = DEFAULT_CONTEXT_LINES
) -> str:
    """Get unstaged changes in the working directory."""
    try:
        return cast(str, repo.git.diff(f"--unified={context_lines}"))
    except Exception as e:
        return f"Error getting unstaged diff: {str(e)}"


def git_diff_staged(repo: git.Repo, context_lines: int = DEFAULT_CONTEXT_LINES) -> str:
    """Get changes that are staged for commit."""
    try:
        return cast(str, repo.git.diff(f"--unified={context_lines}", "--cached"))
    except Exception as e:
        return f"Error getting staged diff: {str(e)}"


def git_diff(
    repo: git.Repo, target: str, context_lines: int = DEFAULT_CONTEXT_LINES
) -> str:
    """Get differences between branches or commits."""
    try:
        return cast(str, repo.git.diff(f"--unified={context_lines}", target))
    except Exception as e:
        return f"Error getting diff with {target}: {str(e)}"


def git_commit(repo: git.Repo, message: str) -> str:
    """Commit changes to the repository."""
    try:
        commit = repo.index.commit(message)
        return f"Changes committed successfully with hash {commit.hexsha}"
    except Exception as e:
        return f"Error committing: {str(e)}"


def git_add(repo: git.Repo, files: list[str]) -> str:
    """Add file contents to the staging area."""
    try:
        if files == ["."]:
            repo.git.add(".")
        else:
            repo.index.add(files)
        return "Files staged successfully"
    except Exception as e:
        return f"Error adding files: {str(e)}"


def git_reset(repo: git.Repo) -> str:
    """Unstage all staged changes."""
    try:
        repo.index.reset()
        return "All staged changes reset"
    except Exception as e:
        return f"Error resetting: {str(e)}"


def git_log(repo: git.Repo, max_count: int = 10) -> list[str]:
    """Get commit logs."""
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
    """Create a new branch."""
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
    """Switch branches."""
    try:
        repo.git.checkout(branch_name)
        return f"Switched to branch '{branch_name}'"
    except Exception as e:
        return f"Error checking out branch: {str(e)}"


def git_init(repo_path: str) -> str:
    """Initialize a new Git repository."""
    try:
        repo = git.Repo.init(path=repo_path, mkdir=True)
        return f"Initialized empty Git repository in {repo.git_dir}"
    except Exception as e:
        return f"Error initializing repository: {str(e)}"


def git_show(repo: git.Repo, revision: str) -> str:
    """Show the contents of a commit."""
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
    """List Git branches."""
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
