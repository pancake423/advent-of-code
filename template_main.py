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
    # cancel if data is all whitespace
    if len(data[0].strip()) == 0:
        return
    t0 = time.perf_counter()
    res = func(*data)
    t1 = time.perf_counter()
    # cancel if function does not return a value
    if res == None:
        return
    print(msg, end=" ")
    print(res)
    print("\t" + f"[ran in {int((t1 - t0)*1000)}ms.]")

if __name__ == "__main__":
    run("Part one (example input)", sln.part_one, "example.txt")
    run("Part one (full input)", sln.part_one, "input.txt")
    run("Part two (example input)", sln.part_two, "example.txt")
    run("Part two (full input)", sln.part_two, "input.txt")
