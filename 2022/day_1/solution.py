# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

def calories_per_elf(raw):
    return [sum(int(item_txt) for item_txt in elf_txt.split("\n")) for elf_txt in raw.strip().split("\n\n")]

def part_one(raw, lines, grid):
    return max(calories_per_elf(raw))

def part_two(raw, lines, grid):
    return sum(sorted(calories_per_elf(raw))[-3:])
