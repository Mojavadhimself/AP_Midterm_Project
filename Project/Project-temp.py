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

    def get_path(self):
        pass


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
        pass

    def appendtxt(self):
        pass

    def editline(self, line, text):
        pass

    def delline(self, line):
        pass

    def cat(self):
        pass


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
