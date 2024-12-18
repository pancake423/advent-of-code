from math import sin, cos, atan2, pi, inf

# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = True

P2_EXAMPLE = False
P2_FULL = True
# ========================= #

def sign(n):
    if n == 0:
        return 0
    if n < 0:
        return -1
    return 1

def points_of_interest(grid):
    # find the start, end, and all pathway tiles
    s = (-1, -1)
    e = (-1, -1)
    paths = set()
    intersections = set()
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c != "#":
                paths.add((i, j))
            if c == "S":
                s = (i, j)
                continue
            if c == "E":
                e = (i, j)
                continue
    # pathway tiles that have both a horizontal and vertical connection
    # are intersections.
    for path in paths:
        v = 0
        h = 0
        i, j = path
        if (i+1, j) in paths:
            v += 1
        if (i-1, j) in paths:
            v += 1
        if (i, j+1) in paths:
            h += 1
        if (i, j-1) in paths:
            h += 1
        if v > 0 and h > 0 or path == s or path == e:
            intersections.add((i, j))
    return s, e, paths, intersections

def make_graph(paths, intersections):
    # graph represented as a dict of point: edges
    # slightly special because edges also need to
    # contain direction and cost information.
    # each edge is a tuple (pos, dir, cost)
    graph = {}
    for intersection in intersections:
        graph[intersection] = []
        for d in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            i, j = intersection
            i += d[0]
            j += d[1]
            cost = 1
            while (i, j) in paths:
                if (i, j) in intersections:
                    graph[intersection].append(((i, j), d, cost))
                i += d[0]
                j += d[1]
                cost += 1
    return refactor_graph(graph)

def rotate_90deg(d, cw=True):
    theta = atan2(*d) + (pi/2)* (1 if cw else -1)
    return round(sin(theta)), round(cos(theta))

def closest_node(nodes):
    min = inf
    min_n = (((-1, -1), (-1, -1)), -1)
    for node, dist in nodes.items():
        if dist < min:
            min = dist
            min_n = node
    return min_n, min

def dijkstra(start, graph):
    # shit implementation, really slow but it works
    visited = {}
    unvisited = {}
    for v in graph.keys():
        unvisited[v] = 0 if v == start else inf

    while True:
        node, cost = closest_node(unvisited)
        if cost == inf:
            break
        for edge_node, edge_cost in graph[node]:
            if edge_node in unvisited and unvisited[edge_node] > cost + edge_cost:
                unvisited[edge_node] = cost + edge_cost
        visited[node] = cost
        del unvisited[node]

    return visited

def all_sssp_nodes(s, e, graph, sssp):
    max_d = min([dist if pos == e else inf for (pos, _), dist in sssp.items()])
    visited = set() # of nodes
    active = set() # of nodes
    # find all nodes at position e with weight max_d
    for node, dist in sssp.items():
        pos, _ = node
        if pos == e and dist == max_d:
            active.add(node)

    while len(active) > 0:
        next = set()
        for node in active:
            visited.add(node)
            for edge_node, edge_cost in graph[node]:
                if sssp[edge_node] == sssp[node] - edge_cost:
                    next.add(edge_node)
        active = next
    return set(pos for pos, _ in visited)


def refactor_graph(g):
    # make a standard v: (e, w) representation
    graph = {}
    # each vertex is represented as (pos, dir)
    for pos in g.keys():
        for d in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            graph[(pos, d)] = set([((pos, rotate_90deg(d)), 1000), ((pos, rotate_90deg(d, False)), 1000)])
    for pos in g.keys():
        for e in g[pos]:
            p, d, c = e
            graph[(pos, d)].add(((p, d), c))
            graph[(p, d)].add(((pos, d), c))
    return graph

def all_tiles(grid, nodes):
    node_list = list(nodes)
    tiles = set()
    for a in range(len(nodes)):
        for b in range(a+1, len(nodes)):
            n1 = node_list[a]
            n2 = node_list[b]
            # check if nodes are axis-aligned
            if n1[0] - n2[0] == 0 or n1[1] - n2[1] == 0:
                d = (sign(n1[0] - n2[0]), sign(n1[1] - n2[1]))
                i, j = n2
                ok = True
                while (i, j) != n1:
                    if grid[i][j] == "#":
                        ok = False
                        break
                    i += d[0]
                    j += d[1]
                if ok:
                    i, j = n2
                    while (i, j) != n1:
                        tiles.add((i, j))
                        i += d[0]
                        j += d[1]
                    tiles.add((i, j))
    return tiles

def draw(grid, tiles):
    RED='\033[1;31m'
    NC='\033[0m'
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if (i, j) in tiles:
                print(RED + "O" + NC, end="")
                continue
            print(c, end="")
        print()


def part_one(raw, lines, grid):
    s, e, paths, intersections = points_of_interest(grid)
    graph = make_graph(paths, intersections)
    sssp = dijkstra((s, (0, 1)), graph)
    return min([dist if pos == e else inf for (pos, _), dist in sssp.items()])

def part_two(raw, lines, grid):
    s, e, paths, intersections = points_of_interest(grid)
    graph = make_graph(paths, intersections)
    sssp = dijkstra((s, (0, 1)), graph)
    nodes = all_sssp_nodes(s, e, graph, sssp)
    tiles = all_tiles(grid, nodes)
    draw(grid, tiles)
    return len(tiles)
