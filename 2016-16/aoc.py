#!/usr/bin/env pypy3

import numpy as np


ExampleInput1 = """\
10000
"""


def parse(s):
    return list(map(int, s.strip()))


def generate(iv, space):
    arr = np.zeros(space, bool)
    n = len(iv)
    arr[:n] = iv[:]
    while n < space:
        a0 = None
        if (delta := 2*n + 1 - space) > 0:
            a0 = delta - 1

        src = slice(n - 1, a0, -1)
        dst = slice(n + 1, 2*n + 1)

        arr[dst] = np.logical_not(arr[src])
        n = 2*n + 1
    return arr


def checksum(d):
    while len(d) % 2 == 0:
        d = np.logical_not(np.logical_xor(d[::2], d[1::2]))
    return d.astype(int)


def part1(s, space=272):
    d = generate(parse(s), space)
    c = checksum(d)
    return "".join(map(str, c))


def part2(s):
    return part1(s, 35651584)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (01100)")
    print(part1(ExampleInput1, space=20))

    print()
    print("Part 1 (10100011010101011)")
    print(part1(real_input()))

    print()
    print("Part 2 (01010001101011001)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
