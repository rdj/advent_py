#!/usr/bin/env python3

import math
import re

from functools import reduce

ExampleInput1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

ExampleInput2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

ExampleInput3 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

def parse_nodes(lines):
    nodes = {}
    for line in lines:
        name, left, right = re.findall(r'[A-Z0-9]{3}', line)
        nodes[name] = (left, right)
    return nodes


def parse(s):
    lines = s.splitlines()
    prog = lines[0]
    nodes = parse_nodes(lines[2:])
    return prog, nodes


def do_once(prog, nodes, start='AAA'):
    cur = start
    steps = 0
    while not cur.endswith('Z'):
        index = 0
        if prog[steps % len(prog)] == 'R':
            index = 1
        cur = nodes[cur][index]
        steps += 1

    return steps


def part1(s):
    prog, nodes = parse(s)
    return do_once(prog, nodes)


def part2(s):
    prog, nodes = parse(s)

    starts = [_ for _ in nodes.keys() if _.endswith('A')]
    cycles = [do_once(prog, nodes, _) for _ in starts]

    return reduce(math.lcm, cycles, 1)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (6)")
    print(part1(ExampleInput2))

    print()
    print("Part 1 (21389)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (6)")
    print(part2(ExampleInput3))

    print()
    print("Part 2 (21083806112641)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
