#!/usr/bin/env python3

import itertools
from pathlib import Path

ExampleInput1 = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""


def make_sums(s):
    ints = [1]
    for line in s.splitlines():
        ints.append(0)
        if n := line.split()[1:]:
            ints.append(int(n[0]))
    return list(itertools.accumulate(ints))


def part1(s):
    CYCLES_OF_INTEREST = (20, 60, 100, 140, 180, 220)
    sums = make_sums(s)
    return sum(c * sums[c - 1] for c in CYCLES_OF_INTEREST)


def part2(s):
    SCREEN_WIDTH = 40
    TOTAL_PIXELS = 240
    sums = make_sums(s)
    chars = []
    for c in range(TOTAL_PIXELS):
        X = sums[c]
        px = c % SCREEN_WIDTH
        if c > 0 and px == 0:
            chars.append("\n")
        if X - 1 <= px <= X + 1:
            chars.append("#")
        else:
            chars.append(".")

    return "".join(chars)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print('Example Part 1 (want 13140)')
    print(part1(ExampleInput1))

    print()
    print('Part 1')
    print(part1(real_input()))

    print()
    print('Example Part 2')
    print(part2(ExampleInput1))

    print()
    print('Part 2')
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
