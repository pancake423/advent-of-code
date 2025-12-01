# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True


# ========================= #
def parse(line):
    return int(line.replace("R", "+").replace("L", "-"))


def part_one(raw, lines, grid):
    steps = [parse(line) for line in lines]
    counter = 0
    dial = 50
    for step in steps:
        dial += step
        dial %= 100
        if dial == 0:
            counter += 1
    return counter


def part_two(raw, lines, grid):
    # the easy way is to just simulate each click
    # steps = [parse(line) for line in lines]
    # counter = 0
    # dial = 50
    # for step in steps:
    #     d = 1 if step > 0 else -1
    #     n = abs(step)
    #     for _ in range(n):
    #         dial += d
    #         dial %= 100
    #         if dial == 0:
    #             counter += 1
    # return counter
    return part_two_fast(lines)


# this way is about 30x faster
def part_two_fast(lines):
    dial = 50
    counter = 0
    for line in lines:
        sign = 1
        if line[0] == "L":
            sign = -1
        n = int(line[1:])
        laps = n // 100
        r = n % 100
        steps_to_zero = 100 - dial if sign == 1 else dial

        counter += laps
        if steps_to_zero != 0 and r >= steps_to_zero:
            counter += 1
        dial += r * sign
        dial %= 100

    return counter
