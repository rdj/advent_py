#!/usr/bin/env pypy3

from itertools import combinations, count
from math import prod


MultiLineExample = """\
1
2
3
4
5
7
8
9
10
11
"""

ExamplesPart1 = (
    (MultiLineExample, 99),
)

ExamplesPart2 = (
    (MultiLineExample, 44),
)


def parse(s):
    return tuple(map(int, s.splitlines()))


def run(s, div):
    boxes = parse(s)
    target = sum(boxes)//div

    for n in count():
        groups = [nums for nums in combinations(boxes, n) if sum(nums) == target]
        if groups:
            return min(map(prod, groups))


def part1(s):
    return run(s, 3)


def part2(s):
    return run(s, 4)


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

    print("Part 1 (11846773891)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (80393059)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
