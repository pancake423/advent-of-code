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

        # we need to be able to figure out which points are inside vs outside the tile path
        x_critical_points = add_midpoints(sorted({tile[0] for tile in red_tiles}))
        y_critical_points = add_midpoints(sorted({tile[1] for tile in red_tiles}))

        # print(x_critical_points)
        # print(y_critical_points)

        # for each point in the matrix, if true,
        # that point lies on the border of the path.
        intersection_matrix = [[point_intersects_path((x, y), red_tiles) for x in x_critical_points] for y in y_critical_points]
        display_matrix = [["O" if cell else " " for cell in row] for row in intersection_matrix]
        for tile in red_tiles:
            display_matrix[y_critical_points.index(tile[1])][x_critical_points.index(tile[0])] = "X"

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
                    if (intersections % 2 != 0):
                        display_matrix[y][x] = "."
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
                # can index more efficiently w/ hash table if its a bottleneck
                sx = x_critical_points.index(min(t1[0], t2[0]))
                ex = x_critical_points.index(max(t1[0], t2[0]))

                sy = y_critical_points.index(min(t1[1], t2[1]))
                ey = y_critical_points.index(max(t1[1], t2[1]))

                # now, check the perimeter
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

                rect_size = (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)
                max_rect_size = max(rect_size, max_rect_size)

        return max_rect_size


def add_midpoints(points: list[int]) -> list[int]:
    midpoints = []
    for i in range(len(points) - 1):
        if points[i + 1] - points[i] > 1:
            midpoints.append((points[i + 1] + points[i]) // 2)

    return sorted(midpoints + points)


def point_intersects_path(point: tuple[int, int], path: list[tuple[int, int]]) -> bool:
    for i in range(len(path)):
        if point_intersects_line(point, path[i], path[(i + 1) % len(path)]):
            return True

    return False


def point_intersects_line(
    point: tuple[int, int], a: tuple[int, int], b: tuple[int, int]
) -> bool:
    return (
        # horizontal line with point in bounds
        a[1] == b[1] == point[1] and min(a[0], b[0]) <= point[0] <= max(a[0], b[0])
    ) or (
        # vertical line with point in bounds
        a[0] == b[0] == point[0] and min(a[1], b[1]) <= point[1] <= max(a[1], b[1])
    )

start = perf_counter()
print("Part one:")
print("Example input:", part_one("example.txt"))
print("Actual input:", part_one("input.txt"))

print("Part two:")
print("Example input:", part_two("example.txt"))
print("Actual input:", part_two("input.txt"))
end = perf_counter()

print(f"Total runtime: {end-start:.3f}s")
