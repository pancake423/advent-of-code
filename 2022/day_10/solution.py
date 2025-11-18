# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

def part_one(raw, lines, grid):
    pc = 0 # program counter
    x = 1
    cycle = 1
    wait_add = True
    measure_at = [n for n in range(20, 221, 40)]
    results = []
    while pc < len(lines)-1:
        if cycle in measure_at:
            results.append(cycle * x)
        cmd = lines[pc].split(" ")
        if cmd[0] == "addx":
            if wait_add:
                wait_add = False
            else:
                x += int(cmd[1])
                wait_add = True
                pc += 1
        elif cmd[0] == "noop":
            wait_add = True
            pc += 1
        cycle += 1

    return sum(results)

def part_two(raw, lines, grid):
    pc = 0 # program counter
    x = 1
    crt_x = 0
    cycle = 1
    wait_add = True
    out = "\n"
    while pc < len(lines)-1:
        cmd = lines[pc].split(" ")
        out += "█" if abs(crt_x - x) <= 1 else " "
        if cmd[0] == "addx":
            if wait_add:
                wait_add = False
            else:
                x += int(cmd[1])
                wait_add = True
                pc += 1
        elif cmd[0] == "noop":
            wait_add = True
            pc += 1
        cycle += 1
        crt_x += 1
        if crt_x >= 40:
            crt_x = 0
            out += "\n"

    return out
