import time

# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = True

P2_EXAMPLE = False
P2_FULL = True
# ========================= #

def part_one(raw, lines, grid):
    stones = [int(n) for n in lines[0].strip().split(" ")]
    return dict_solve(stones, 25)

def inc(d, v, amt):
    if v in d:
        d[v] += amt
    else:
        d[v] = amt

def step_dict(d):
    out = {}
    for v in d.keys():
        if v == 0:
            inc(out, 1, d[v])
            continue
        s = str(v)
        l = len(s)
        if l % 2 == 0:
            inc(out, int(s[:l // 2]), d[v])
            inc(out, int(s[l // 2:]), d[v])
            continue
        inc(out, v*2024, d[v])
    return out


def dict_solve(stones, n):
    stones_dict = {}
    for s in stones:
        if s in stones_dict:
            stones_dict[s] += 1
        else:
            stones_dict[s] = 1
    for i in range(n):
        stones_dict = step_dict(stones_dict)
    return sum(stones_dict.values())


def part_two(raw, lines, grid):
    stones = [int(n) for n in lines[0].strip().split(" ")]
    return dict_solve(stones, 75)
