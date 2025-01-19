#!/usr/bin/env pypy3


import itertools as it
from collections import defaultdict


ExampleInput1 = """\
.#.
..#
###
"""


def parse(s):
    lines = s.splitlines()
    return [(x, y) for y in range(len(lines)) for x in range(len(lines[0])) if lines[y][x] == '#']


def subcube(p):
    ndim = len(p)
    x, y, z, *rest = p
    a = [None] * 3**ndim
    i = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                if ndim == 3:
                    a[i] = (x+dx, y+dy, z+dz)
                    i += 1
                else:
                    for dw in range(-1, 2):
                        a[i] = (x+dx, y+dy, z+dz, rest[0] + dw)
                        i += 1
    return a


def run(iv, niter, ndim):
    src = { p + (0,) * (ndim - 2) for p in iv }

    for i in range(niter):
        counts = defaultdict(int)

        for p in src:
            for n in subcube(p):
                counts[n] += 1

        dst = set()
        for p, n in counts.items():
            if n == 3 or (n == 4 and p in src):
                dst.add(p)

        src = dst

    return len(src)


def part1(s):
    return run(parse(s), 6, 3)


def part2(s):
    return run(parse(s), 6, 4)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (112)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (276)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (848)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (2136)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
