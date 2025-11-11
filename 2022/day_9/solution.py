# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

def get_steps(lines):
    steps = []
    # input parsing: add vectors to steps
    for line in lines:
        dir, n = line.split(" ")
        for _ in range(int(n)):
            steps.append(DIR_LOOKUP[dir])

    return steps

# steps to get from t to h along each component
def delta(h, t):
    return tuple(h[i] - t[i] for i in range(len(h)))

def touching(h, t):
    return all(abs(c) <= 1 for c in delta(h, t))

def add(a, b):
    return tuple(a[i] + b[i] for i in range(len(a)))

DIR_LOOKUP = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1)
}

def sign(n):
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0

def move_tail(h, t):
    d = delta(h, t)
    if d[0] == 0:
        return add(t, (0, sign(d[1])))
    if d[1] == 0:
        return add(t, (sign(d[0]), 0))
    return add(t, (sign(d[0]), sign(d[1])))


def print_grid(grid):
    for line in grid:
        for char in line:
            print(char, end="")
        print()

def print_state(h, t, size=10):
    grid = [["." for _ in range(size)] for _ in range(size)]
    grid[size-1][0] = "s"
    grid[size - t[1] - 1][t[0]] = "T"
    grid[size - h[1] - 1][h[0]] = "H"

    print_grid(grid)
    print("head: ", h)
    print("tail: ", t)

def print_visited(visited, size=10):
    grid = [["." for _ in range(size)] for _ in range(size)]
    for item in visited:
        grid[size - item[1] - 1][item[0]] = "#"
    print_grid(grid)



def part_one(raw, lines, grid):
    visited = set([(0, 0)])
    head = (0, 0)
    tail = (0, 0)
    steps = get_steps(lines)

    # debug output
    # print_state(head, tail)
    # print(f"\n{"="*10}\n")
    for step in steps:
        # move head, move tail to follow, add position to set
        head = add(head, step)
        if not touching(head, tail):
            tail = move_tail(head, tail)
        visited.add(tail)
        # print_state(head, tail)
        # print(f"\n{"="*10}\n")

    # print(visited)
    # print_visited(visited)
    return len(visited)

def part_two(raw, lines, grid):
    visited = set([(0, 0)])
    rope_segments = [(0, 0) for _ in range(10)]
    steps = get_steps(lines)

    for step in steps:
        # step the first segment
        rope_segments[0] = add(rope_segments[0], step)
        # each subsequent segment follows
        for i in range(1, len(rope_segments)):
            if not touching(rope_segments[i], rope_segments[i-1]):
                rope_segments[i] = move_tail(rope_segments[i-1], rope_segments[i])
        # track position of the last segment
        visited.add(rope_segments[-1])
    return len(visited)
