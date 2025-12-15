# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

from math import ceil


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


def first_half(n):
    s = str(n)
    return int(s[: ceil(len(s) / 2)])


def solve_fast_p1(lines):
    total = 0
    for r in parse_ranges(lines):
        low = first_half(r[0])
        high = first_half(r[1])
        if low > high:
            low //= 10
        for i in range(low, high + 1):
            n = int(str(i) * 2)
            if r[0] <= n <= r[1]:
                total += n
    return total


def solve_fast_p2(lines):
    total = 0
    for r in parse_ranges(lines):
        matches = set()
        max_l = len(str(r[1]))
        min_l = len(str(r[0]))
        low = first_half(r[0])
        high = first_half(r[1])
        if low > high:
            high *= 10
        for n in range(low, high + 1):
            s = str(n)
            for i in range(1, len(s) + 1):
                pattern = s[:i]
                cmp = int(pattern * (max_l // i))
                if max_l > 1 and r[0] <= cmp <= r[1]:
                    matches.add(cmp)
                cmp = int(pattern * (min_l // i))
                if min_l > 1 and r[0] <= cmp <= r[1]:
                    matches.add(cmp)
        total += sum(matches)
    return total


def part_one(raw, lines, grid):
    # sum = 0
    # for r in parse_ranges(lines):
    #     for i in range(r[0], r[1] + 1):
    #         if repeated_digits(i):
    #             sum += i
    # return sum
    return solve_fast_p1(lines)


def part_two(raw, lines, grid):
    # sum = 0
    # for r in parse_ranges(lines):
    #     for i in range(r[0], r[1] + 1):
    #         if repeated_pattern(i):
    #             sum += i
    # return sum
    return solve_fast_p2(lines)
