def read_file(filename):
    raw = None
    lines = None
    grid = None
    with open(filename) as f:
        raw = f.read()
    lines = raw.strip().split("\n")
    grid = [[c for c in line.strip()] for line in lines]
    return raw, lines, grid


example_data = read_file("example.txt")
data = read_file("input.txt")


def part_one(raw, lines, grid):
    pass


def part_two(raw, lines, grid):
    pass


if __name__ == "__main__":
    print("Part one (example input):", part_one(*example_data))
    # print("Part one (full input):", part_one(*data))
    # print("Part two (example input):", part_two(*example_data))
    # print("Part two (full input):", part_two(*data))
