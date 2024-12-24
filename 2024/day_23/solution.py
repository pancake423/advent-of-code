# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = False

P2_EXAMPLE = True
P2_FULL = True
# ========================= #
def add_edge(graph, start, end):
    if start in graph:
        graph[start].append(end)
    else:
        graph[start] = [end]

def make_graph(edges):
    graph = {}
    for edge in edges:
        add_edge(graph, *edge)
        add_edge(graph, *list(reversed(edge)))
    return graph

def find_triples(graph):
    triples = set()
    for a, l in graph.items():
        for i in range(len(l)):
            for j in range(i+1, len(l)):
                if l[i] in graph[l[j]]:
                    triples.add(tuple(sorted([a, l[i], l[j]])))
    return triples

def part_one(raw, lines, grid):
    edges = [l.split("-") for l in lines]
    graph = make_graph(edges)
    triples = find_triples(graph)
    return len(list(filter(lambda n: any(['t' == m[0] for m in n]), triples)))

def grow_groups(groups, graph):
    next_groups = set()
    for group in groups:
        for node, connections in graph.items():
            if all(n in connections for n in group):
                next_groups.add(frozenset(list(group) + [node]))
    return next_groups

def part_two(raw, lines, grid):
    edges = [l.split("-") for l in lines]
    graph = make_graph(edges)

    largest_groups = set()
    groups = set(frozenset([n]) for n in graph.keys())
    tracker = 0
    while len(groups) > 0:
        tracker += 1
        largest_groups = groups
        print(f"searching {len(groups)} groups of size {tracker}.")
        groups = grow_groups(groups, graph)

    for g in largest_groups:
        return ",".join(sorted(list(g)))
