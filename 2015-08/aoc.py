#!/usr/bin/env pypy3

import re


MultiLineExample = """\
""
"abc"
"aaa\\"aaa"
"\\x27"
"""

ExamplesPart1 = (
    (MultiLineExample, 12),
)

ExamplesPart2 = (
    (MultiLineExample, 19),
)


def part1(s):
    lines = len(s.splitlines())
    escapes = re.findall(r'\\["\\]|\\x[0-9a-f][0-9a-f]', s)
    return 2*lines + sum(len(e) for e in escapes) - len(escapes)


def part2(s):
    lines = len(s.splitlines())
    specials = re.findall(r'[\\"]', s)
    return 2*lines + len(specials)


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

    print("Part 1 (1342)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (2074)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
