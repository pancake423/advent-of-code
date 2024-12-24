# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = True

P2_EXAMPLE = False
P2_FULL = True
# ========================= #

numpad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [" ", "0", "A"]
]
numpad_init = (3, 2)

keypad = [
    [" ", "^", "A"],
    ["<", "v", ">"]
]
keypad_init = (0, 2)
# it will always be more efficient to do all of your horizontal and then
# all of your vertical (or vice versa), since the keypad controlling that robot
# can just spam A instead of having to use its arrow keys.
# I think that I need to check both possibilities (h/v and v/h) for each decision we make.
# -> will lead to more branching, but it should be acceptable.
#
# greedy: short path at previous layer is always going to be better

def get_coords(pad, key):
    for i, row in enumerate(pad):
        for j, k in enumerate(row):
            if k == key:
                return (i, j)
    raise ValueError(f"key '{key}' not in pad '{pad}'")

def shortest_sequence(control_pad, start_pos, seq):
    pos = start_pos
    out_seq = []
    for key in seq:
        goal_pos = get_coords(control_pad, key)
        di = goal_pos[0] - pos[0]
        dj = goal_pos[1] - pos[1]
        if dj < 0:
            out_seq += ["<"]*abs(dj)
        if dj > 0:
            out_seq += [">"]*dj
        if di < 0:
            out_seq += ["^"]*abs(di)
        if di > 0:
            out_seq += ["v"]*di
        pos = goal_pos
        out_seq.append("A")
    return "".join(out_seq)

def all_shortest_seq(control_pad, start_pos, seq):
    pos = start_pos
    sequences = set([""])
    for key in seq:
        next_sequences = set()
        goal_pos = get_coords(control_pad, key)
        for out_seq in sequences:
            di = goal_pos[0] - pos[0]
            dj = goal_pos[1] - pos[1]
            vertical = ""
            horiz = ""
            if dj < 0:
                horiz += "<"*abs(dj)
            if dj > 0:
                horiz += ">"*dj
            if di < 0:
                vertical += "^"*abs(di)
            if di > 0:
                vertical += "v"*di
            next_sequences.add(out_seq + vertical + horiz + "A")
            next_sequences.add(out_seq + horiz + vertical + "A")
        pos = goal_pos
        sequences = next_sequences
    return sequences

def complexity(line, seq):
    print(line, seq)
    return int(line[:-1])*len(seq)

# returns a list of optimal sequences at the given depth
def solve_puzzle(lines, robot_keypads=2):
    seqs = []
    # theory: choosing between going v or h first only matters at the numpad layer, not the keypad layer
    for line in lines:
        seq = all_shortest_seq(numpad, numpad_init, line)
        seq = list(filter(lambda s: verify(numpad, numpad_init, s), seq))
        for i in range(robot_keypads):
            seq = [n for s in seq for n in all_shortest_seq(keypad, keypad_init, s)]
            seq = list(filter(lambda s: verify(numpad, numpad_init, s), seq))
            # make sure to only keep items of minimum length
            min_l = min(len(s) for s in seq)
            seq = list(filter(lambda s: len(s) == min_l, seq))

        example_longest = get(seq)
        seqs.append(example_longest)
    return seqs

def verify(pad, pad_start, seq):
    pos = pad_start
    bad_pos = get_coords(pad, " ")
    for instr in seq:
        if instr == "^":
            pos = (pos[0]-1, pos[1])
        if instr == "v":
            pos = (pos[0]+1, pos[1])
        if instr == "<":
            pos = (pos[0], pos[1]-1)
        if instr == ">":
            pos = (pos[0], pos[1]+1)
        if pos == bad_pos:
            return False
    return True

def get(seq):
    for s in seq:
        return s

def part_one(raw, lines, grid):
    seqs = solve_puzzle(lines, robot_keypads=2)
    return sum(complexity(lines[i], seqs[i]) for i in range(len(seqs)))


# too expensive; string of characters itself becomes too long
# each code has the same length string??? (why)
#
# observation: each action at one layer corresponds to an A press at the next higher layer
# each sequence ending in an A will always expand into the same sequence at the next layer.
#
'''
depth: 0 length: 2 code length: 12 depth: 1 length: 2 code length: 28
depth: 2 length: 2 code length: 68
depth: 3 length: 1 code length: 160
depth: 4 length: 1 code length: 390
depth: 5 length: 1 code length: 958
depth: 6 length: 1 code length: 2366
depth: 7 length: 1 code length: 5840
depth: 8 length: 1 code length: 14428
depth: 9 length: 1 code length: 35644
depth: 10 length: 1 code length: 88074
depth: 11 length: 1 code length: 217622
depth: 12 length: 1 code length: 537738
depth: 13 length: 1 code length: 1328732
depth: 14 length: 1 code length: 3283268
depth: 15 length: 1 code length: 8112880
depth: 16 length: 1 code length: 20046758
depth: 17 length: 1 code length: 49535118
'''

def make_dict(list):
    d = {}
    for n in list:
        if n in d:
            d[n] += 1
        else:
            d[n] = 1
    return d

def seq_length(dict):
    l = 0
    for key, value in dict.items():
        l += len(key) * value
    return l

def step_dict(d):
    next = {}
    for seq, count in d.items():
        sub_actions = make_dict(sane_split(get(all_shortest_seq(keypad, keypad_init, seq)), "A"))
        for sub_seq, sub_count in sub_actions.items():
            if sub_seq in next:
                next[sub_seq] += sub_count * count
            else:
                next[sub_seq] = sub_count * count
    return next

def sane_split(string, char):
    out = []
    prev = 0
    for i in range(len(string)):
        if string[i] == char:
            out.append(string[prev:i+1])
            prev = i+1
    return out

def part_two(raw, lines, grid):
    seqs = solve_puzzle(lines, robot_keypads=5)
    count = 0
    for i, s in enumerate(seqs):
        d = make_dict(sane_split(s, "A"))
        for _ in range(20):
            d = step_dict(d)
        count += int(lines[i][:-1]) * seq_length(d)
    return count
