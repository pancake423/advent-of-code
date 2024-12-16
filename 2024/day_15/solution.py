# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = True

P2_EXAMPLE = False
P2_FULL = True
# ========================= #
d_lookup = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1),
}

def print_grid(g):
    for l in g:
        print("".join(l))

def gps(grid):
    score = 0
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "O" or c == "[":
                score += i * 100 + j
    return score

def find_robot(grid):
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "@":
                return (i, j)
    return (-1, -1)

def step(grid, char, robot_loc):
    # figure out what direction we're moving
    d = d_lookup[char]
    # start at robot's position continue stepping in
    # direction D until we hit a wall or empty space tile.
    can_move = False
    i, j = robot_loc
    visited = []
    while True:
        i += d[0]
        j += d[1]
        tile = grid[i][j]
        if (tile == "#"):
            can_move = False
            break
        if (tile == "."):
            can_move = True
            break
        visited.append((i, j))
    # if we can't move, just stop here
    if not can_move:
        return robot_loc
    # move the boxes:
    # replace the tile at pos + d with the value at pos for every position we encountered
    # (in reverse order !!)
    for i, j in reversed(visited):
        grid[i + d[0]][j + d[1]] = grid[i][j]
    # move the robot and return the updated robot position
    i, j = robot_loc
    grid[i][j] = "."
    i += d[0]
    j += d[1]
    grid[i][j] = "@"
    return (i, j)

def part_one(raw, lines, grid):
    # parse input: g-> tile grid | m-> moves list
    g, m = raw.split("\n\n")
    g = [[c for c in r] for r in g.split("\n")]
    m = list(filter(lambda c: not c.isspace(), [c for c in m]))

    robot_loc = find_robot(g)
    for move in m:
        robot_loc = step(g, move, robot_loc)
    # print_grid(g)
    return gps(g)

def expand(grid):
    transform = {
        "@": ["@", "."],
        "#": ["#", "#"],
        ".": [".", "."],
        "O": ["[", "]"]
    }
    return [[n for c in row for n in transform[c]] for row in grid]

def p2_step(grid, char, robot_loc):
    d = d_lookup[char]
    tiles_to_move = [[*robot_loc, False]]
    l = 0
    while l != len(tiles_to_move):
        l = len(tiles_to_move)
        for i in range(l):
            tile = tiles_to_move[i]
            if tile[2]:
                continue
            tile[2] = True
            i, j = tile[0] + d[0], tile[1] + d[1]
            if grid[i][j] == "[":
                tiles_to_move.append([i, j, False])
                if d[1] == 0:
                    tiles_to_move.append([i, j+1, False])
            if grid[i][j] == "]":
                tiles_to_move.append([i, j, False])
                if d[1] == 0:
                    tiles_to_move.append([i, j-1, False])
    tiles = set((t[0], t[1]) for t in tiles_to_move)
    # print(tiles)
    # ensure that every tile either has another tile that we want to move
    # or an empty space in front of it.
    can_move = True
    for tile in tiles:
        i, j = tile[0] + d[0], tile[1] + d[1]
        if (i, j) in tiles or grid[i][j] == ".":
            continue
        can_move = False
    # move the tiles, if allowed
    if not can_move:
        return robot_loc

    tiles = [(i, j, grid[i][j]) for i, j in tiles]
    for i, j, _ in tiles:
        grid[i][j] = "."
    for i, j, c in tiles:
        grid[i + d[0]][j + d[1]] = c

    return robot_loc[0] + d[0], robot_loc[1] + d[1]


def part_two(raw, lines, grid):
    g, m = raw.split("\n\n")
    g = [[c for c in r] for r in g.split("\n")]
    m = list(filter(lambda c: not c.isspace(), [c for c in m]))

    g = expand(g)
    robot_loc = find_robot(g)
    #print_grid(g)
    for move in m:
        robot_loc = p2_step(g, move, robot_loc)
        #print_grid(g)
    return gps(g)
