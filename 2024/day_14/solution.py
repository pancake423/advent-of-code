from math import prod, lcm
# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = True

P2_EXAMPLE = False
P2_FULL = True
# ========================= #

def safety_score(robots, w, h):
    count = [0]*4
    for r in robots:
        (x, y), (dx, dy) = r
        if x == w//2 or y == h//2:
            continue
        count[(0 if x < w//2 else 1) + (0 if y < h//2 else 2)] += 1
    return prod(count)

def draw_scene(robots, w, h):
    out = ""
    map = [[0 for _ in range(w)] for _ in range(h)]
    for r in robots:
        x, y = r[0]
        map[y][x] += 1
    if max([n for row in map for n in row]) > 1:
        return
    for row in map:
        out += "".join([str(c) if c != 0 else "." for c in row]) + "\n"
    return out

def parse_line(line):
    return [[int(n) for n in s.split("=")[1].split(",")] for s in line.split(" ")]

def step_robot(r, w, h):
    p, v = r
    d = (w, h)
    return [[(p[i] + v[i]) % d[i] for i in range(len(p))], v]

def part_one(raw, lines, grid):
    w = 101
    h = 103
    robots = [parse_line(line) for line in lines]
    # draw_scene(robots, w, h)
    for _ in range(100):
        robots = [step_robot(r, w, h) for r in robots]

    # draw_scene(robots, w, h)
    return safety_score(robots, w, h)


def n_groups(robots):
    def get_first(s):
        for x in s:
            break
        return x

    def flood_fill(points, node):
        out = set()
        def flood_recurse(points, node, out):
            if node in points:
                i, j = node
                points.remove(node)
                out.add(node)
                flood_recurse(points, (i+1, j), out)
                flood_recurse(points, (i-1, j), out)
                flood_recurse(points, (i, j+1), out)
                flood_recurse(points, (i, j-1), out)
                flood_recurse(points, (i+1, j+1), out)
                flood_recurse(points, (i-1, j-1), out)
                flood_recurse(points, (i-1, j+1), out)
                flood_recurse(points, (i+1, j-1), out)

        flood_recurse(points, node, out)
        return out

    s = set([tuple(r[0]) for r in robots])
    groups = 0
    while len(s) > 0:
        flood_fill(s, get_first(s))
        groups += 1
    return groups

def part_two(raw, lines, grid):
    # how on earth to detect a picture??
    # probably, lots of grouping (flood fill???), not a lot of overlapping
    w = 101
    h = 103
    robots = [parse_line(line) for line in lines]
    n = 10000 # search depth, should be sufficient? (at least it is for mine)
    min_score = len(robots)*2
    min_loc = 0
    pic = draw_scene(robots, w, h)
    for i in range(n):
        robots = [step_robot(r, w, h) for r in robots]
        groups = n_groups(robots)
        if groups < min_score:
            min_score = groups
            min_loc = i + 1
            pic = draw_scene(robots, w, h)
    print(pic)
    return min_loc
