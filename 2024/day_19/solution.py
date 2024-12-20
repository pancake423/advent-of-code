# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = True

P2_EXAMPLE = False
P2_FULL = True
# ========================= #

# not really sure where to go with this one? gonna mess around with some stuff
def match(design, towel, idx):
    if idx + len(towel) > len(design):
        return False
    for i in range(len(towel)):
        if design[i+idx] != towel[i]:
            return False
    return True

def all_matches(design, towels, idx):
    return list(filter(lambda t: match(design, t, idx), towels))

def all_combos(design, towels):
    # dynamic programming is so hot
    n_combos = [1] + [0]*len(design)
    for idx in range(len(design)):
        for match in all_matches(design, towels, idx):
            n_combos[idx + len(match)] += n_combos[idx]
    return n_combos[-1]

def part_one(raw, lines, grid):
    towels = [[c for c in t] for t in lines[0].split(", ")]
    designs = [[c for c in l] for l in lines[2:]]

    return [all_combos(design, towels) > 0 for design in designs].count(True)

def part_two(raw, lines, grid):
    towels = [[c for c in t] for t in lines[0].split(", ")]
    designs = [[c for c in l] for l in lines[2:]]

    return sum(all_combos(design, towels) for design in designs)
