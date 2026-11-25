# I got tired of writing string parsing code in zig NGL

def get_contents(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

def filter_blank(items: list[str])->list[str]:
    return list(filter(lambda s: s != "", items))

file = get_contents("input.txt")
rows = filter_blank(file.split("\n"))
ops = filter_blank(rows.pop().split(" "))
columns = ["".join([row[i] if i < len(row) else "" for row in rows]).strip() for i in range(max(len(row) for row in rows))]
columns.append("")

grand_total = 0
for op in ops:
    if (op == "*"):
        total = 1
        value = columns.pop(0)
        while (value != ""):
            total *= int(value)
            value = columns.pop(0)
        grand_total += total

    if(op == "+"):
        value = columns.pop(0)
        while (value != ""):
            grand_total += int(value)
            value = columns.pop(0)

print(grand_total)
