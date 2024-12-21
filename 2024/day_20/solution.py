# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = True

P2_EXAMPLE = False
P2_FULL = True
# ========================= #

# important observations:
#
# there is only a single path from the start to the end (meaning, we can order tiles based on when
# they occur in the race and easily calculate the benefit of every skip).
#
# collisions can only be disabled once per race.
# I think you're only allowed to go through a single wall tile, since both entering and exiting
# the wall relies on breaking collisions.
#
# are there ever two path tiles that are diagonal to eachother?
# if not, skips always go in a straight line, never an elbow shape.

# returns a list of (i, j) tuples where the position in the list
# corresponds to the distance along the track.
def get_path(grid):
    track_tiles = set()
    start = (-1, -1)
    end = (-1, -1)
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c != "#":
                track_tiles.add((i, j))
            if c == "S":
                start = (i, j)
    path = [start]
    track_tiles.remove(start)
    while len(track_tiles) > 0:
        i, j = path[-1]
        for d in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            tile = (i + d[0], j + d[1])
            if tile in track_tiles:
                track_tiles.remove(tile)
                path.append(tile)
                break
    return path

def add(a, b):
    return tuple(a[i] + b[i] for i in range(len(b)))

def find_shortcuts(path, min_saved=0):
    # at every tile along the path:
    # try to go L, R, U, D two tiles
    # see if the first tile isn't in the path (ie, is a wall)
    # but the second tile is (a shortcut)
    # based on the index of the current tile and the destination tile, we can
    # determine how much time is saved.
    num_shortcuts = 0
    for i in range(len(path)):
        for d in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            p0 = path[i]
            p1 = add(p0, d)
            p2 = add(p1, d)
            if p1 not in path and p2 in path:
                j = path.index(p2)
                shortcut = (j - i) - 2
                if shortcut >= min_saved:
                    num_shortcuts += 1
                    #print(f"shortcut from {p0} to {p2} saves {shortcut} picoseconds.")
    return num_shortcuts

def part_one(raw, lines, grid):
    path = get_path(grid)
    return find_shortcuts(path, min_saved=100)


def manhattan(a, b):
    return sum([abs(a[i] - b[i]) for i in range(len(a))])
# new approach:
# use the manhattan distance (which will equal the length of the shortest path)
# between two nodes on the path to see if they are within shortcutting range
#
# nothing in the rules says a cheat HAS to go through walls for every step of its existence,
# just that it has to end up on a path in time.
#
# since cheats are defined by their start and end positions, they are inherently efficient:
# there are no cheats that waste time by shuffling, for example.
def find_shortcuts_n(path, shortcut_dist=20, min_saved=100):
    num_shortcuts = 0
    for i, p0 in enumerate(path):
        for j in range(i+1, len(path)):
            p1 = path[j]
            dist = manhattan(p0, p1)
            if dist <= shortcut_dist:
                shortcut = (j - i) - dist
                if shortcut >= min_saved:
                    num_shortcuts += 1
    return num_shortcuts

def part_two(raw, lines, grid):
    path = get_path(grid)
    return find_shortcuts_n(path, shortcut_dist=20, min_saved=100)
