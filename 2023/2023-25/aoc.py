#!/usr/bin/env python3

from colors import color
import pygraphviz as pgv
import math


ExampleInput1 = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

def parse(s):
    g = pgv.AGraph()
    for line in s.splitlines():
        src, rest = line.split(": ")
        for dst in rest.split():
            g.add_edge(src, dst)
    return g

# I feel like the graphviz AGraph class should be able to do this, but none of
# the things I tried worked right away.
def count_connected(g, start):
    visited = set()
    visited.add(start)

    q = [start]
    while q:
        n = q.pop()
        for n in g.neighbors(n):
            if n not in visited:
                visited.add(n)
                q.append(n)

    return len(visited)

def part1(s):
    g = parse(s)

    g.layout()
    g.draw('part1.png')
    # easy enought to just look at the graph and see which edges to delete

    to_remove = (('dfk', 'nxk'), ('ldl', 'fpg'), ('lhn', 'hcf'))
    for a, b in to_remove:
        g.remove_edge(a, b)

    return math.prod(count_connected(g, _) for _ in to_remove[0])

def part2(s):
    return "TODO"


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    # print("Example Part 1")
    # print(part1(ExampleInput1))

    print()
    print("Part 1")
    print(part1(real_input()))


if __name__ == "__main__":
    run_all()
