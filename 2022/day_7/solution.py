# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

def p_i(s, i):
    return "  "*i + str(s) + "\n"

class Directory:
    def __init__(self, parent = None, path = ""):
        self.parent = parent
        self.path = path
        self.children = []
        self.size = None

    def full_path(self):
        if self.parent == None:
            return self.path
        return self.parent.full_path() + "/" + self.path

    def __str__(self):
        return self._str_internal(0)

    def _str_internal(self, i = 0):
        out = ""
        out += p_i(f"Directory (path: {self.path}, size: {self.get_size()}) {{", i)
        for child in self.children:
            out += child._str_internal(i+1)
        out += p_i("}", i)
        return out

    def get_size(self):
        # dynamic programming to avoid excessive recursion
        if (self.size == None):
            self.size = sum(child.get_size() for child in self.children)
        return self.size

    def flatten(self):
        out = [self]
        for child in self.children:
            if type(child) == File:
                out.append(child)
                continue
            out += child.flatten()
        return out

class File:
    def __init__(self, name, size):
        self.path = name
        self.size = int(size)

    def __str__(self):
        return self._str_internal(0)

    def _str_internal(self, i = 0):
        return p_i(f"File (path: {self.path}, size: {self.size}) ", i)

    def get_size(self):
        return self.size


def parse_input(lines):
    root = Directory()
    cwd = root
    for line in lines:
        tokens = line.split(" ")
        if tokens[0] == "$":
            cmd = tokens[1]
            if cmd == "cd":
                path = tokens[2]
                if path == "..":
                    cwd = cwd.parent
                elif path == "/":
                    cwd = root
                else:
                    cwd = list(filter(lambda n: n.path == path, cwd.children))[0]
            elif cmd == "ls":
                pass
        else:
            # we are a listed item. create in the current path
            if tokens[0] == "dir":
                cwd.children.append(Directory(cwd, tokens[1]))
            else:
                cwd.children.append(File(tokens[1], tokens[0]))
    return root

def part_one(raw, lines, grid):
    root = parse_input(lines)
    root.get_size()
    return sum(filter(lambda n: n <= 100000, map(lambda n: n.size, filter(lambda n: type(n) == Directory, root.flatten()))))


def part_two(raw, lines, grid):
    root = parse_input(lines)
    free_space = 70000000 - root.get_size()
    return min(filter(lambda n: n + free_space >= 30000000, map(lambda n: n.size, filter(lambda n: type(n) == Directory, root.flatten()))))
