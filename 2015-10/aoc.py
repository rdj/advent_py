#!/usr/bin/env pypy3

from itertools import groupby
from more_itertools import ilen


ExamplesPart1 = (
    ("1", "11"),
    ("11", "21"),
    ("21", "1211"),
    ("1211", "111221"),
    ("111221", "312211"),
)


def parse(s):
    return [int(c) for c in s.strip()]


def expand(s):
    t = []
    for d, g in groupby(s):
        t += [ilen(g), d]
    return t


def part1(s, cycles=40):
    s = parse(s)
    for _ in range(cycles):
        s = expand(s)
    return len(s)


def part2(s):
    return part1(s, cycles=50)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1):
        c = "".join(map(str, expand(parse(a))))
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 (329356)")
    print(part1(real_input()))
    print()

    print("Part 2 (4666278)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
