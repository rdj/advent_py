#!/usr/bin/env python3

from collections import Counter
import re


MultiLineExample = """\
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""

ExamplesPart1 = (
    (MultiLineExample, 2),
)

ExamplesPart2 = (
    (MultiLineExample, 1),
)


def parse(s):
    entries = []
    for line in s.splitlines():
        a, b, c, pw = re.search(r'^(\d+)-(\d+) ([a-z]): ([a-z]+)$', line).groups()
        entries.append((int(a), int(b), c, pw))
    return entries


def part1(s):
    entries = parse(s)
    valid = 0
    for a, b, c, pw in entries:
        ctr = Counter(pw)
        if a <= ctr[c] <= b:
            valid += 1
    return valid


def part2(s):
    entries = parse(s)
    valid = 0
    for a, b, c, pw in entries:
        if (pw[a-1] == c) ^ (pw[b-1] == c):
            valid += 1
    return valid

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

    print("Part 1 (398)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (562)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
