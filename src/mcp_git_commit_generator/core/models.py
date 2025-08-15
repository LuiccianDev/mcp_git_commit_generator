"""Data models for the Git Commit Generator MCP server."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

# Default number of context lines to show in diff output
DEFAULT_CONTEXT_LINES = 3


class GitStatus(BaseModel):
    """Model for git status command."""

    repo_path: str


class GitDiffUnstaged(BaseModel):
    """Model for git diff unstaged changes."""

    repo_path: str
    context_lines: int = DEFAULT_CONTEXT_LINES


class GitDiffStaged(BaseModel):
    """Model for git diff staged changes."""

    repo_path: str
    context_lines: int = DEFAULT_CONTEXT_LINES


class GitDiff(BaseModel):
    """Model for git diff between commits or branches."""

    repo_path: str
    target: str
    context_lines: int = DEFAULT_CONTEXT_LINES


class GitCommit(BaseModel):
    """Model for git commit."""

    repo_path: str
    message: str


class GitAdd(BaseModel):
    """Model for git add command."""

    repo_path: str
    files: list[str]


class GitReset(BaseModel):
    """Model for git reset command."""

    repo_path: str


class GitLog(BaseModel):
    """Model for git log command."""

    repo_path: str
    max_count: int = 10


class GitCreateBranch(BaseModel):
    """Model for git branch creation."""

    repo_path: str
    branch_name: str
    base_branch: str | None = None


class GitCheckout(BaseModel):
    """Model for git checkout command."""

    repo_path: str
    branch_name: str


class GitShow(BaseModel):
    """Model for git show command."""

    repo_path: str
    revision: str


class GitInit(BaseModel):
    """Model for git init command."""

    repo_path: str


class GitBranch(BaseModel):
    """Model for git branch listing."""

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


class GitCommitMessage(BaseModel):
    """Model for generating commit messages."""

    repo_path: str
    commit_type: Optional[str] = None
    scope: Optional[str] = None
    lite_mode: bool = False


class GitOptimizedStatus(BaseModel):
    """Model for optimized git status."""

    repo_path: str


class GitTools(str, Enum):
    """Enumeration of available Git tools."""

    # Basic Git tools
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

    # Optimized tools
    GENERATE_COMMIT_MESSAGE = "generate_commit_message"
    OPTIMIZED_STATUS = "git_optimized_status"
