# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

def make_pipe( *fns ):
    def pipe(input_data):
        state = input_data
        for fn in fns:
            state = fn(state)
        return state
    return pipe

# transforms ["A Y", "B X", "C Z"] into [["A", "Y"], ["B", "X"], ["C", "Z"]]
def split_lines(lines):
    return [line.split(" ") for line in lines]

decoder = {
    "A" : "R",
    "B" : "P",
    "C" : "S",
    "X" : "R",
    "Y" : "P",
    "Z" : "S"
}
game = {"R": 1, "P": 2, "S": 3} # +1 = win, -1 = lose
game_inverted = {
    1 : "R",
    2 : "P",
    3 : "S"
}

# transforms [["A", "Y"], ["B", "X"], ["C", "Z"]] into [["R", "P"], ["P", "R"], ["S", "S"]]
def decode(lines):
    return [[decoder[char] for char in line] for line in lines]

def decode_2(lines):
    # now, x means lose, y means draw, z means win
    return [decode_line(your_choice, opp_choice) for (your_choice, opp_choice) in lines]

def decode_line(your_choice, opp_choice):
    strat_map = {
        "X": -1,
        "Y": 0,
        "Z": 1
    }
    o = decoder[your_choice]
    y = game_inverted[(game[o] - 1 + strat_map[opp_choice]) % len(game) + 1]

    return [o, y]

def choice_points(char):
    return game[char]

def win_points(opp_choice, your_choice):
    outcomes = {
        0: 3, # delta of zero means tie (3pts)
        1: 6, # delta of 1 or -2 means win
        1 - len(game): 6,
        -1: 0, #delta of -1 or 2
        len(game) - 1: 0
    }
    return outcomes[game[your_choice] - game[opp_choice]]



def round_points(games):
    return [choice_points(your_choice) + win_points(opp_choice, your_choice) for (opp_choice, your_choice) in games]

def part_one(raw, lines, grid):
    return make_pipe(split_lines, decode, round_points, sum)(lines)

def part_two(raw, lines, grid):
    return make_pipe(split_lines, decode_2, round_points, sum)(lines)
