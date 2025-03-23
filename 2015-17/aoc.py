#!/usr/bin/env pypy3

from collections import Counter
from itertools import combinations
from more_itertools import ilen


MultiLineExample = """\
20
15
10
5
5
"""

ExamplesPart1 = (
    (MultiLineExample, 4),
)

ExamplesPart2 = (
    (MultiLineExample, 3),
)


def parse(s):
    return [int(x) for x in s.splitlines()]


def solutions(jugs, volume):
    yield from (c for n in range(len(jugs) + 1) for c in combinations(jugs, n) if sum(c) == volume)


def part1(s, volume=150):
    jugs = parse(s)
    return ilen(solutions(jugs, volume))


def part2(s, volume=150):
    jugs = parse(s)
    c = Counter(map(len, solutions(jugs, volume)))
    return c[min(c.keys())]


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1):
        c = part1(a, 25)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 (1304)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a, 25)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (18)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
