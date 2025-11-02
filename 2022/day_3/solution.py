# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

def split_line(line):
    hl = len(line) // 2
    return [line[:hl], line[hl:]]

def common_items( *args ):
    common = set(args[0])
    for arg in args:
        common &= set(arg)
    return list(common)

def priority(char):
    ord_c = ord(char)
    if ord_c >= 97:
        return ord_c - ord("a") + 1
    return ord_c - ord("A") + 27

def group_lines(lines, n):
    i = 0
    out = []
    while i < len(lines):
        item = []
        for j in range(n):
            item.append(lines[i])
            i += 1
        out.append(item)
    return out



def part_one(raw, lines, grid):
    # split lines in half
    return sum([priority(common_items( *split_line(line) )[0]) for line in lines])

def part_two(raw, lines, grid):
    return sum([priority(common_items( *group )[0]) for group in group_lines(lines, 3)])
