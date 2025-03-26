#!/usr/bin/env pypy3

from math import sqrt
from itertools import count


def factors(n):
    factors = []
    for f in range(1, int(sqrt(n)) + 1):
        q, r = divmod(n, f)
        if r == 0:
            factors.append(f)
            if f != q:
                factors.append(q)
    return factors


def part1(s):
    want = int(s.strip()) // 10
    for n in count(1):
        if sum(factors(n)) > want:
            return n


def part2(s):
    want = int(s.strip())
    for n in count(1):
        if sum(11*f for f in factors(n)[:50]) > want:
            return n


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Part 1 (786240)")
    print(part1(real_input()))
    print()

    print("Part 2 (831600)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
