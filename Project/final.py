def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class File:
    def __init__(self, name, data=None, parent=None):
        self.name = name
        self.data = data if data else []
        self.parent = parent

    def newfiletxt(self):
        print("Enter lines (/end/ to finish):")
        self.data = []
        while True:
            line = input()
            if line == '/end/':
                break
            self.data.append(line)

    def appendtxt(self):
        print("Enter lines to append (/end/ to finish):")
        while True:
            line = input()
            if line == '/end/':
                break
            self.data.append(line)

    def editline(self, line, text):
        if 0 <= line < len(self.data):
            self.data[line] = text
        else:
            print("Line number out of range")

    def delline(self, line):
        if 0 <= line < len(self.data):
            self.data.pop(line)
        else:
            print("Line number out of range")

    def cat(self):
        for line in self.data:
            print(line)


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.child = []
        self.files = []

    def mkdir(self, name):
        new_dir = Directory(name, self)
        self.child.append(new_dir)
        return new_dir

    def touch(self, name):
        new_file = File(name, parent=self)
        self.files.append(new_file)
        return new_file

    def find_file(self, name):
        for file in self.files:
            if file.name == name:
                return file
        return None

    def find_dir(self, name):
        for dir in self.child:
            if dir.name == name:
                return dir
        return None

    def ls(self):
        items = [d.name for d in self.child] + [f.name for f in self.files]
        for item in sorted(items):
            print(item)


@singleton
class FileSystem:
    def __init__(self):
        self.root = Directory('/')
        self.current_dir = self.root
        self.path = '/'

    def _resolve_path(self, path):
        if path.startswith('/'):
            current = self.root
            parts = path.strip('/').split('/')
        else:
            current = self.current_dir
            parts = path.split('/')

        for part in parts:
            if part == '..':
                current = current.parent if current.parent else current
            elif part == '.' or part == '':
                continue
            else:
                next_dir = current.find_dir(part)
                if next_dir:
                    current = next_dir
                else:
                    return None
        return current

    def _resolve_file(self, path):
        dir_path, file_name = path.rsplit('/', 1) if '/' in path else ('.', path)
        directory = self._resolve_path(dir_path)
        return directory.find_file(file_name) if directory else None

    def make_directory(self, path, name):
        parent_dir = self._resolve_path(path)
        if parent_dir:
            parent_dir.mkdir(name)
        else:
            print("Path not found")

    def create_file(self, path, name):
        parent_dir = self._resolve_path(path)
        if parent_dir:
            parent_dir.touch(name)
        else:
            print("Path not found")

    def remove(self, path):
        target_dir = self._resolve_path(path)
        if target_dir and target_dir.parent:
            target_dir.parent.child.remove(target_dir)
        else:
            target_file = self._resolve_file(path)
            if target_file:
                target_file.parent.files.remove(target_file)
            else:
                print("File or directory not found")

    def change_directory(self, path):
        target = self._resolve_path(path)
        if target:
            self.current_dir = target
            self.path = self._get_path(target)
        else:
            print("Directory not found")

    def _get_path(self, directory):
        if directory.parent is None:
            return '/'
        path = []
        while directory.parent:
            path.insert(0, directory.name)
            directory = directory.parent
        return '/' + '/'.join(path)

    def list_current_directory(self):
        self.current_dir.ls()

    def write_to_file(self, path, lines):
        file = self._resolve_file(path)
        if file:
            file.data = lines
        else:
            print("File not found")

    def append_to_file(self, path, lines):
        file = self._resolve_file(path)
        if file:
            file.data.extend(lines)
        else:
            print("File not found")

    def edit_line(self, path, line, text):
        file = self._resolve_file(path)
        if file:
            file.editline(line, text)
        else:
            print("File not found")

    def delete_line(self, path, line):
        file = self._resolve_file(path)
        if file:
            file.delline(line)
        else:
            print("File not found")

    def read_file(self, path):
        file = self._resolve_file(path)
        if file:
            file.cat()
        else:
            print("File not found")

    def move(self, src, dst):
        file = self._resolve_file(src)
        dst_dir = self._resolve_path(dst)
        if file and dst_dir:
            file.parent.files.remove(file)
            file.parent = dst_dir
            dst_dir.files.append(file)
        else:
            print("Source or destination not found")

    def copy(self, src, dst):
        file = self._resolve_file(src)
        dst_dir = self._resolve_path(dst)
        if file and dst_dir:
            new_file = File(file.name, file.data[:], dst_dir)
            dst_dir.files.append(new_file)
        else:
            print("Source or destination not found")

    def rename(self, path, new_name):
        file = self._resolve_file(path)
        dir = self._resolve_path(path)
        if file:
            file.name = new_name
        elif dir:
            dir.name = new_name
        else:
            print("Path not found")


class CommandParser:
    def __init__(self, command):
        parts = command.strip().split()
        self.cmd = parts[0] if parts else ''
        self.args = parts[1:] if len(parts) > 1 else []

    def handle_command(self):
        fs = FileSystem()

        try:
            if self.cmd == 'mkdir':
                if len(self.args) == 2:
                    fs.make_directory(self.args[0], self.args[1])
                elif len(self.args) == 1:
                    fs.make_directory(fs.path, self.args[0])
                else:
                    raise ValueError("mkdir usage: mkdir [<path>] <folder_name>")

            elif self.cmd == 'rm':
                if len(self.args) != 1:
                    raise ValueError("rm usage: rm <path>")
                fs.remove(self.args[0])

            elif self.cmd == 'touch':
                if len(self.args) == 2:
                    fs.create_file(self.args[0], self.args[1])
                elif len(self.args) == 1:
                    fs.create_file(fs.path, self.args[0])
                else:
                    raise ValueError("touch usage: touch [<path>] <filename>.txt")

            elif self.cmd == 'cd':
                if len(self.args) != 1:
                    raise ValueError("cd usage: cd <path>")
                fs.change_directory(self.args[0])

            elif self.cmd == 'ls':
                if self.args:
                    raise ValueError("ls usage: ls")
                fs.list_current_directory()

            elif self.cmd == 'nwfiletxt':
                if len(self.args) != 1:
                    raise ValueError("nwfiletxt usage: nwfiletxt <path>")
                lines = self._input_lines()
                fs.write_to_file(self.args[0], lines)

            elif self.cmd == 'appendtxt':
                if len(self.args) != 1:
                    raise ValueError("appendtxt usage: appendtxt <path>")
                lines = self._input_lines()
                fs.append_to_file(self.args[0], lines)

            elif self.cmd == 'editline':
                if len(self.args) < 3:
                    raise ValueError("editline usage: editline <path> <line> <text>")
                path = self.args[0]
                line = int(self.args[1])
                text = ' '.join(self.args[2:])
                fs.edit_line(path, line, text)

            elif self.cmd == 'deline':
                if len(self.args) != 2:
                    raise ValueError("deline usage: deline <path> <line>")
                fs.delete_line(self.args[0], int(self.args[1]))

            elif self.cmd == 'cat':
                if len(self.args) != 1:
                    raise ValueError("cat usage: cat <path>")
                fs.read_file(self.args[0])

            elif self.cmd == 'mv':
                if len(self.args) != 2:
                    raise ValueError("mv usage: mv <source> <destination>")
                fs.move(self.args[0], self.args[1])

            elif self.cmd == 'cp':
                if len(self.args) != 2:
                    raise ValueError("cp usage: cp <source> <destination>")
                fs.copy(self.args[0], self.args[1])

            elif self.cmd == 'rename':
                if len(self.args) != 2:
                    raise ValueError("rename usage: rename <path> <new_name>")
                fs.rename(self.args[0], self.args[1])

            else:
                raise ValueError(f"Unknown command: {self.cmd}")

        except Exception as e:
            print(f"Error: {e}")

    def _input_lines(self):
        print("Enter lines (/end/ to finish):")
        lines = []
        while True:
            line = input()
            if line == '/end/':
                break
            lines.append(line)
        return lines


if __name__ == '__main__':
    fs = FileSystem()
    while True:
        print(f"{fs.path}$", end=' ')
        command = input()
        parser = CommandParser(command)
        parser.handle_command()
