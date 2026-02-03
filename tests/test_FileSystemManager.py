"""
Unit tests for FileSystemManager.

Run with: pytest test_FileSystemManager.py -v
Or:       python -m pytest test_FileSystemManager.py -v
"""

import pytest
from FileSystemManager import FileSystem, Node, FileNode, DirectoryNode


# --- Fixtures: reusable test setup ---
@pytest.fixture
def fs():
    """Fresh FileSystem instance for each test (no shared state)."""
    return FileSystem("test_fs")


# --- Tests for mkdir ---
def test_mkdir_creates_root_level_directory(fs):
    """mkdir("/users") should create /users."""
    fs.mkdir("/users")
    assert "users" in fs.root.children
    assert fs.root.children["users"].is_file is False


def test_mkdir_creates_nested_directory(fs):
    """mkdir("/a/b/c") after creating /a and /a/b should work."""
    fs.mkdir("/a")
    fs.mkdir("/a/b")
    fs.mkdir("/a/b/c")
    assert "c" in fs.root.children["a"].children["b"].children


def test_mkdir_duplicate_raises_error(fs):
    """Creating the same directory twice should raise ValueError."""
    fs.mkdir("/users")
    with pytest.raises(ValueError, match="already exists"):
        fs.mkdir("/users")


def test_mkdir_missing_parent_raises_error(fs):
    """mkdir("/a/b/c") when /a doesn't exist should raise ValueError."""
    with pytest.raises(ValueError, match="does not exist"):
        fs.mkdir("/a/b/c")


# --- Tests for ls ---
def test_ls_root_empty(fs):
    """ls("/") on empty filesystem returns empty list."""
    assert fs.ls("/") == []


def test_ls_root_after_mkdir(fs):
    """ls("/") returns names of top-level directories."""
    fs.mkdir("/users")
    fs.mkdir("/data")
    assert fs.ls("/") == ["data", "users"]


def test_ls_directory(fs):
    """ls on a directory returns sorted child names."""
    fs.mkdir("/users")
    fs.mkdir("/users/alice")
    fs.mkdir("/users/jacqueline")
    assert fs.ls("/users") == ["alice", "jacqueline"]


def test_ls_file_raises_error(fs):
    """ls on a file path should raise ValueError."""
    fs.mkdir("/users")
    fs.touch("/users/notes.txt")
    with pytest.raises(ValueError, match="is a file, not a directory"):
        fs.ls("/users/notes.txt")


# --- Tests for touch ---
def test_touch_creates_file(fs):
    """touch creates a file in an existing directory."""
    fs.mkdir("/users")
    fs.touch("/users/notes.txt")
    assert "notes.txt" in fs.root.children["users"].children
    assert fs.root.children["users"].children["notes.txt"].is_file is True


def test_touch_invalid_extension_raises_error(fs):
    """touch with unsupported extension should raise ValueError."""
    fs.mkdir("/users")
    with pytest.raises(ValueError, match="invalid extension"):
        fs.touch("/users/script.py")


def test_touch_missing_parent_raises_error(fs):
    """touch when parent directory doesn't exist should raise ValueError."""
    with pytest.raises(ValueError, match="does not exist"):
        fs.touch("/missing/file.txt")
