def read_file(filename):
    raw = None
    lines = None
    grid = None
    with open(filename) as f:
        raw = f.read()
    lines = raw.strip().split("\n")
    grid = [[c for c in line.strip()] for line in lines]
    return raw, lines, grid


example_data = read_file("example.txt")
data = read_file("input.txt")


def sum_middle_n(list_of_seq):
    return sum(s[len(s)//2] for s in list_of_seq)


def find_vertex(graph, v):
    for node in graph:
        if node["v"] == v:
            return node
    return {"v": -1, "e": [], "m":0}


def topological_sort(rules):
    graph = [] # each node is a dict of {v: int, e: []}
    # find unique numbers in rules, use as vertices in graph
    graph = [{"v": v, "e":[], "m": 0} for v in set(n for r in rules for n in r)]
    for rule  in rules:
        find_vertex(graph, rule[0])["e"].append(rule[1])

    # Topological sort alg
    # https://en.wikipedia.org/wiki/Topological_sorting
    # m = 0 -> unmarked
    # m = 1 -> temporary
    # m = 2 -> permanent
    L = []
    def visit(v):
        node = find_vertex(graph, v)
        if node["m"] >= 2:
            return
        if node["m"] == 1:
            raise ValueError("graph has a cycle")
        node["m"] = 1
        for vertex in node["e"]:
            visit(vertex)
        node["m"] = 2
        L.append(node["v"])

    # visit every node of the graph (so it works w/ disconnected graphs)
    for i in range(len(graph)):
        visit(graph[i]["v"])

    # create a lookup table out of the order of the topological sort
    L = list(reversed(L))
    table = {}
    for i, v in enumerate(L):
        table[v] = i
    return table


# ensure the sequence is strictly increasing based on its value
# in the lookup table.
def strict_increasing(seq, lookup):
    for i in range(len(seq)-1):
        if lookup[seq[i]] >= lookup[seq[i+1]]:
            return False
    return True


def parse_input(raw):
    rules, seq = raw.split("\n\n")
    rules = [[int(n) for n in r.split("|")] for r in rules.strip().split("\n")]
    seq = [[int(n) for n in s.split(",")] for s in seq.strip().split("\n")]
    return rules, seq

def applicable_rules(s, rules):
    return list(filter(lambda r: r[0] in s and r[1] in s, rules))


def part_one(raw, lines, grid):
    rules, seq = parse_input(raw)

    # construct a topological sort of a DAG* (rules are edges)
    # create lookup table (value -> order in topological sort)
    # check that every sequence is in strictly increasing order

    ok_seq = []
    for s in seq:
        lookup = topological_sort(applicable_rules(s, rules))
        if (strict_increasing(s, lookup)):
            ok_seq.append(s)

    return sum_middle_n(ok_seq)


def part_two(raw, lines, grid):
    rules, seq = parse_input(raw)

    # *creating a global lookup table turned out to not work
    # because the graph has cycles. instead, we filter the rules
    # applicable to the current sequence, and create a lookup table
    # out of just those rules.

    fixed_seq = []
    for s in seq:
        lookup = topological_sort(applicable_rules(s, rules))
        if not strict_increasing(s, lookup):
            fixed_seq.append(sorted(s, key=lambda n: lookup[n]))

    return sum_middle_n(fixed_seq)


if __name__ == "__main__":
    # print("Part one (example input):", part_one(*example_data))
    print("Part one (full input):", part_one(*data))
    # print("Part two (example input):", part_two(*example_data))
    print("Part two (full input):", part_two(*data))
