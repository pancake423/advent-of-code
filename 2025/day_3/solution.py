# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #


def max_sublist(l, n):
    # where l is a list of digits,
    # and n is the number of digits in the sublist
    if n == 1:
        return [max(l)]
    idx = 0
    max_v = 0
    for i, d in enumerate(l[: -n + 1]):
        if d > max_v:
            idx = i
            max_v = d

    return [max_v] + max_sublist(l[idx + 1 :], n - 1)


# convert a list of digits to an integer
def to_int(list):
    return int("".join([str(n) for n in list]))


def part_one(raw, lines, grid):
    return sum(to_int(max_sublist([int(n) for n in line], 2)) for line in grid)


def part_two(raw, lines, grid):
    return sum(to_int(max_sublist([int(n) for n in line], 12)) for line in grid)
