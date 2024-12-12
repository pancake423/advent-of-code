# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = True

P2_EXAMPLE = False
P2_FULL = True
# ========================= #

# brute force approach:
# generate all possible combinations of operators,
# see if any of them equal the expected result
#
# This approach is feasible, but took about 20 seconds
# to solve part 2.

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

# naive/brute force approach
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

# recursive approach: only checking if we can match the expected value,
# not checking all possible values. Why is this so much faster???
def sum_valid_lines_2(lines, operators_to_try):
    sum = 0
    for line in lines:
        v, data = line.split(":")
        v = int(v)
        data = [int(d) for d in data.strip().split(" ")]
        if recursive_eval(data, operators_to_try, v):
            sum += v
    return sum

def inverse_concat(res, b):
    if len(str(int(res))) <= len(str(b)) or b != int(b) or b < 0:
        return -1
    return int(str(int(res))[:-len(str(b))])

forward = {
    "+": lambda a, b: a + b,
    "*": lambda a, b: a * b,
    "c": lambda a, b: int(str(a) + str(b)),
}
inverse = {
    "+": lambda res, b: res - b,
    "*": lambda res, b: res / b,
    "c": inverse_concat,
}

def recursive_eval(data, ops, v):
    if (v != int(v) or v < 0):
        return False
    if len(data) == 1:
        if data[0] == v:
            return True
        else:
            return False
    for o in ops:
        a = int(inverse[o](v, data[-1]))
        if a < 0 or forward[o](a, data[-1]) != v:
            continue
        if recursive_eval(data[:-1], ops, inverse[o](v, data[-1])):
            return True
    return False


def part_one(raw, lines, grid):
    return sum_valid_lines_2(lines, ["+", "*"])

def part_two(raw, lines, grid):
    return sum_valid_lines_2(lines, ["+", "*", "c"])
