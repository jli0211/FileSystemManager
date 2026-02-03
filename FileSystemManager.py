from collections import deque
import os
FILE_EXTENSIONS = {".txt", ".md", ".pdf", ".jpg", ".png"}

class Node:
    def __init__(self, name: str, is_file: bool):
        self.name = name
        self.parent = None
        self.is_file = is_file
        self.path = ""

class FileNode(Node):
    def __init__(self, name: str):
        super().__init__(name, True)

class DirectoryNode(Node):
    def __init__(self, name: str):
        super().__init__(name, False)
        self.children = {}
        #print(f"DirectoryNode: {name}")

class FileSystem:

    def __init__(self, name: str):
        self.name = name
        self.root = DirectoryNode("/")

    def __str__(self) -> str:
        result = []
        queue = deque([(self.root, "")])
        while queue:
            node, prefix = queue.popleft()
            result.append(prefix + node.name)
            if not node.is_file and node.children:
                children_list = sorted(node.children.values(), key=lambda x: x.name)
                queue.extend([(child, prefix + "  ") for child in children_list])
        return "\n".join(result)
    
    def mkdir(self, path: str) -> None:
        """TODO: Creates a directory
        Purpose:
            Create a new directory at the given absolute path.

        Behavior:

            If all parent directories exist → create the final directory.

            If the directory already exists → raise an error.

            If any parent directory does NOT exist → raise an error.

        Examples:
            mkdir("/users")           → OK
            mkdir("/users/jacqueline") → OK
            mkdir("/users/jacqueline/docs") → OK

            mkdir("/users/jacqueline") → ERROR (already exists)
            mkdir("/a/b/c") → ERROR ("/a" does not exist)
        """
        directories = path.split("/")[1:]
        current = self.root
        path = ""
        for dir in directories[:-1]:
            path += "/" + dir
            if dir in current.children:
                current = current.children[dir]
            else:
                raise ValueError(f"Directory {dir} does not exist")
        if directories[-1] in current.children:
            raise ValueError(f"Directory {directories[-1]} already exists")
        else:
            new_node = DirectoryNode(directories[-1])
            new_node.parent = current
            current.children[new_node.name] = new_node
            new_node.path = path + "/" + new_node.name
            print(f"Directory {directories[-1]} created")
            print(f"Directory Path: {new_node.path}")
                        

    def touch(self, path: str):
        """TODO: Creates a file
        Purpose:
            Create a new empty file at the given path.

        Behavior:

            Parent directory must exist.

            If a file or directory with the same name already exists → error.

            The created node is a file (not a directory).

        Examples:
            touch("/users/jacqueline/notes.txt") → OK
            touch("/users/jacqueline") → ERROR (already a directory)
            touch("/users/unknown/file.txt") → ERROR (parent doesn't exist)
        
        """
        _, ext = os.path.splitext(path)
        if ext not in FILE_EXTENSIONS:
            raise ValueError(f"File {path} has an invalid extension")
        current = self.root
        directories = path.split("/")[1:]
        path = ""
        for dir in directories[:-1]:
            path += "/" + dir
            if dir in current.children:
                current = current.children[dir]
            else:
                raise ValueError(f"Directory {dir} does not exist")
        if directories[-1] in current.children:
            raise ValueError(f"File {directories[-1]} already exists")
        else:
            new_node = FileNode(directories[-1])
            new_node.parent = current
            current.children[new_node.name] = new_node
            new_node.path = path + "/" + new_node.name
            print(f"File {directories[-1]} created")
            print(f"File Path: {new_node.path}")

    def ls(self, path: str) -> list[str]:
        """
        Purpose:
            List the immediate children of a directory.

        Behavior:

            If path is a file → error.

            If path is a directory → return list of child names.

            Return results sorted alphabetically.

        Examples:

            Assume structure:

            /users/
            ├── alice/
            └── jacqueline/
                ├── notes.txt
                ├── todo.md
                └── photos/

            ls("/") → ["users"]
            ls("/users") → ["alice", "jacqueline"]
            ls("/users/jacqueline") → ["notes.txt", "photos", "todo.md"]
            ls("/users/jacqueline/notes.txt") → ERROR
        """
        current = self.root
        directories = path.split("/")[1:]
        # Handle root directory case
        if not directories or (len(directories) == 1 and directories[0] == ""):
            res = sorted(current.children.keys())
            print(res)
            return res
        
        res = []
        for dir in directories[:-1]:
            if dir in current.children:
                current = current.children[dir]
            else:
                raise ValueError(f"Directory {dir} does not exist")
        if directories[-1] in current.children:
            current = current.children[directories[-1]]
            if current.is_file:
                raise ValueError(f"Path {path} is a file, not a directory")
            else:
                res = sorted(current.children.keys())
                print(res)
                return res
        else:
            raise ValueError(f"Directory {path} does not exist")


    def find(self, name: str) -> list[str]:
        """
        Purpose:
            Search the entire filesystem for files or directories with a given name.

        Behavior:

            Perform a full tree search (DFS or BFS — your choice).

            Return all matching absolute paths.

        Example:
            If there are two files named notes.txt:

            find("notes.txt") →
            [
            "/users/jacqueline/notes.txt",
            "/work/jacqueline/notes.txt"
        ]


        If no match → return empty list.
        """
        queue = deque([self.root])
        res = []
        while queue:
            for _ in range(len(queue)):
                node = queue.popleft()
                if node.name == name:
                    res.append(node.path)
                if not node.is_file:
                    queue.extend(node.children.values())
        print(res)
        return res

    def rm(self, path: str) -> None:
        """
        Purpose:
            Delete a file or directory.

        Behavior:

            If path is a file → delete it.

            If path is a directory → delete it recursively (all children).

            If path does not exist → error.

            Cannot delete root /.

        Examples:
            rm("/users/jacqueline/notes.txt") → deletes file
            rm("/users/jacqueline") → deletes entire subtree
            rm("/") → ERROR
        """
        if path == "/":
            raise ValueError("Cannot delete root directory")
        
        directories = path.split("/")[1:]
        if not directories or (len(directories) == 1 and directories[0] == ""):
            raise ValueError("Cannot delete root directory")
        
        current = self.root
        for dir in directories[:-1]:
            if dir in current.children:
                current = current.children[dir]
            else:
                raise ValueError(f"Directory {dir} does not exist")
        
        if directories[-1] in current.children:
            node = current.children[directories[-1]]
            if node.is_file:
                current.children.pop(directories[-1])
                print(f"File {directories[-1]} deleted")
            else:
                current.children.pop(directories[-1])
                print(f"Directory {directories[-1]} deleted")
        else:
            raise ValueError(f"Path {path} does not exist")


    def mv(self, src: str, dest: str) -> None:
        """
        Purpose:
            Move (or rename) a file or directory.

        Behavior:

            src must exist.

            dest parent must exist.

            If moving into an existing directory, place inside it.

            If renaming, change the node's name.

        Examples:
            Rename a file:
            mv("/users/jacqueline/notes.txt",
            "/users/jacqueline/notes_v2.txt")

            Move file into another directory:
            mv("/users/jacqueline/notes.txt",
            "/users/jacqueline/docs/")

            Move entire directory:
            mv("/users/jacqueline", "/backup/")
        """
        # Find source node
        src_dirs = [d for d in src.split("/")[1:] if d]
        src_current = self.root
        for dir in src_dirs[:-1]:
            if dir in src_current.children:
                src_current = src_current.children[dir]
            else:
                raise ValueError(f"Source path {src} does not exist")
        
        if src_dirs[-1] not in src_current.children:
            raise ValueError(f"Source path {src} does not exist")
        
        src_node = src_current.children[src_dirs[-1]]
        
        # Determine destination
        dest_dirs = [d for d in dest.split("/")[1:] if d]
        dest_parent = self.root
        
        # Check if dest ends with "/" (moving into directory) or is a new name
        if dest.endswith("/") or (dest_dirs and dest_dirs[-1] in dest_parent.children and 
                                  not dest_parent.children[dest_dirs[-1]].is_file):
            # Moving into existing directory
            for dir in dest_dirs:
                if dir in dest_parent.children:
                    dest_parent = dest_parent.children[dir]
                else:
                    raise ValueError(f"Destination directory {dest} does not exist")
            new_name = src_dirs[-1]
        else:
            # Renaming or moving to new location
            for dir in dest_dirs[:-1]:
                if dir in dest_parent.children:
                    dest_parent = dest_parent.children[dir]
                else:
                    raise ValueError(f"Destination parent directory does not exist")
            new_name = dest_dirs[-1]
        
        # Check if destination already exists
        if new_name in dest_parent.children:
            raise ValueError(f"Destination {dest} already exists")
        
        # Validate file extension if it's a file
        if src_node.is_file:
            _, ext = os.path.splitext(new_name)
            if ext not in FILE_EXTENSIONS:
                raise ValueError(f"File {new_name} has an invalid extension")
        
        # Move the node
        del src_current.children[src_dirs[-1]]
        src_node.name = new_name
        src_node.parent = dest_parent
        dest_parent.children[new_name] = src_node
        
        # Update path recursively if it's a directory
        def update_paths(node, parent_path):
            node.path = parent_path + "/" + node.name
            if not node.is_file:
                for child in node.children.values():
                    update_paths(child, node.path)
        
        update_paths(src_node, dest_parent.path if dest_parent.path else "")
        
        print(f"Moved {src} to {dest_parent.path + '/' + new_name if dest_parent.path else '/' + new_name}")
    def tree(self, path: str = "/") -> str:
        """
        Purpose:
            Pretty-print the filesystem structure.

        Example output:
        /
        └── users
            ├── alice
            └── jacqueline
                ├── notes.txt
                ├── todo.md
                └── photos
        """
        # Find the starting node
        if path == "/":
            start_node = self.root
        else:
            directories = [d for d in path.split("/")[1:] if d]
            start_node = self.root
            for dir in directories:
                if dir in start_node.children:
                    start_node = start_node.children[dir]
                else:
                    raise ValueError(f"Path {path} does not exist")
            if start_node.is_file:
                raise ValueError(f"Path {path} is a file, not a directory")
        
        def build_tree(node, prefix="", is_last=True, is_root=False):
            result = []
            if is_root:
                result.append(node.name)
            else:
                connector = "└── " if is_last else "├── "
                result.append(prefix + connector + node.name)
            
            if not node.is_file and node.children:
                children_list = sorted(node.children.values(), key=lambda x: x.name)
                for i, child in enumerate(children_list):
                    is_last_child = (i == len(children_list) - 1)
                    extension = "    " if is_last else "│   "
                    result.extend(build_tree(child, prefix + extension, is_last_child, False))
            
            return result
        
        tree_lines = build_tree(start_node, "", True, path == "/")
        tree_str = "\n".join(tree_lines)
        print(tree_str)
        return tree_str

if __name__ == "__main__":
    fs = FileSystem("MyFileSystem")
    fs.mkdir("/users")
    fs.mkdir("/users/jacqueline")
    fs.mkdir("/work")
    fs.mkdir("/work/jacqueline")
    # fs.mkdir("/users/jacqueline/docs")

    # print(fs)
    fs.touch("/users/jacqueline/notes.txt")
    fs.touch("/work/jacqueline/notes.txt")
    fs.ls("/users")
    #fs.ls("/users/jacqueline/notes.txt")
    fs.find("notes.txt")
    fs.mv("/users/jacqueline/notes.txt", "/users/jacqueline/notes2.txt")
    fs.tree()