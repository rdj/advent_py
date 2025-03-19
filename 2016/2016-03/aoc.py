#!/usr/bin/env pypy3

import numpy as np
from more_itertools import batched


def parse(s):
    return tuple(tuple(map(int, line.split())) for line in s.splitlines())


def ntri(arr):
    return sum(1 for a, b, c in arr if a + b > c and a + c > b and b + c > a)


def part1(s):
    return ntri(parse(s))


def part2(s):
    return ntri(batched(np.transpose(parse(s)).flatten(), n=3))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Part 1 (1050)")
    print(part1(real_input()))

    print()
    print("Part 2 (1921)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
