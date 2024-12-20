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

def shortest_path(memory, goal_pos):
    # use a BFS to find the shortest path through the memory
    explored = set([(0, 0)])
    depth = [0] #queue holding the depth of nodes to explore
    queue = [(0, 0)] #queue holding the position of nodes to explore
    while len(queue) > 0:
        i,j = queue.pop(0)
        d = depth.pop(0)
        if (i, j) == goal_pos:
            return d
        coords = ((i+1, j), (i, j+1), (i-1, j), (i, j-1))
        for c in coords:
            if c not in explored and get(memory, *c) == 0:
                explored.add(c)
                queue.append(c)
                depth.append(d+1)
    return inf


def part_one(raw, lines, grid):
    grid_size = 71 # 7 for example, 71 for full
    n_corrupted = 1024 # 12 for example, 1024 for full

    memory = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    incoming = [[int(n) for n in line.split(",")] for line in lines]
    for i in range(n_corrupted):
        x, y = incoming[i]
        memory[x][y] = 1

    return shortest_path(memory, (grid_size-1, grid_size-1))

# determine if the memory is passable based on the number of bytes corrupted
def is_blocked(n_corrupted, incoming, grid_size):
    memory = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    for i in range(n_corrupted):
        x, y = incoming[i]
        memory[x][y] = 1
    # draw(memory, incoming[n_corrupted-1])
    return shortest_path(memory, (grid_size-1, grid_size-1)) == inf

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
