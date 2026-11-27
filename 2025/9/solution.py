# this is probably the easiest puzzle of the entire event so far
from time import perf_counter


def part_one(filename: str) -> int:
    with open(filename, "r") as f:
        red_tiles = [
            tuple(int(n) for n in line.split(",")) for line in f.read().split("\n")[:-1]
        ]

        max_rect_size = 0
        for t1 in red_tiles:
            for t2 in red_tiles:
                rect_size = (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)
                max_rect_size = max(rect_size, max_rect_size)

        return max_rect_size


# so, as expected part two is really hard :)
def part_two(filename: str) -> int:
    with open(filename, "r") as f:
        red_tiles = [
            tuple(int(n) for n in line.split(",")) for line in f.read().split("\n")[:-1]
        ]

        # we need to be able to figure out which points are inside vs outside the tile path.
        # the grid is very large, so iterating over every possible X and Y coordinate isn't practical.
        # instead, we just track the interesting points on X and Y and know nothing important
        # happens between them.
        # (midpoints are necessary to figure out which regions are inside/outside the shape.
        # imagine a rectangular U-shaped region, there's no way to differentiate that the inside of the U isn't
        # part of the shape unless we track some point between the two ends)
        x_critical_points = add_midpoints(sorted({tile[0] for tile in red_tiles}))
        y_critical_points = add_midpoints(sorted({tile[1] for tile in red_tiles}))

        # optimization #2: lookup table for critical point indices
        # saves another 0.5s or so
        #
        # maps real x, y values to indices into the critical point lists (which are also
        # indices into the matrices defined later)
        x_lookup = {}
        y_lookup = {}
        for tile in red_tiles:
            x_lookup[tile[0]] = x_critical_points.index(tile[0])
            y_lookup[tile[1]] = y_critical_points.index(tile[1])

        # print(x_critical_points)
        # print(y_critical_points)


        # optimization #3
        # improve how the intersection matrix is calculated
        # no idea how on earth I cooked up the previous implementation
        # saved about 12.2s (50x speedup!)

        # for each cell in the intersection matrix, if True,
        # that point lies on the border of the path.
        intersection_matrix = [[False for _ in x_critical_points] for _ in y_critical_points]
        for i in range(len(red_tiles)-1):
            a = red_tiles[i]
            b = red_tiles[(i + 1) % len(red_tiles)]

            if (a[0] == b[0]):
                # vertical line
                x = x_lookup[a[0]]
                y_start = y_lookup[min(a[1], b[1])]
                y_end = y_lookup[max(a[1], b[1])]
                for y in range(y_start, y_end + 1):
                    intersection_matrix[y][x] = True
            else:
                # horizontal line
                y = y_lookup[a[1]]
                x_start = x_lookup[min(a[0], b[0])]
                x_end = x_lookup[max(a[0], b[0])]
                for x in range(x_start, x_end + 1):
                    intersection_matrix[y][x] = True


        # display_matrix = [["O" if cell else " " for cell in row] for row in intersection_matrix]
        # for tile in red_tiles:
        #     display_matrix[y_critical_points.index(tile[1])][x_critical_points.index(tile[0])] = "X"

        # for each cell in the interior matrix, if True,
        # that point lies inside the path.
        interior_matrix = []
        for y, row in enumerate(intersection_matrix):
            interior_row = []
            intersections = 0
            previous_cell = False
            in_horizontal_line = False
            for x, cell in enumerate(row):
                if cell:
                    interior_row.append(True)
                    if (previous_cell == True):
                        in_horizontal_line = True
                    intersections += 1
                else:
                    # if we were previously in a horizontal line (edge case that borks my code)
                    # whether we are inside or outside the shape can be determined by looking at the row above.
                    if in_horizontal_line:
                        if y == 0:
                            intersections = 0
                        else:
                            intersections = 1 if interior_matrix[y-1][x] else 0
                    interior_row.append(intersections % 2 != 0)
                    # if (intersections % 2 != 0):
                    #     display_matrix[y][x] = "."
                    in_horizontal_line = False
                previous_cell = cell
            interior_matrix.append(interior_row)

        # [print("".join(c for c in row)) for row in display_matrix]


        # now finally I have a way to test if any point is inside or outside the shape.
        # I claim that, for any rectangle, the rectangle is fully inside the shape if every
        # point on the perimeter of the rectangle is fully inside the shape.
        #
        # (this is only true because our shape's perimiter is drawn with a single line,
        # if it was discontinuous,this claim would not hold).

        max_rect_size = 0
        for t1 in red_tiles:
            for t2 in red_tiles:
                # optimization 1: don't bother checking the perimeter of rectangles that
                # can't possibly be the biggest
                # saves roughly 0.5s
                rect_size = (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)
                if rect_size < max_rect_size:
                    continue

                # find the indices of the four corners of the rectangle
                sx = x_lookup[min(t1[0], t2[0])]
                ex = x_lookup[max(t1[0], t2[0])]

                sy = y_lookup[min(t1[1], t2[1])]
                ey = y_lookup[max(t1[1], t2[1])]

                # now, check the perimeter
                # if any cell is not inside the path the rectangle is not valid.
                valid = True
                for x in range(sx, ex+1):
                    if not interior_matrix[sy][x] or not interior_matrix[ey][x]:
                        valid = False
                        break
                if not valid:
                    continue
                for y in range(sy, ey+1):
                    if not interior_matrix[y][sx] or not interior_matrix[y][ex]:
                        valid = False
                        break
                if not valid:
                    continue

                max_rect_size = max(rect_size, max_rect_size)

        return max_rect_size

# bug fix: allow critical points to exist between tiles, which I think fixes an edge
# case with two adjacent lines breaking the fill algorithm
#
# in any case, it doesn't break or slow down my puzzle input :)
def add_midpoints(points: list[int]) -> list[int|float]:
    midpoints = []
    for i in range(len(points) - 1):
            midpoints.append((points[i + 1] + points[i]) / 2)

    return sorted(midpoints + points)

start = perf_counter()
print("Part one:")
print("Example input:", part_one("example.txt"))
print("Actual input:", part_one("input.txt"))

print("Part two:")
print("Example input:", part_two("example.txt"))
print("Actual input:", part_two("input.txt"))
end = perf_counter()

print(f"\nTotal runtime: {end-start:.3f}s")
