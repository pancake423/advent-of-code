# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.

P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

def grid_apply(grid, fn):
    return [[fn(i, j, grid) for j in range(len(grid[i]))] for i in range(len(grid))]

def flatten(grid):
    out = []
    for row in grid:
        out += row
    return out

def to_int(grid):
    return grid_apply(grid, lambda i, j, grid: int(grid[i][j]))

def print_grid(grid):
    [print(row) for row in grid]


def tree_visible(i, j, grid):
    row = grid[i]
    col = [row[j] for row in grid]
    height = grid[i][j]
    cmps = [
        row[:j],
        row[j+1:],
        col[:i],
        col[i+1:],
    ]
    return height > min([max([-1] + l) for l in cmps])

def scenic_score(i, j, grid):
    row = grid[i]
    col = [row[j] for row in grid]
    height = grid[i][j]
    views = [
        list(reversed(row[:j])),
        row[j+1:],
        list(reversed(col[:i])),
        col[i+1:],
    ]
    score = 1
    for view in views:
        multiplier = 0
        for tree in view:
            multiplier += 1
            if tree >= height:
                break
        score *= multiplier
    return score

def part_one(raw, lines, grid):
    return flatten(grid_apply(to_int(grid), tree_visible)).count(True)

def part_two(raw, lines, grid):
    return max(flatten(grid_apply(to_int(grid), scenic_score)))
