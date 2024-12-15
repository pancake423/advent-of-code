# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = True

P2_EXAMPLE = False
P2_FULL = True
# ========================= #

# solution: convert the grid into a set of (i, j, c) tuples
# perform flood-fill algorithm repeatedly on the set
def make_set(grid):
    s = set()
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            s.add((i, j, c))
    return s

# flood-fill algorithm (https://en.wikipedia.org/wiki/Flood_fill)
# points is a set of tuples (i, j, characteristic)
# node is a single tuple representing the starting point
# returns a set of all tuples within the region,
# and removes those points from the original set.
def flood_fill(points, node):
    out = set()

    def flood_recurse(points, node, out):
        if node in points:
            i, j, c = node
            points.remove(node)
            out.add(node)
            flood_recurse(points, (i+1, j, c), out)
            flood_recurse(points, (i-1, j, c), out)
            flood_recurse(points, (i, j+1, c), out)
            flood_recurse(points, (i, j-1, c), out)

    flood_recurse(points, node, out)
    return out

#get the first item of a set.
def get_first(s):
    for x in s:
        break
    return x

# calculate the area of a group of point tuples.
def area(group):
    return len(group)

# calculate the perimeter of a group of point tuples.
def perimeter(group):
    delta = ((1, 0), (-1, 0), (0, 1), (0, -1))
    perimeter = 0
    for p in group:
        for d in delta:
            i, j, c = p
            di, dj = d
            if (i + di, j + dj, c) not in group:
                perimeter += 1
    return perimeter

# idea: create a set of points (i, j normal) representing tiles that are around the perimeter
# of the shape. then, use flood-fill again to join them together into groups each representing a side.
def num_sides(group):
    delta = ((1, 0, "u"), (-1, 0, "d"), (0, 1, "r"), (0, -1, "l"))
    perimeter = set()
    for p in group:
        for d in delta:
            i, j, c = p
            di, dj, dn = d
            if (i + di, j + dj, c) not in group:
                perimeter.add((i + di, j + dj, dn))
    sides = 0
    while len(perimeter) > 0:
        flood_fill(perimeter, get_first(perimeter))
        sides += 1
    return sides

def part_one(raw, lines, grid):
    points = make_set(grid)
    score = 0
    while len(points) > 0:
        group = flood_fill(points, get_first(points))
        score += area(group) * perimeter(group)
    return score

def part_two(raw, lines, grid):
    points = make_set(grid)
    score = 0
    while len(points) > 0:
        group = flood_fill(points, get_first(points))
        score += area(group) * num_sides(group)
    return score
