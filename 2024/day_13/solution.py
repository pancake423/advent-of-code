# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

def linear_solve(ax, ay, bx, by, cx, cy):
    x = (cx*by - bx*cy) / (ax*by - ay*bx)
    y = (ax*cy - cx*ay) / (ax*by - ay*bx)

    return x, y

def is_int(n):
    return n == int(n)

def get_inputs(raw, offset=0):
    out = []
    for rule_text in raw.split("\n\n"):
        a_line, b_line, prize_line = rule_text.split("\n")[:3]
        ax = int(a_line[a_line.find("X+")+2:a_line.find(",")])
        ay = int(a_line[a_line.find("Y+")+2:])
        bx = int(b_line[b_line.find("X+")+2:b_line.find(",")])
        by = int(b_line[b_line.find("Y+")+2:])
        cx = int(prize_line[prize_line.find("X=")+2:prize_line.find(",")])
        cy = int(prize_line[prize_line.find("Y=")+2:])
        out.append([ax, ay, bx, by, cx+offset, cy+offset])
    return out

def part_one(raw, lines, grid):
    a_price = 3
    b_price = 1

    total_cost = 0
    coeff = get_inputs(raw)

    for c in coeff:
        a, b = linear_solve(*c)
        if is_int(a) and is_int(b):
            total_cost += a_price*a + b_price*b
    return int(total_cost)


def part_two(raw, lines, grid):
    a_price = 3
    b_price = 1
    offset = 10000000000000

    total_cost = 0
    coeff = get_inputs(raw, offset)

    for c in coeff:
        a, b = linear_solve(*c)
        if is_int(a) and is_int(b):
            total_cost += a_price*a + b_price*b
    return int(total_cost)
