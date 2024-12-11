import math

example_data = None
data = None

with open("example.txt") as f:
    example_data = f.readlines()
with open("input.txt") as f:
    data = f.readlines()

def letter(grid, i, j):
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
        return "."
    return grid[i][j]

def match(grid, pattern, i, j, di, dj):
    pattern_match = ""
    for k in range(len(pattern)):
        pattern_match += letter(grid, i + di*k, j + dj*k)
    return pattern_match == pattern

def part_one(data):
    grid = [[c for c in line.strip()] for line in data]
    deltas = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    matches = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            for d in deltas:
                if match(grid, "XMAS", i, j, *d):
                    matches += 1
    return matches

def part_two(data):
    grid = [[c for c in line.strip()] for line in data]

    matches = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if ((match(grid, "MAS", i-1, j-1, 1, 1) or match(grid, "MAS", i+1, j+1, -1, -1)) and
                (match(grid, "MAS", i-1, j+1, 1, -1) or match(grid, "MAS", i+1, j-1, -1, 1))):
                    matches += 1
    return matches


if __name__ == "__main__":
    print("Part one (example input):", part_one(example_data))
    print("Part one (full input):", part_one(data))
    print("Part two (example input):", part_two(example_data))
    print("Part two (full input):", part_two(data))
