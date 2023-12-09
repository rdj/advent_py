#!/usr/bin/env python3

from functools import reduce
import more_itertools as mit

ExampleInput1 = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def parse(s):
    return [list(map(int, line.split())) for line in s.splitlines()]


def get_diffs(line):
    diffs = [list(line)]
    while any(diffs[-1]):
        diffs.append([b - a for a, b in mit.windowed(diffs[-1], 2)])
    return diffs


def do_part1(parsed):
    futures = []
    for line in parsed:
        diffs = get_diffs(line)
        futures.append(sum(diff[-1] for diff in diffs))

    return sum(futures)


def part1(s):
    return do_part1(parse(s))


def part2(s):
    return do_part1(map(reversed, parse(s)))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (114)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (1930746032)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (2)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1154)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
