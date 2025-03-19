#!/usr/bin/env pypy3

import _md5
from itertools import count

def md5(s):
    return _md5.md5(s, usedforsecurity=False).hexdigest()


ExamplesPart1 = (
    ("abcdef", 609043),
    ("pqrstuv", 1048970),
)


def find_leading_zeros(s, zeros=5):
    prefix = "0" * zeros

    seed = bytes(s.strip(), "ascii")
    for n in count():
        if md5(seed + bytes(str(n), "ascii"))[:zeros] == prefix:
            return n


def part1(s):
    return find_leading_zeros(s)


def part2(s):
    return find_leading_zeros(s, 6)


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

    print("Part 1 (117946)")
    print(part1(real_input()))
    print()

    print("Part 2 (3938038)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
