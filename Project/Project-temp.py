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

    def mkdir(self, dir):
        self.child.append(dir)
        dir.parent = self

    def cp(self, dir1, dir2):
        pass

    def mv(self, dir1, dir2):
        pass

    def ls(self):
        output = ''
        for dire in self.child:
            output += dire.name + ' '
        print(output)

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
        parts = command.split()
        self.cmd = parts[0]
        self.args = parts[1:]

    def handle_command(self):
        if self.cmd == 'mkdir':
            pass
        elif self.cmd == 'rm':
            pass
        elif self.cmd == 'touch':
            pass
        elif self.cmd == 'cd':
            pass
        elif self.cmd == 'nwfiletxt':
            pass
        elif self.cmd == 'appendtxt':
            pass
        elif self.cmd == 'editline':
            pass
        elif self.cmd == 'deline':
            pass
        elif self.cmd == 'cat':
            pass
        elif self.cmd == 'mv':
            pass
        elif self.cmd == 'cp':
            pass
        elif self.cmd == 'rename':
            pass
        elif self.cmd == 'ls':
            pass


if __name__ == '__main__':
    filesystem = FileSystem('/')

    while True:
        print(filesystem.path)
        command = input()
        parser = CommandParser(command)
        parser.handle_command()
