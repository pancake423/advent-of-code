import math

example_data = None
data = None

with open("example.txt") as f:
    example_data = f.readlines()
with open("input.txt") as f:
    data = f.readlines()


def part_one(data):
    input_str = "".join(data);
    mul_start = []
    mul_end = []
    for i in range(len(input_str)):
        if input_str[i] == ")":
            mul_end.append(i)
        if i >= 4 and input_str[i-4:i] == "mul(":
            mul_start.append(i)

    res = 0
    for start in mul_start:
        # NOT EFFICIENT WHO CARES
        end = min(filter(lambda n: n > start, mul_end))
        args = input_str[start:end].split(",")
        if len(args) != 2:
            continue
        try:
            args = [int(n) for n in args]
            res += args[0] * args[1]
        except:
            pass
    return res

def part_two(data):
    input_str = "".join(data);
    cmd_words = ["do", "don't", "mul"]
    cmd_start = []
    cmd_type = []
    cmd_end = []
    for i in range(len(input_str)):
        if input_str[i] == ")":
            cmd_end.append(i)
        for cmd in cmd_words:
            if i >= len(cmd) and input_str[i-len(cmd)-1:i] == cmd + "(":
                cmd_start.append(i)
                cmd_type.append(cmd)

    res = 0
    mul_active = True
    for i, start in enumerate(cmd_start):
        cmd = cmd_type[i]
        if cmd == "do":
            mul_active = True
            continue
        if cmd == "don't":
            mul_active = False
            continue
        if not mul_active:
            continue
        end = min(filter(lambda n: n > start, cmd_end))
        args = input_str[start:end].split(",")
        if len(args) != 2:
            continue
        try:
            args = [int(n) for n in args]
            res += args[0] * args[1]
        except:
            pass
    return res



if __name__ == "__main__":
    # print("Part one (example input):", part_one(example_data))
    print("Part one (full input):", part_one(data))
    # print("Part two (example input):", part_two(example_data))
    print("Part two (full input):", part_two(data))
