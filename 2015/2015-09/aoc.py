#!/usr/bin/env python3

import networkx as nx
from itertools import permutations


MultiLineExample = """\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""

ExamplesPart1 = (
    (MultiLineExample, 605),
)

ExamplesPart2 = (
    (MultiLineExample, 982),
)



def parse(s):
    G = nx.Graph()
    for line in s.splitlines():
        toks = line.split()
        G.add_edge(toks[0], toks[2], weight=int(toks[-1]))
    return G


def part1(s):
    G = parse(s)

    # NetworkX just making it convenient to get path lengths. It does have a
    # TSP solver, but it's heuristic approximations because that's what you do
    # in real life. For this puzzle, we need brute force.
    return min(nx.path_weight(G, path, "weight") for path in permutations(G.nodes))

def part2(s):
    G = parse(s)
    return max(nx.path_weight(G, path, "weight") for path in permutations(G.nodes))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1):
        c = part1(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 (251)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (898)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
