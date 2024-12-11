import time

#################################################
#                 BEGIN SOLUTION                #
#################################################

def rotate_90deg_cw(d):
    dir_map = {
        (-1, 0): (0, 1),
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0)
    }
    return dir_map[d]

def in_bounds(grid, i, j):
    return i >=0 and i < len(grid) and j >= 0 and j < len(grid[0])

def get_char(grid, i, j):
    if not in_bounds(grid, i, j):
        return "."
    return grid[i][j]

def step(l, d):
    return [l[i] + d[i] for i in range(len(l))]

def find_all_visited(grid):
    # find the guard's location
    l = [0, 0]
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "^":
                l = [i, j]
    d = (-1, 0)
    found_tiles = set()
    while in_bounds(grid, *l):
        # add current location to set of visited locations
        found_tiles.add(tuple(l))
        front = step(l, d)
        if get_char(grid, *front) == "#":
            d = rotate_90deg_cw(d) # turn right
        else:
            l = front # walk forward
    return found_tiles

def part_one(raw, lines, grid):
    return len(find_all_visited(grid))

def has_loop(grid):
    l = [0, 0]
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "^":
                l = [i, j]

    d = (-1, 0)
    states = set()
    while in_bounds(grid, *l):
        # if you end up in the same position and orientation as before,
        # there must be a loop.
        state = (tuple(l), d)
        if state in states:
            return True # there is a loop
        states.add((tuple(l), d))
        front = step(l, d)
        if get_char(grid, *front) == "#":
            d = rotate_90deg_cw(d) # turn right
        else:
            l = front # walk forward
    return False # there is not a loop


def part_two(raw, lines, grid):
    # intuitive approach (too slow!)
    # try, one at a time, replacing every tile with an obstacle and
    # then check if a loop is formed
    #
    # optimization:
    # only tiles that the guard actually occupies can alter her
    # path. there are a lot less tiles to try here. (about 4x speedup)
    tiles = find_all_visited(grid)
    num_loop = 0
    for (i, j) in tiles:
        if get_char(grid, i, j) == ".":
            # save a lot of effort by temporarily modifying
            # the existing grid instead of copying it.
            grid[i][j] = "#"
            if has_loop(grid):
                num_loop += 1
            grid[i][j] = "."
    return num_loop

#################################################
#                   END SOLUTION                #
#################################################
def read_file(filename):
    raw = None
    with open(filename) as f:
        raw = f.read()
    lines = raw.strip().split("\n")
    grid = [[c for c in line.strip()] for line in lines]
    return raw, lines, grid
if __name__ == "__main__":
    runs = {
        "Part one (example input):": (part_one, "example.txt"),
        "Part one (full input):": (part_one, "input.txt"),
        "Part two (example input):": (part_two, "example.txt"),
        "Part two (full input):": (part_two, "input.txt"),
    }
    for msg, (f, file) in runs.items():
        print(msg)
        data = read_file(file)
        t0 = time.perf_counter()
        res = f(*data)
        t1 = time.perf_counter()
        print("\t" + str(res))
        print("\t" + f"ran in {int((t1 - t0)*1000)}ms.")
