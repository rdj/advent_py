#!/usr/bin/env python3

import re

from functools import reduce
from operator import mul


ExampleInput1 = """\
Time:      7  15   30
Distance:  9  40  200
""".strip()


def parse(s):
    lines = s.splitlines();
    times = [int(_) for _ in lines[0].split()[1:]]
    distances = [int(_) for _ in lines[1].split()[1:]]
    return list(zip(times, distances))

def part1(s):
    races = parse(s)

    results = []

    for r in races:
        t, d = r
        wins = 0
        for n in range(t):
            if (t - n) * n > d:
                wins += 1
        results.append(wins)

    return reduce(mul, results, 1)


def find_lower(t, d):
    for n in range(t):
        if (t - n) * n > d:
            return n
    raise Exception("found no lower bound")


def find_upper(t, d):
    for n in range(t, 0, -1):
        if (t - n) * n > d:
            return n
    raise Exception("found no upper bound")


def part2(s):
    t, d = [int(re.sub(r'\s+','', line).split(':')[-1]) for line in s.splitlines()]

    lower = find_lower(t,d)
    upper = find_upper(t,d)

    return upper + 1 - lower


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read().strip()


def run_all():
    print("Example Part 1 (288)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (281600)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (71503)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (33875953)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
