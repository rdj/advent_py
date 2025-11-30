#!/usr/bin/env python3


import networkx as nx
from collections import deque
from functools import reduce


ExampleInput1 = """\
flqrgnkx
"""


################################################################################
# Knot Hash implementation from Day 10
#
# Reddit says I'm a dummy for thinking this is poorly written, but I had a lot
# of questions. The "suffix" provided here in Day 14 is applied to the key
# string and then that combined string is the input to Day 10 Part 2.
#
# Day 10 Part 2 is applied in its entirety, including adding the salt-like
# fixed 5-byte suffix value.
#
#   day10_part2( day17_input + "-" + "0"-"127" ) -> 128x 128-bit numbers -> ...

def run(inputs, start, rounds):
    a = deque(start)

    cur = 0
    skip = 0
    for _ in range(rounds):
        for n in inputs:
            b = deque()
            for _ in range(n):
                b.appendleft(a.popleft())
            a.extend(b)
            a.rotate(-skip)
            skip += 1

    a.rotate(rounds*sum(inputs) + (skip * (skip-1)) // 2)
    return list(a)


def salted(s):
    return list(map(ord, s.strip())) + [17, 31, 73, 47, 23]


def knothash(s):
    key = salted(s)
    a = run(key, range(256), 64)

    result = 0
    while a:
        chunk, a = a[:16], a[16:]
        result <<= 8
        result |= reduce(lambda a, b: a ^ b, chunk)

    return result

assert(f'{knothash("AoC 2017"):x}' == "33efeb34ea91902bb2f59c9920caa6cd")

################################################################################


def part1(s):
    key = s.strip()
    return sum(knothash(key + f"-{n}").bit_count() for n in range(128))


def neighbors(x, y):
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        x1, y1 = x + dx, y + dy
        if 0 <= x1 < 128 and 0 <= y1 < 128:
            yield x1, y1


def part2(s):
    key = s.strip()
    a = [list(map(int, "{0:0128b}".format(knothash(key + f"-{n}")))) for n in range(128)]

    g = nx.Graph()
    for y0 in range(len(a)):
        for x0 in range(128):
            if a[y0][x0]:
                g.add_node((x0, y0))
                for x1, y1 in neighbors(x0, y0):
                    if a[y1][x1]:
                        g.add_edge((x0, y0), (x1, y1))

    return nx.number_connected_components(g)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (8108)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (8222)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (1242)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1086)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
