def get_contents(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def filter_blank(items: list[str]) -> list[str]:
    return list(filter(lambda s: s != "", items))


def get_cell(grid, x, y):
    if x < 0 or y < 0 or y >= len(grid) or x >= len(grid[0]):
        return "."
    return grid[y][x]


def set_cell(grid, x, y, val):
    if x < 0 or y < 0 or y >= len(grid) or x >= len(grid[0]):
        return
    grid[y][x] = val


def part_one(filename):
    file = get_contents(filename)
    lines = file.split("\n")[:-1]
    grid = [list(line) for line in lines]

    split_count = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "S" or cell == "|":
                if y + 1 >= len(grid):
                    continue
                if get_cell(grid, x, y + 1) == ".":
                    set_cell(grid, x, y + 1, "|")
                if get_cell(grid, x, y + 1) == "^":
                    set_cell(grid, x + 1, y + 1, "|")
                    set_cell(grid, x - 1, y + 1, "|")
                    split_count += 1

    return split_count


# the big optimization here is counting the multiplicity (AKA number of possible
# timelines arriving at that point) of the beam at each
# location rather than keeping a copy to represent each timeline. The number
# of timelines grows exponentially, but the number of beam locations at each layer is
# limited by the size of the grid.
def part_two(filename):
    file = get_contents(filename)
    lines = file.split("\n")[:-1]
    grid = [list(line) for line in lines]
    beams = set()
    beam_multiplicites = {}
    splitters = set()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "S":
                beams.add((x, y))
                beam_multiplicites[(x, y)] = 1
            if cell == "^":
                splitters.add((x, y))

    for _ in range(len(grid)):
        next_beams = set()
        for beam in beams:
            mul = beam_multiplicites[beam]
            step = (beam[0], beam[1] + 1)
            new_beams = []
            if step in splitters:
                new_beams.append((beam[0] + 1, beam[1] + 1))
                new_beams.append((beam[0] - 1, beam[1] + 1))
            else:
                new_beams.append(step)

            for new_beam in new_beams:
                if new_beam in next_beams:
                    beam_multiplicites[new_beam] += mul
                else:
                    next_beams.add(new_beam)
                    beam_multiplicites[new_beam] = mul

        beams = next_beams

    return sum(beam_multiplicites[beam] for beam in beams)


print("part one")
print("example:", part_one("example.txt"))
print("input:", part_one("input.txt"), "\n")

print("part two")
print("example:", part_two("example.txt"))
print("input:", part_two("input.txt"))
