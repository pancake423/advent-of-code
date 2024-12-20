from math import inf
import sys

# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = True

P2_EXAMPLE = False
P2_FULL = True
# ========================= #
def get(grid, i, j):
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[i]):
        return -1
    return grid[i][j]

def make_graph(memory):
    graph = {}
    for i, row in enumerate(memory):
        for j, n in enumerate(row):
            if n == 0:
                candidates = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
                graph[(i, j)] = [(p, 1) for p in filter(lambda p: get(memory, *p) == 0, candidates)]
    return graph

def dijkstra(start, graph):
    def closest_node(nodes):
        min = inf
        min_n = ((-1, -1), -1)
        for node, dist in nodes.items():
            if dist < min:
                min = dist
                min_n = node
        return min_n, min
    # shit implementation, really slow but it works
    visited = {}
    unvisited = {}
    for v in graph.keys():
        unvisited[v] = 0 if v == start else inf

    while True:
        node, cost = closest_node(unvisited)
        if cost == inf:
            break
        for edge_node, edge_cost in graph[node]:
            if edge_node in unvisited and unvisited[edge_node] > cost + edge_cost:
                unvisited[edge_node] = cost + edge_cost
        visited[node] = cost
        del unvisited[node]

    return visited


def part_one(raw, lines, grid):
    grid_size = 71 # 7 for example, 71 for full
    n_corrupted = 1024 # 12 for example, 1024 for full

    memory = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    incoming = [[int(n) for n in line.split(",")] for line in lines]
    for i in range(n_corrupted):
        x, y = incoming[i]
        memory[x][y] = 1

    graph = make_graph(memory)
    sssp = dijkstra((0, 0), graph)
    return sssp[(grid_size-1, grid_size-1)]

# determine if there is any path (doesn't find optimal path)
# through the given memory
def is_path(start, goal, memory):
    # depth first search of memory space looking for any connection
    # to the goal
    visited = set()
    def dfs(i, j, goal):
        if (i, j) == goal:
            return True
        if get(memory, i, j) != 0:
            return False
        if (i, j) in visited:
            return False
        visited.add((i, j))

        coords = ((i+1, j), (i, j+1), (i-1, j), (i, j-1))
        for c in coords:
            if dfs(*c, goal):
                return True
        return False

    return dfs(*start, goal)

# determine if the memory is passable based on the number of bytes corrupted
def is_blocked(n_corrupted, incoming, grid_size):
    memory = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    for i in range(n_corrupted):
        x, y = incoming[i]
        memory[x][y] = 1
    # draw(memory, incoming[n_corrupted-1])
    return not is_path((0, 0), (grid_size-1, grid_size-1), memory)

# for debugging
def draw(grid, last_blocked):
    RED='\033[1;31m'
    NC='\033[0m'
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if (i, j) == tuple(last_blocked):
                print(RED, end="")
            print("." if c == 0 else "#", end="")
            print(NC, end="")
        print()


def part_two(raw, lines, grid):
    grid_size = 71 # 7 for example, 71 for full
    incoming = [[int(n) for n in line.split(",")] for line in lines]
    sys.setrecursionlimit((grid_size+1)**2)

    # binary search for the exact number where it is no longer passable
    low = 0
    high = len(incoming)
    while True:
        n = (low + high) // 2
        blocked = is_blocked(n, incoming, grid_size)
        blocked_prev = is_blocked(n-1, incoming, grid_size)
        # looking for n where is_blocked(n) is true, but is_blocked n-1 is false
        if blocked and not blocked_prev:
            return ",".join([str(n) for n in incoming[n-1]])
        if low == high:
            return "error: memory is never blocked"
        if blocked and blocked_prev:
            # too high
            high = n
        if not blocked and not blocked_prev:
            # too low
            low = n+1
