import unittest
from unittest.mock import MagicMock, patch

from mcp_git_commit_generator.tools import git_operations


class TestGitOperations(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_repo = MagicMock()

    def test_git_status(self) -> None:
        self.mock_repo.git.status.return_value = "On branch main"
        status = git_operations.git_status(self.mock_repo)
        self.assertEqual(status, "On branch main")

    def test_git_status_error(self) -> None:
        self.mock_repo.git.status.side_effect = Exception("Git error")
        status = git_operations.git_status(self.mock_repo)
        self.assertEqual(status, "Error getting status: Git error")

    def test_git_diff_unstaged(self) -> None:
        self.mock_repo.git.diff.return_value = "diff --git a/file.txt b/file.txt"
        diff = git_operations.git_diff_unstaged(self.mock_repo)
        self.assertEqual(diff, "diff --git a/file.txt b/file.txt")
        self.mock_repo.git.diff.assert_called_with("--unified=3")

    def test_git_diff_staged(self) -> None:
        self.mock_repo.git.diff.return_value = "diff --git a/file.txt b/file.txt"
        diff = git_operations.git_diff_staged(self.mock_repo)
        self.assertEqual(diff, "diff --git a/file.txt b/file.txt")
        self.mock_repo.git.diff.assert_called_with("--unified=3", "--cached")

    def test_git_diff(self) -> None:
        self.mock_repo.git.diff.return_value = "diff --git a/file.txt b/file.txt"
        diff = git_operations.git_diff(self.mock_repo, "develop")
        self.assertEqual(diff, "diff --git a/file.txt b/file.txt")
        self.mock_repo.git.diff.assert_called_with("--unified=3", "develop")

    def test_git_commit(self) -> None:
        mock_commit = MagicMock()
        mock_commit.hexsha = "12345"
        self.mock_repo.index.commit.return_value = mock_commit
        result = git_operations.git_commit(self.mock_repo, "Test commit")
        self.assertEqual(result, "Changes committed successfully with hash 12345")
        self.mock_repo.index.commit.assert_called_with("Test commit")

    def test_git_add(self) -> None:
        result = git_operations.git_add(self.mock_repo, ["file1.txt", "file2.txt"])
        self.assertEqual(result, "Files staged successfully")
        self.mock_repo.index.add.assert_called_with(["file1.txt", "file2.txt"])

    def test_git_add_all(self) -> None:
        result = git_operations.git_add(self.mock_repo, ["."])
        self.assertEqual(result, "Files staged successfully")
        self.mock_repo.git.add.assert_called_with(".")

    def test_git_reset(self) -> None:
        result = git_operations.git_reset(self.mock_repo)
        self.assertEqual(result, "All staged changes reset")
        self.mock_repo.index.reset.assert_called_once()

    def test_git_log(self) -> None:
        mock_commit = MagicMock()
        mock_commit.hexsha = "12345"
        mock_commit.author = "Test Author"
        mock_commit.authored_datetime = "2025-08-15"
        mock_commit.message = "Test commit"
        self.mock_repo.iter_commits.return_value = [mock_commit]
        log = git_operations.git_log(self.mock_repo)
        expected_log = [
            "Commit: 12345\n"
            "Author: Test Author\n"
            "Date: 2025-08-15\n"
            "Message: Test commit\n"
        ]
        self.assertEqual(log, expected_log)

    def test_git_create_branch(self) -> None:
        self.mock_repo.active_branch.name = "main"
        result = git_operations.git_create_branch(self.mock_repo, "new-feature")
        self.assertEqual(result, "Created branch 'new-feature' from 'main'")
        self.mock_repo.create_head.assert_called_with(
            "new-feature", self.mock_repo.active_branch
        )

    def test_git_checkout(self) -> None:
        result = git_operations.git_checkout(self.mock_repo, "new-feature")
        self.assertEqual(result, "Switched to branch 'new-feature'")
        self.mock_repo.git.checkout.assert_called_with("new-feature")

    @patch("git.Repo.init")
    def test_git_init(self, mock_init: MagicMock) -> None:
        mock_repo_instance = MagicMock()
        mock_repo_instance.git_dir = "/tmp/test_repo/.git"
        mock_init.return_value = mock_repo_instance
        result = git_operations.git_init("/tmp/test_repo")
        self.assertEqual(
            result, "Initialized empty Git repository in /tmp/test_repo/.git"
        )
        mock_init.assert_called_with(path="/tmp/test_repo", mkdir=True)


if __name__ == "__main__":
    unittest.main()
