"""Unit tests for commit analysis tools."""

import unittest
from unittest.mock import MagicMock

from mcp_git_commit_generator.tools.commit_analysis import (
    generate_commit_analysis,
    optimized_git_status,
)


class TestCommitAnalysis(unittest.TestCase):
    """Test suite for commit analysis functions."""

    def setUp(self) -> None:
        """Set up a mock repository object for each test."""
        self.mock_repo = MagicMock()
        self.mock_repo.untracked_files = []
        self.mock_repo.index.diff.return_value = []
        self.mock_repo.active_branch.name = "main"

    def _create_mock_diff(self, change_type: str, path: str) -> MagicMock:
        """Helper to create a mock diff object."""
        diff = MagicMock()
        diff.change_type = change_type
        diff.a_path = path if change_type != "A" else None
        diff.b_path = path if change_type != "D" else None
        # Ensure a_path or b_path has a value
        if diff.a_path is None and diff.b_path is None:
            diff.a_path = path
        return diff

    # --- Tests for generate_commit_analysis ---

    def test_generate_commit_analysis_no_staged_changes(self) -> None:
        """Test analysis generation when there are no staged changes."""
        self.mock_repo.index.diff.return_value = []
        result = generate_commit_analysis(self.mock_repo)
        self.assertEqual(
            result,
            "No staged changes found. Please stage your changes with 'git add' first.",
        )
        self.mock_repo.index.diff.assert_called_once_with("HEAD")

    def test_generate_commit_analysis_lite_mode(self) -> None:
        """Test analysis generation in lite mode."""
        staged_diffs = [
            self._create_mock_diff("A", "new_file.py"),
            self._create_mock_diff("M", "modified_file.py"),
        ]
        self.mock_repo.index.diff.side_effect = [staged_diffs, []]  # staged, unstaged
        self.mock_repo.untracked_files = ["untracked.txt"]

        result = generate_commit_analysis(
            self.mock_repo, commit_type="feat", scope="test", lite_mode=True
        )

        self.assertIn("## Git Change Analysis for Conventional Commit Message", result)
        self.assertIn("### Changed Files:", result)
        self.assertIn("A\tnew_file.py", result)
        self.assertIn("M\tmodified_file.py", result)
        self.assertIn("### Repository Status:", result)
        self.assertIn("Staged: 2, Unstaged: 0, Untracked: 1", result)
        self.assertIn("Diff not loaded in lite mode.", result)
        self.assertIn("- Requested commit type: feat", result)
        self.assertIn("- Requested scope: test", result)
        self.mock_repo.git.diff.assert_not_called()

    def test_generate_commit_analysis_full_mode(self) -> None:
        """Test analysis generation in full mode with a successful diff."""
        staged_diffs = [self._create_mock_diff("M", "app.py")]
        self.mock_repo.index.diff.side_effect = [staged_diffs, []]
        self.mock_repo.untracked_files = []
        self.mock_repo.git.diff.return_value = (
            "--- a/app.py\n+++ b/app.py\n- old line\n+ new line"
        )

        result = generate_commit_analysis(self.mock_repo, lite_mode=False)

        self.assertIn("### Diff Preview (first 1500 chars):", result)
        self.assertIn("- old line", result)
        self.assertIn("+ new line", result)
        self.assertNotIn("Diff not loaded in lite mode.", result)
        self.assertIn("- Requested commit type: auto-detect based on changes", result)
        self.assertIn("- Requested scope: auto-detect based on files changed", result)
        self.mock_repo.git.diff.assert_called_once_with("--cached")

    def test_generate_commit_analysis_full_mode_diff_error(self) -> None:
        """Test analysis generation in full mode when diff fails."""
        staged_diffs = [self._create_mock_diff("M", "app.py")]
        self.mock_repo.index.diff.side_effect = [staged_diffs, []]
        self.mock_repo.git.diff.side_effect = Exception("Diff failed")

        result = generate_commit_analysis(self.mock_repo, lite_mode=False)

        self.assertIn("Error loading diff preview.", result)
        self.mock_repo.git.diff.assert_called_once_with("--cached")

    def test_generate_commit_analysis_general_exception(self) -> None:
        """Test general exception handling in generate_commit_analysis."""
        self.mock_repo.index.diff.side_effect = Exception("Unexpected error")
        result = generate_commit_analysis(self.mock_repo)
        self.assertEqual(result, "Error generating commit analysis: Unexpected error")

    # --- Tests for optimized_git_status ---

    def test_optimized_git_status_clean(self) -> None:
        """Test optimized status for a clean working tree."""
        result = optimized_git_status(self.mock_repo)
        self.assertIn("Current branch: main", result)
        self.assertIn("✓ Working tree clean", result)
        self.assertNotIn("Staged files", result)

    def test_optimized_git_status_staged(self) -> None:
        """Test optimized status with staged files."""
        staged_diffs = [self._create_mock_diff("A", "staged.txt")]
        self.mock_repo.index.diff.side_effect = [staged_diffs, []]

        result = optimized_git_status(self.mock_repo)
        self.assertIn("Staged files (ready to commit):", result)
        self.assertIn("  [A] staged.txt", result)
        self.assertIn("✓ Ready to generate commit message!", result)

    def test_optimized_git_status_all_states(self) -> None:
        """Test optimized status with files in all states."""
        staged_diffs = [self._create_mock_diff("A", "staged.txt")]
        unstaged_diffs = [self._create_mock_diff("M", "unstaged.txt")]
        self.mock_repo.index.diff.side_effect = [staged_diffs, unstaged_diffs]
        self.mock_repo.untracked_files = ["untracked.txt"]

        result = optimized_git_status(self.mock_repo)
        self.assertIn("Staged files (ready to commit):", result)
        self.assertIn("Unstaged files (need to be added):", result)
        self.assertIn("Untracked files:", result)
        self.assertIn("✓ Ready to generate commit message!", result)


if __name__ == "__main__":
    unittest.main()
