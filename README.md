# FileSystemManager

A Python virtual filesystem implemented as a tree. Create directories and files, list contents, search by name, move/rename, and remove—all in memory with a Unix-like API.

## Features

- **mkdir** — Create directories (parent must exist)
- **touch** — Create files (supported extensions: `.txt`, `.md`, `.pdf`, `.jpg`, `.png`)
- **ls** — List directory contents (sorted)
- **find** — Search the tree for a name; returns all matching paths
- **rm** — Remove a file or directory (recursive for directories)
- **mv** — Move or rename files and directories
- **tree** — Pretty-print the filesystem structure

## Requirements

- Python 3.x (no external dependencies for the core module)

## Quick Start

```python
from FileSystemManager import FileSystem

fs = FileSystem("MyFileSystem")

# Create directories
fs.mkdir("/users")
fs.mkdir("/users/jacqueline")

# Create files (parent directory must exist)
fs.touch("/users/jacqueline/notes.txt")
fs.touch("/users/jacqueline/todo.md")

# List directory contents
fs.ls("/users")           # → ["jacqueline"]
fs.ls("/users/jacqueline") # → ["notes.txt", "todo.md"]

# Search by name
fs.find("notes.txt")      # → ["/users/jacqueline/notes.txt"]

# Move / rename
fs.mv("/users/jacqueline/notes.txt", "/users/jacqueline/notes_v2.txt")

# Pretty-print tree
fs.tree()
# /
# └── users
#     └── jacqueline
#         ├── notes_v2.txt
#         └── todo.md

# Remove
fs.rm("/users/jacqueline/notes_v2.txt")
```

Run the built-in demo:

```bash
python FileSystemManager.py
```

## API Summary

| Method | Description |
|--------|-------------|
| `mkdir(path)` | Create directory at absolute path. Raises `ValueError` if parent missing or path exists. |
| `touch(path)` | Create file. Allowed extensions: `.txt`, `.md`, `.pdf`, `.jpg`, `.png`. |
| `ls(path)` | List direct children of directory (sorted). Raises if path is a file or missing. |
| `find(name)` | Return list of all absolute paths matching `name`. |
| `rm(path)` | Delete file or directory (recursive). Cannot delete root `/`. |
| `mv(src, dest)` | Move or rename. `dest` can be a directory (move into) or new path (rename). |
| `tree(path="/")` | Return (and print) tree string for given path. |

All paths are **absolute** (e.g. `/users/jacqueline/notes.txt`).

## Testing

Unit tests use [pytest](https://pytest.org/) and live in `tests/`.

```bash
pip install pytest
pytest tests/ -v
```

## Development

- **Lint:** `ruff check .`
- **Format:** `black .`
- **Install dev deps:** `pip install -r requirements-dev.txt`

CI runs tests on push/PR (see `.github/workflows/test.yml`).

## Project Structure

```
.
├── FileSystemManager.py   # Main module
├── tests/
│   └── test_FileSystemManager.py
├── FileSystemManager.md   # Detailed documentation
├── README.md
├── LICENSE
├── pyproject.toml         # Project metadata, pytest/ruff/black config
├── requirements.txt       # Runtime deps (none)
├── requirements-dev.txt   # pytest, ruff, black
├── create_release.sh
├── RELEASE_GUIDE.md
└── RELEASE_CHECKLIST.md
```

## License

MIT — see [LICENSE](LICENSE).
