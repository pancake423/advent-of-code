import math

example_data = None
data = None

with open("example.txt") as f:
    example_data = f.readlines()
with open("input.txt") as f:
    data = f.readlines()


def part_one(data):
    return sum([is_safe([int(n) for n in r.split()]) for r in data])


def is_safe(levels):
    sign = levels[-1] - levels[0]
    for i in range(len(levels)-1):
        delta = levels[i+1] - levels[i]
        if delta * sign <= 0 or abs(delta) > 3:
            return 0
    return 1


def part_two(data):
    # not very efficient but whatever
    safe = 0
    for report in data:
        levels = [int(n) for n in report.split()]
        one_removed = [levels] + [levels[0:i]+levels[i+1:] for i in range(len(levels))]
        safe += max(is_safe(l) for l in one_removed)
    return safe


if __name__ == "__main__":
    # print("Part one (example input):", part_one(example_data))
    print("Part one (full input):", part_one(data))
   #  print("Part two (example input):", part_two(example_data))
    print("Part two (full input):", part_two(data))
