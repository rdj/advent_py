#!/usr/bin/env pypy3

import re


ExamplesPart1 = (
    ("ADVENT", 6),
    ("A(1x5)BC", 7),
    ("(3x3)XYZ", 9),
    ("A(2x2)BCD(2x2)EFG", 11),
    ("(6x1)(1x3)A", 6),
    ("X(8x2)(3x3)ABCY", 18),
)

ExamplesPart2 = (
    ("(3x3)XYZ", 9),
    ("X(8x2)(3x3)ABCY", 20),
    ("(27x12)(20x12)(13x14)(7x10)(1x12)A", 241920),
    ("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN", 445),
)


def expandlen(s, recur=False):
    if m := re.search(r"\((\d+)x(\d+)\)", s):
        j, x = map(int, m.groups())
        before, after = m.span()
        midlen = j
        if recur:
            midlen = expandlen(s[after:after+j], recur)
        return before + midlen * x + expandlen(s[after+j:], recur)
    else:
        return len(s)


def part1(s):
    return expandlen(s.strip())


def part2(s):
    return expandlen(s.strip(), recur=True)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1):
        print(f"Example Part 1.{i} ({b})")
        print(part1(a))
        print()

    print("Part 1 (74532)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        print(f"Example Part 2.{i} ({b})")
        print(part2(a))
        print()

    print("Part 2 (11558231665)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
