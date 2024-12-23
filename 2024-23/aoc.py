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


def parse(s):
    G = nx.Graph()
    for a, b in [line.split("-") for line in s.splitlines()]:
        G.add_edge(a, b)
    return G


def part1(s):
    G = parse(s)
    count = 0
    for c in nx.enumerate_all_cliques(G):
        if len(c) == 3 and any(n.startswith('t') for n in c):
            count += 1
        elif len(c) > 3:
            break
    return count


def part2(s):
    G = parse(s)
    cliques = list(nx.find_cliques(G))
    cliques.sort(key=len)
    return ",".join(sorted(cliques[-1]))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (7)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (1156)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (co,de,ka,ta)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (bx,cx,dr,dx,is,jg,km,kt,li,lt,nh,uf,um)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
