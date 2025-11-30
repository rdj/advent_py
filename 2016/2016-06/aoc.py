#!/usr/bin/env python3

from collections import Counter

ExampleInput1 = """\
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
"""


def decode(s, weight):
    lines = s.splitlines()
    counts = [Counter() for _ in range(len(lines[0]))]

    for line in lines:
        for i, c in enumerate(line):
            counts[i][c] += weight

    return "".join(c.most_common(1)[0][0] for c in counts)


def part1(s):
    return decode(s, 1)


def part2(s):
    return decode(s, -1)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (easter)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (dzqckwsd)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (advent)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (lragovly)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
