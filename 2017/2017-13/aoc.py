#!/usr/bin/env python3

from itertools import count
from math import prod


ExampleInput1 = """\
0: 3
1: 2
4: 4
6: 4
"""


def parse(s):
    return tuple(tuple(map(int, line.split(":"))) for line in s.splitlines())


# 1 -> 0; 2 -> 2; 3 -> 4; 4 -> 6; 5 -> 8, 6 -> 10
# (r - 1) * 2
def icollisions(fw, t):
    for d, r in fw:
        if 0 == (d + t) % (2*(r-1)):
            yield (d, r)


def sev(fw):
    return sum(map(prod, icollisions(fw, 0)))


def tsafe(fw):
    for t in count():
        try:
            next(icollisions(fw, t))
        except(StopIteration):
            return t


def part1(s):
    return sev(parse(s))


def part2(s):
    return tsafe(parse(s))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (24)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (632)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (10)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (3849742)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
