"""Commit message analysis and generation tools."""

import git


def generate_commit_analysis(
    repo: git.Repo,
    commit_type: str | None = None,
    scope: str | None = None,
    lite_mode: bool = False,
) -> str:
    """
    Generate analysis for commit using GitPython.

    Args:
        repo: The Git repository object
        commit_type: Optional commit type (feat, fix, etc.)
        scope: Optional scope for the commit
        lite_mode: If True, skip loading full diff for performance

    Returns:
        str: Formatted commit message analysis
    """
    try:
        # Get staged files
        staged_diffs = repo.index.diff("HEAD")
        if not staged_diffs:
            return "No staged changes found. Please stage your changes with 'git add' first."

        # Generate list of changed files
        files_status = []
        for diff in staged_diffs:
            change_type = diff.change_type[0] if diff.change_type else "M"
            files_status.append(f"{change_type}\t{diff.a_path or diff.b_path}")

        files_output = "\n".join(files_status)

        # Get diff only if not in lite_mode
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
    """
    Get optimized git status using GitPython.

    Args:
        repo: The Git repository object

    Returns:
        str: Formatted status information
    """
    try:
        current_branch = repo.active_branch.name

        # Get files in different states
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
