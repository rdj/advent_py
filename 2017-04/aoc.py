#!/usr/bin/env pypy3

from collections import Counter


ExampleInput1 = """\
aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa
"""

ExampleInput2 = """\
abcde fghij
abcde xyz ecdab
a ab abc abd abf abj
iiii oiii ooii oooi oooo
oiii ioii iioi iiio
"""


def part1(s):
    return sum(1 for line in s.splitlines() if all(v == 1 for v in Counter(line.split()).values()))


def frozencounter(s):
    return tuple(sorted(Counter(s).items()))


def part2(s):
    # Woops, I used frozenset first and it worked for my input but then I went
    # back to add the example and realized my mistake.
    return sum(1 for line in s.splitlines() if all(v == 1 for v in Counter(map(frozencounter, line.split())).values()))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (2)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (325)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (3)")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (119)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
