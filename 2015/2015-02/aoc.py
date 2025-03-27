#!/usr/bin/env pypy3

from itertools import combinations
from math import prod


ExamplesPart1 = (
    ("2x3x4", 58),
    ("1x1x10", 43),
)

ExamplesPart2 = (
    ("2x3x4", 34),
    ("1x1x10", 14),
)


def parse(s):
    return tuple(tuple(map(int, line.split("x"))) for line in s.splitlines())


def part1(s):
    boxes = parse(s)
    total = 0

    for dims in boxes:
        areas = [a*b for a, b in combinations(dims, 2)]
        total += min(areas) + sum(2*a for a in areas)

    return total


def part2(s):
    boxes = parse(s)
    total = 0

    for dims in boxes:
        circs = [2*(a+b) for a, b in combinations(dims, 2)]
        vol = prod(dims)
        total += vol + min(circs)

    return total


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

    print("Part 1 (1588178)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (3783758)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
