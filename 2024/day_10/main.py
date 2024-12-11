import time
import solution as sln

def read_file(filename):
    raw = None
    with open(filename) as f:
        raw = f.read()
    lines = raw.strip().split("\n")
    grid = [[c for c in line.strip()] for line in lines]
    return raw, lines, grid

def run(msg, func, filename):
    data = read_file(filename)
    t0 = time.perf_counter()
    res = func(*data)
    t1 = time.perf_counter()
    print(msg, end=" ")
    print(res, end=" ")
    print(f"[{int((t1 - t0)*1000)}ms]")


if __name__ == "__main__":
    if sln.P1_EXAMPLE:
        run("Part one (example input):", sln.part_one, "example.txt")
    if sln.P1_FULL:
        run("Part one (full input):", sln.part_one, "input.txt")
    if sln.P2_EXAMPLE:
        run("Part two (example input):", sln.part_two, "example.txt")
    if sln.P2_FULL:
        run("Part two (full input):", sln.part_two, "input.txt")
