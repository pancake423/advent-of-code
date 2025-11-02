# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

def parse_input(lines):
    return [[[int(n) for n in p.split("-")] for p in line.split(",")] for line in lines]

def contained(p1, p2):
    return p1[0] >= p2[0] and p1[1] <= p2[1]

def contained_both(p1, p2):
    return 1 if contained(p1, p2) or contained(p2, p1) else 0

def point_within(p, range):
    return p >= range[0] and p <= range[1]

def overlaps(p1, p2):
    tests = [
        (p1[0], p2),
        (p1[1], p2),
        (p2[0], p1),
        (p2[1], p1)
    ]
    return 1 if any(point_within( *test ) for test in tests) else 0

def part_one(raw, lines, grid):
    return sum(contained_both( *pair ) for pair in parse_input(lines))

def part_two(raw, lines, grid):
    return sum(overlaps( *pair ) for pair in parse_input(lines))
