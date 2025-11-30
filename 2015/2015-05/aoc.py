#!/usr/bin/env python3

import re

ExamplesPart1 = (
    ("ugknbfddgicrmopn", 1),
    ("aaa", 1),
    ("jchzalrnumimnmhp", 0),
    ("haegwjzuvuyypxyu", 0),
    ("dvszwmarrgswjxmb", 0),
)

ExamplesPart2 = (
    ("qjhvhtzxzqqjkmpb", 1),
    ("xxyxx", 1),
    ("uurcxstgmygtbstg", 0),
    ("ieodomkazucvgmuy", 0),
)


THREE_VOWELS = re.compile(r"[aeiou].*[aeiou].*[aeiou]")
DOUBLE_LETTER = re.compile(r"(.)\1")
BAD_PAIRS = re.compile(r"ab|cd|pq|xy")

def isnice1(s):
    return THREE_VOWELS.search(s) and DOUBLE_LETTER.search(s) and not BAD_PAIRS.search(s)


def part1(s):
    return sum(1 for word in s.splitlines() if isnice1(word))


REPEAT_PAIR = re.compile(r"(..).*\1")
ONE_APART = re.compile(r"(.).\1")

def isnice2(s):
    return ONE_APART.search(s) and REPEAT_PAIR.search(s)


def part2(s):
    return sum(1 for word in s.splitlines() if isnice2(word))


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

    print("Part 1 (255)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (55)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()

