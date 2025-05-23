def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class FileSystem:
    def __init__(self, root):
        self.root = root
        self.path = '/'
        self.directories = {'/': Directory('/')}

    def get_path(self, path):
        if path[0] == '/':
            return self.absolute_path(path)
        else:
            return self.relative_path(path)

    def absolute_path(self, path):
        if path == '/':
            return self.directories['/']

        parts = path.split("/")
        parts.remove("")

        current = self.root

        for part in parts:
            found = False
            for directory in current.child:
                if directory.name == part:
                    current = directory
                    found = True
                    break
            if not found:
                print("Path not found")
                return None
        return current

    def relative_path(self, path):
        return self.absolute_path(self.path.rstrip('/') + '/' + path)


class Directory:
    def __init__(self, name):
        self.child = []
        self.files = []
        self.name = name
        self.parent = None

    def mkdir(self, dir1):
        self.child.append(dir1)
        dir1.parent = self

    def cp(self, dir1, dir2):
        pass

    def mv(self, dir1, dir2):
        pass

    def ls(self):
        output = []
        for dire in self.child:
            output.append(dire.name)
        for file in self.files:
            output.append(file.name)
        print(' '.join(sorted(output)))

    def touch(self, name):
        pass


class File:
    def __init__(self, name, data, parent):
        self.name = name
        self.data = data
        self.parent = parent

    def newfiletxt(self):
        print("Enter your text: (/e means done)")
        text = []
        while True:
            line = input()
            if line == '/e':
                break
            text.append(line)
        self.data = text
        print(f"{self.name} overwritten")

    def appendtxt(self):
        print("Enter your text to append: (/e means done)")
        text = []
        while True:
            line = input()
            if line == '/e':
                break
            text.append(line)
        self.data.extend(text)
        print(f"{self.name} overwritten")

    def editline(self, line, text):
        if 0 <= line < len(self.data):
            self.data[line] = text
            print(f"{self.name} overwritten")
        else:
            print(f"{self.name} have not this line")

    def delline(self, line):
        if 0 <= line < len(self.data):
            self.data.pop(line)
            print(f"{self.name} overwritten")
        else:
            print(f"{self.name} have not this line")

    def cat(self):
        for line in self.data:
            print(line)


class CommandParser:
    def __init__(self, command):
        parts = command.strip().split()
        self.cmd = parts[0] if parts else ''
        self.args = parts[1:] if len(parts) > 1 else []

    def handle_command(self):
        fs = FileSystem()
        try:
            if self.cmd == 'mkdir':
                if len(self.args) > 1:
                    fs.make_directory(self.args[1], self.args[0])
                else:
                    fs.make_directory(self.args[0])

            elif self.cmd == 'rm':
                if len(self.args) != 1:
                    raise ValueError("rm requires exactly one argument")
                fs.remove(self.args[0])

            elif self.cmd == 'touch':
                if len(self.args) > 1:
                    fs.create_file(self.args[1], self.args[0])
                elif len(self.args) == 1:
                    fs.create_file(self.args[0])

            elif self.cmd == 'cd':
                if len(self.args) != 1:
                    raise ValueError("cd requires exactly one argument")
                fs.change_directory(self.args[0])

            elif self.cmd == 'nwfiletxt':
                if len(self.args) < 2:
                    raise ValueError("nwfiletxt requires a filename and text")
                filename = self.args[0]
                text = ' '.join(self.args[1:])
                fs.new_file_text(filename, text)

            elif self.cmd == 'appendtxt':
                path = self.args[0]
                i = input('-->')
                text = ''
                while i != '!finish':
                    text = text + i + '\n'
                    i = input('(enter !finish to exit append mode)--> ')
                fs.append_text(path, text)

            elif self.cmd == 'editline':
                if len(self.args) < 3:
                    raise ValueError("editline requires a filename, line number, and text")
                filename = self.args[0]
                try:
                    line = int(self.args[1])
                except ValueError:
                    raise ValueError("Line number must be an integer")
                text = ' '.join(self.args[2:])
                fs.edit_line(filename, line, text)

            elif self.cmd == 'deline':
                if len(self.args) != 2:
                    raise ValueError("deline requires a filename and line number")
                filename = self.args[0]
                try:
                    line = int(self.args[1])
                except ValueError:
                    raise ValueError("Line number must be an integer")
                fs.delete_line(filename, line)

            elif self.cmd == 'cat':
                if len(self.args) != 1:
                    raise ValueError("cat requires exactly one argument")
                print(fs.cat_file(self.args[0]))

            elif self.cmd == 'mv':
                if len(self.args) != 2:
                    raise ValueError("mv requires exactly two arguments")
                fs.move(self.args[0], self.args[1])

            elif self.cmd == 'cp':
                if len(self.args) != 2:
                    raise ValueError("cp requires exactly two arguments")
                fs.copy(self.args[0], self.args[1])

            elif self.cmd == 'rename':
                if len(self.args) != 2:
                    raise ValueError("rename requires exactly two arguments")
                fs.rename(self.args[0], self.args[1])

            elif self.cmd == 'ls':
                if self.args:
                    raise ValueError("ls takes no arguments")
                fs.list_directory()

            else:
                raise ValueError(f"Unknown command: {self.cmd}")

        except (FileNotFoundErrorCustomException, DirectoryNotFoundError, FileExistsErrorCustomException, DirectoryExistsError, ValueError) as e:
            print(f"Error: {e}")


class FileNotFoundErrorCustomException(Exception):
    pass

class DirectoryNotFoundError(Exception):
    pass

class FileExistsErrorCustomException(Exception):
    pass

class DirectoryExistsError(Exception):
    pass


if __name__ == '__main__':
    filesystem = FileSystem('/')

    while True:
        print(filesystem.path)
        command = input()
        parser = CommandParser(command)
        parser.handle_command()