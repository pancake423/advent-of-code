from math import floor, inf

# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = True

P2_EXAMPLE = False
P2_FULL = True
# ========================= #
a = 0
b = 0
c = 0
pointer = 0
output = []
program = []

def literal_operand(n):
    return n

def combo_operand(n):
    if n <= 3:
        return n
    if n == 4:
        return a
    if n == 5:
        return b
    if n == 6:
        return c
    return -1

def adv(n):
    global a, pointer
    a = a // (2 ** combo_operand(n))
    pointer += 2

def bxl(n):
    global b, pointer
    b = b ^ literal_operand(n)
    pointer += 2

def bst(n):
    global b, pointer
    b = combo_operand(n) % 8
    pointer += 2

def jnz(n):
    global pointer
    if a != 0:
        pointer = literal_operand(n)
        return
    pointer += 2

def bxc(n):
    global b, pointer
    b = b ^ c
    pointer += 2

def out(n):
    global pointer
    output.append(combo_operand(n) % 8)
    pointer += 2

def bdv(n):
    global pointer, b
    b = a // (2 ** combo_operand(n))
    pointer += 2

def cdv(n):
    global pointer, c
    c = a // (2 ** combo_operand(n))
    pointer += 2

def init(lines):
    global a, b, c, pointer, program
    pointer = 0
    a = int(lines[0].split(":")[1])
    b = int(lines[1].split(":")[1])
    c = int(lines[2].split(":")[1])

    program = [int(n) for n in lines[4].split(":")[1].strip().split(",")]

# used for the massive amount of debugging this puzzle required :)
def status():
    print("="*10)
    print("A:", a)
    print("B:", b)
    print("C:", c)
    print()
    print("Program:")
    print(", ".join([str(n) for n in program]))
    for n in program:
        if n < pointer:
            print(" "*len(str(n)), end="  ")
            continue
        print("^")
        break
    print()
    print("Output:", output)
    print("="*10)

def step():
    opcode = program[pointer]
    operand = program[pointer+1]
    instr = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
    instr[opcode](operand)

def run():
    while True:
        if pointer >= len(program):
            break
        step()

def write_output():
    return ",".join([str(n) for n in output])

def part_one(raw, lines, grid):
    init(lines)
    run()
    return write_output()

# run the program with a given value in the A register
def try_a(a_register):
    global a, b, c, pointer, output
    a = a_register
    b = 0
    c = 0
    pointer = 0
    output = []
    run()
    return [n for n in output]

# used for converting base-8 numbers (where digits correspond to output digits)
# back into base 10 for the answers.
def base_n_to_10(n, list):
    # n is an array of digits, most significant first
    out = 0
    pow = 0
    for digit in reversed(list):
        out += digit * n**pow
        pow += 1
    return out


def part_two(raw, lines, grid):
    init(lines)

    # initial observation: the modulo 8 output operations mean that, in base 8,
    # every digit roughly corresponds to a different output digit.

    # new observation: multiple values can sometimes result in the same output digit.
    # we need to search all possible digits that give that value in the output,
    # not just the first one.
    search_strings = [[0]*len(program)]
    #nth digit of search string corresponds to last digit of output
    for n in range(len(program)):
        new_search_strings = []
        for string in search_strings:
            matching_digits = []
            cpy = [d for d in string]
            for j in range(8):
                cpy[n] = j
                i = base_n_to_10(8, cpy)
                try_a(i)
                if output[-1-n] == program[-1-n]:
                    matching_digits.append(j)
            for j in matching_digits:
                cpy = [d for d in string]
                cpy[n] = j
                new_search_strings.append(cpy)
        search_strings = new_search_strings
    min_i = inf
    for string in search_strings:
        i = base_n_to_10(8, string)
        if i < min_i:
            min_i = i
    return min_i
