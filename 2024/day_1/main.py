import math

example_data = None
data = None

with open("example.txt") as f:
    example_data = f.readlines()
with open("input.txt") as f:
    data = f.readlines()


def part_one(data):
    split = [d.split() for d in data]
    l1 = sorted([int(s[0]) for s in split])
    l2 = sorted([int(s[-1]) for s in split])
    sum = 0
    for i, j in zip(l1, l2):
        sum += abs(i - j)
    return sum

def part_two(data):
    split = [d.split() for d in data]
    l1 = [int(s[0]) for s in split]
    l2 = [int(s[-1]) for s in split]
    sim_score = 0
    for i in l1:
        sim_score += i * l2.count(i)
    return sim_score



if __name__ == "__main__":
    # print("Part one (example input):", part_one(example_data))
    print("Part one (full input):", part_one(data))
    # print("Part two (example input):", part_two(example_data))
    print("Part two (full input):", part_two(data))
