# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #

from functools import reduce
from math import lcm

class Monkey:
    def __init__(self, raw_text, monkey_list):
        def last_word_int(line):
            return int(line.split(" ")[-1])

        self.monkey_list = monkey_list
        monkey_list.append(self)
        n, items, op, test, tc, fc  = raw_text.split("\n")[:6]
        self.items = [int(n) for n in items.split(":")[1].split(",")]
        self.op = op.split("=")[1].strip().split(" ")
        self.test = last_word_int(test)
        self.tc = last_word_int(tc)
        self.fc = last_word_int(fc)
        self.inspect_count = 0
        self.lcm = -1;

    def step(self, part_2 = False):
        # potential bug here: assumes that no monkey can throw items to themselves
        for item in reversed(self.items):
            #inspect item
            self.inspect_count += 1
            # perform operation
            # get the other value
            operand = item
            if (self.op[2] != "old"):
                operand = int(self.op[2])
            if self.op[1] == "+":
                item += operand
            elif self.op[1] == "*":
                item *= operand
            # monkey gets bored step
            if not part_2:
                item //= 3
            # test and throw to next monkey
            self.monkey_list[self.tc if item % self.test == 0 else self.fc].items.append(item % self.lcm if self.lcm != -1 else item)
        self.items = []

    def set_lcm(self, lcm):
        self.lcm = lcm

def parse_input(raw):
    l = []
    [Monkey(r, l) for r in raw.split("\n\n")]
    LCM = lcm(*[m.test for m in l])
    for m in l:
        m.set_lcm(LCM)

    return l

def monkey_business(monkeys):
    return reduce(lambda a, b: a*b, sorted((m.inspect_count for m in monkeys), reverse=True)[:2])

def part_one(raw, lines, grid):
    monkeys = parse_input(raw)
    for _ in range(20):
        for monkey in monkeys:
            monkey.step()
    return monkey_business(monkeys)

def part_two(raw, lines, grid):
    monkeys = parse_input(raw)
    for _ in range(10000):
        for monkey in monkeys:
            monkey.step(part_2 = True)
    return monkey_business(monkeys)
