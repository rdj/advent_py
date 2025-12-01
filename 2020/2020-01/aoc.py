#!/usr/bin/env python3

from itertools import product    ## Cartesian product
from math import prod


MultiLineExample = """\
1721
979
366
299
675
1456
"""

ExamplesPart1 = (
    (MultiLineExample, 514579),
)

ExamplesPart2 = (
    (MultiLineExample, 241861950),
)


def parse(s):
    return list(map(int, s.splitlines()))


def prodsum(total, groups):
    for g in groups:
        if sum(g) == total:
            return prod(g)
    raise Exception("sum not found")


def part1(s):
    nums = parse(s)
    pairs = product(nums, nums)
    return prodsum(2020, pairs)


def part2(s):
    nums = parse(s)
    trips = product(nums, nums, nums)
    return prodsum(2020, trips)


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

    print("Part 1 (744475)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (70276940)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
