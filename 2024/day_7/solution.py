# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = False

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

# brute force approach:
# generate all possible combinations of operators,
# see if any of them equal the expected result
#
# This approach is feasible, but took about 20 seconds
# to solve part 2.
#
# heuristics:
# [before optimization, part 2 took about 21 seconds to run on my laptop.]
# all operators grow the expected result. We can immediately stop calculating if
# at any point the result exceeds the expected value.
# [only saves about a second, oof]

def evaluate(nbrs, ops, v):
    res = nbrs[0]
    funcs = {
        "+": lambda a, b: a + b,
        "*": lambda a, b: a * b,
        "c": lambda a, b: int(str(a) + str(b))
    }
    for i in range(1, len(nbrs)):
        res = funcs[ops[i-1]](res, nbrs[i])
        if res > v:
            break

    return res == v

def oper_pattern(ops, i, n):
    return [ops[(i // len(ops)**j) % len(ops)] for j in range(n)]

def sum_valid_lines(lines, operators_to_try):
    sum = 0
    for line in lines:
        v, data = line.split(":")
        v = int(v)
        data = [int(d) for d in data.strip().split(" ")]
        n = len(data)-1
        for i in range(len(operators_to_try)**n):
            if evaluate(data, oper_pattern(operators_to_try, i, n), v):
                sum += v
                break
    return sum

def part_one(raw, lines, grid):
    return sum_valid_lines(lines, ["+", "*"])

def part_two(raw, lines, grid):
    return sum_valid_lines(lines, ["+", "*", "c"])
