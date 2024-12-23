#!/usr/bin/env pypy3

import networkx as nx

ExampleInput1 = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def parsegraph(s):
    G = nx.Graph()
    for a, b in [line.split("-") for line in s.splitlines()]:
        G.add_edge(a, b)
    return G


def part1nx(s):
    G = parsegraph(s)
    count = 0
    for c in nx.enumerate_all_cliques(G):
        if len(c) == 3 and any(n.startswith('t') for n in c):
            count += 1
        elif len(c) > 3:
            break
    return count


def part2nx(s):
    G = parsegraph(s)
    cliques = list(nx.find_cliques(G))
    cliques.sort(key=len)
    return ",".join(sorted(cliques[-1]))


def parse(s):
    return tuple(tuple(line.split("-")) for line in s.splitlines())


from collections import defaultdict
from itertools import combinations


def build_edges(pairs):
    edges = defaultdict(set)
    for a, b in pairs:
        edges[a].add(b)
        edges[b].add(a)
    return edges


def enlarge_cliques(edges, known):
    bigger = set()
    for clique in known:
        x = set.intersection(*[edges[n] for n in clique])
        for c in x:
            bigger.add(tuple(sorted([c, *clique])))
    return bigger


def part1(s):
    pairs = parse(s)
    edges = build_edges(pairs)
    cliques = enlarge_cliques(edges, pairs)
    return sum(1 for c in cliques if any(n.startswith('t') for n in c))


def part2(s):
    pairs = parse(s)
    edges = build_edges(pairs)

    known = pairs
    bigger = None
    while True:
        bigger = enlarge_cliques(edges, known)
        if len(bigger) == 0:
            assert(len(known) == 1)
            return ",".join(list(known)[0])
        known = bigger


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (7)")
    print(part1nx(ExampleInput1))

    print()
    print("Part 1 (1156)")
    print(part1nx(real_input()))

    print()
    print("Example Part 2 (co,de,ka,ta)")
    print(part2nx(ExampleInput1))

    print()
    print("Part 2 (bx,cx,dr,dx,is,jg,km,kt,li,lt,nh,uf,um)")
    print(part2nx(real_input()))


if __name__ == "__main__":
    run_all()
