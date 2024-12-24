# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run.
P1_EXAMPLE = False
P1_FULL = False

P2_EXAMPLE = False
P2_FULL = True
# ========================= #

def mix(a, b):
    return a ^ b

def prune(n):
    return n % 16777216

def next_secret(n):
    out = prune(mix(n, n*64))
    out = prune(mix(out, out//32))
    out = prune(mix(out, out*2048))
    return out

def part_one(raw, lines, grid):
    s = 0
    for line in lines:
        secret = int(line)
        for _ in range(2000):
            secret = next_secret(secret)
        # print(line, secret)
        s += secret
    return s

def sell_seq(prices, deltas, seq):
    l = len(seq)
    sell_price = 0
    for i, p in enumerate(prices):
        d = deltas[i]
        for j in range(len(d) - l):
            if d[j:j+l] == seq:
                sell_price += p[j+l]
                break
    return sell_price

def candidate_seqs(deltas, l=4):
    seqs = {}
    sell_price = 0
    for d in deltas:
        this_line = set()
        for j in range(len(d) - l):
            seq = tuple(d[j:j+l])
            if seq in this_line:
                continue
            this_line.add(seq)
            if seq in seqs:
                seqs[seq] += 1
            else:
                seqs[seq] = 1
    return seqs

def most_frequent(dict):
    m = max(dict.values())
    for key, value in dict.items():
        if value == m:
            return key



def part_two(raw, lines, grid):
    secrets = [[int(line)] for line in lines]
    for s in secrets:
        for _ in range(2000):
            s.append(next_secret(s[-1]))
    prices = [[n % 10 for n in s] for s in secrets]
    deltas = [[p[i+1] - p[i] for i in range(len(p)-1)] for p in prices]

    seqs = candidate_seqs(deltas)
    threshold = sell_seq(prices, deltas, list(most_frequent(seqs))) // 5
    seqs = [list(n[0]) for n in list(filter(lambda n: n[1] >= threshold, seqs.items()))]

    best_sell = 0
    for i, seq in enumerate(seqs):
        print(f"{i+1}/{len(seqs)}")
        sell = sell_seq(prices, deltas, list(seq))
        if sell > best_sell:
            best_sell = sell
    return best_sell
