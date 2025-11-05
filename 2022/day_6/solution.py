# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

# returns true iff every character of s in the substring [i, i+n) is unique
def unique(s, i, n = 4):
    return len(set(s[i:i+n])) == n

# returns the first position, p, in string s where the substring [0, p] contains n unique characters in a row
def first_unique_range(s, n):
    for i in range(len(s) - n):
        if unique(s, i, n):
            return i + n
    return -1

# just for fun, because solving an entire AoC puzzle in one line is pretty satisfying
def first_unique_range_oneliner(s, n):
    return min(i if len(set(s[i:i+n])) == n else len(s) for i in range(len(s) - n))

def part_one(raw, lines, grid):
    return first_unique_range(raw, 4)

def part_two(raw, lines, grid):
    return first_unique_range(raw, 14)
