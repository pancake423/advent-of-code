# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = False

P2_EXAMPLE = True
P2_FULL = True
# ========================= #


def parse_ranges(lines):
    return [[int(n) for n in range.split("-")] for range in "".join(lines).split(",")]


def repeated_digits(n):
    s = str(n)
    l = len(s) // 2
    return s[:l] == s[l:]


def repeated_pattern(n):
    s = str(n)
    max_l = len(s) // 2
    for p in range(1, max_l + 1):
        cmp = s[:p]
        match = True
        for i in range(0, len(s), p):
            if s[i : i + p] != cmp:
                match = False
                break
        if match:
            return True
    return False


def part_one(raw, lines, grid):
    sum = 0
    for r in parse_ranges(lines):
        for i in range(r[0], r[1] + 1):
            if repeated_digits(i):
                sum += i
    return sum


def part_two(raw, lines, grid):
    sum = 0
    for r in parse_ranges(lines):
        for i in range(r[0], r[1] + 1):
            if repeated_pattern(i):
                sum += i
    return sum
