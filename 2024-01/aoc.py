#!/usr/bin/env python3

from colors import color
from collections import defaultdict
import re


ExampleInput1 = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""


def part1(s):
    pairs = [[int(_) for _ in re.split(r'\D+', line)] for line in s.splitlines()]
    cols = zip(*pairs)
    cols = [sorted(_) for _ in cols]
    pairs = zip(*cols)
    deltas = [abs(p[0] - p[1]) for p in pairs]
    return sum(deltas)


def part2(s):
    pairs = [[int(_) for _ in re.split(r'\D+', line)] for line in s.splitlines()]
    col1, col2 = zip(*pairs)

    counts = defaultdict(lambda: 0)
    for n in col2:
        counts[n] += 1

    scores = [n * counts[n] for n in col1]

    return sum(scores)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1")
    print(part1(ExampleInput1))

    print()
    print("Part 1")
    print(part1(real_input()))

    print()
    print("Example Part 2")
    print(part2(ExampleInput1))

    print()
    print("Part 2")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
