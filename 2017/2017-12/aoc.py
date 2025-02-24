#!/usr/bin/env pypy3

import networkx as nx


ExampleInput1 = """\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
"""


def parse(s):
    g = nx.Graph()

    for src, dst in map(lambda x: x.split(" <-> "), s.splitlines()):
        src = int(src)
        for d in map(int, dst.split(", ")):
            g.add_edge(src, d)

    return g


def part1(s):
    g = parse(s)
    return len(nx.node_connected_component(g, 0))


def part2(s):
    g = parse(s)
    return nx.number_connected_components(g)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (6)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (115)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (2)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (221)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
