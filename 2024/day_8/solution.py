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
    return [a[i] + b[i] for i in range(len(a))]

def sub(a, b):
    return [a[i] - b[i] for i in range(len(a))]

def mult(v, n):
    return [i * n for i in v]

def in_bounds(grid, a, b):
    return (a >= 0 and a < len(grid) and
        b >= 0 and b < len(grid[1]))

def find_antennas(grid):
    antennas = {}
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c != ".":
                if c not in antennas:
                    antennas[c] = []
                antennas[c].append((i, j))
    return antennas

def part_one(raw, lines, grid):
    antennas = find_antennas(grid)
    antinodes = set()
    for nodes in antennas.values():
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                delta = sub(nodes[j], nodes[i])
                antinodes.add(tuple(add(nodes[j], delta)))
                antinodes.add(tuple(sub(nodes[i], delta)))
    return len(list(filter(lambda n: in_bounds(grid, *n), antinodes)))

def part_two(raw, lines, grid):
    antennas = find_antennas(grid)
    antinodes = set()
    for nodes in antennas.values():
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                delta = sub(nodes[j], nodes[i])
                pos = nodes[j]
                # search in both directions until out of bounds
                while in_bounds(grid, *pos):
                    antinodes.add(tuple(pos))
                    pos = add(pos, delta)
                pos = nodes[i]
                while in_bounds(grid, *pos):
                    antinodes.add(tuple(pos))
                    pos = sub(pos, delta)

    return len(list(filter(lambda n: in_bounds(grid, *n), antinodes)))
