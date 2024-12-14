# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = True

P2_EXAMPLE = False
P2_FULL = True
# ========================= #

def add(a, b):
    return tuple([a[i] + b[i] for i in range(len(a))])

def get_tile(grid, i, j):
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
        return -1
    return int(grid[i][j])

def find_trailheads(grid):
    trailheads = []
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "0":
                trailheads.append((i, j))
    return trailheads

def score(grid, trailhead):
    delta = ((1, 0), (-1, 0), (0, 1), (0, -1))
    reachable = set([trailhead])
    for i in range(1, 10):
        next = set()
        # look for tiles adjacent to any tile in reachable
        # with a value of i
        for tile in reachable:
            for d in delta:
                if get_tile(grid, *add(tile, d)) == i:
                    next.add(add(tile, d))
        reachable = next
    return len(reachable)

def part_one(raw, lines, grid):
    return sum([score(grid, t) for t in find_trailheads(grid)])

def graph_trailhead(grid, th):
    delta = ((1, 0), (-1, 0), (0, 1), (0, -1))
    reachable = set([th])
    graph = {}
    for i in range(1, 10):
        next = set()
        # look for tiles adjacent to any tile in reachable
        # with a value of i
        for tile in reachable:
            graph[tile] = []
            for d in delta:
                loc = add(tile, d)
                if get_tile(grid, *loc) == i:
                    next.add(loc)
                    graph[tile].append(loc)
        reachable = next
    return graph

def count_paths(graph, start):
    if start not in graph:
        return 1
    return sum([count_paths(graph, n) for n in graph[start]])


def part_two(raw, lines, grid):
    t = find_trailheads(grid)
    # part two approach: make a graph out of the path
    # figure out the number of ways to traverse that graph
    # DFS to completion?
    return sum([count_paths(graph_trailhead(grid, th), th) for th in t])
