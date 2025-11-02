# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

def parse_crates(raw):
    # get the rows of crates
    lines = list(reversed(raw.split("\n")[:-1]))
    max_l = max(len(line) for line in lines)
    lines = [line.ljust(max_l) for line in lines]
    cols = (max_l + 1) // 4

    col_contents = [[line[i * 4 + 1] for line in lines] for i in range(cols)]
    return [list(filter(lambda n: n != " ", col)) for col in col_contents]

def seq_to_dict(seq):
    out = {}
    for i in range(0, len(seq), 2):
        out[seq[i]] = int(seq[i+1])
    return out

def parse_moves(raw):
    return [seq_to_dict(line.split(" ")) for line in raw.split("\n")]

# mutates crates, because I am a bad person
def make_move(crates, move_dict):
    for i in range(move_dict["move"]):
        crates[move_dict["to"] - 1].append(crates[move_dict["from"] - 1].pop())


def make_move_9001(crates, move_dict):
    from_col = crates[move_dict["from"] - 1]
    to_col = crates[move_dict["to"] - 1]
    moved_crates = from_col[-move_dict["move"]:]
    crates[move_dict["from"] - 1] = from_col[:-move_dict["move"]]
    to_col += moved_crates


def get_message(crates):
    return "".join(crate[-1] for crate in crates)


def part_one(raw, lines, grid):
    crates_raw, moves_raw = raw.split("\n\n")
    crates = parse_crates(crates_raw)
    moves = parse_moves(moves_raw.strip())
    for move in moves:
        make_move(crates, move)
    return get_message(crates)

def part_two(raw, lines, grid):
    crates_raw, moves_raw = raw.split("\n\n")
    crates = parse_crates(crates_raw)
    moves = parse_moves(moves_raw.strip())
    for move in moves:
        make_move_9001(crates, move)
    return get_message(crates)
