#!/usr/bin/env pypy3

import re
from more_itertools import sliding_window

ExamplesPart1 = (
    ("abcdefgh", "abcdffaa"),
    ("ghijklmn", "ghjaabcc"),
)


MINVAL = ord("a")
MAXVAL = ord("z")

AVOID = tuple(map(ord, ("i", "o", "l")))

RUN_OF_THREE = re.compile("|".join(["".join(run) for run in sliding_window(map(chr, range(ord("a"), ord("z")+1)), 3)]))
TWO_DOUBLES = re.compile(r"(.)\1.*(.)\2")


def increment_one(n):
    carry = False
    n += 1
    if n in AVOID:
        n += 1
    if n > MAXVAL:
        n = MINVAL
        carry = True
    return n, carry


def increment_arr(a):
    a = list(reversed(a))
    carry = True
    for i, n in enumerate(a):
        if carry:
            a[i], carry = increment_one(a[i])
        if a[i] in AVOID:
            a[i], carry = increment_one(a[i])
            for j in range(i):
                a[j] = MINVAL
    if carry:
        a.append(MINVAL)
    return reversed(a)


def increment_str(s):
    return "".join([chr(x) for x in increment_arr([ord(c) for c in s])])


def is_valid(s):
    return RUN_OF_THREE.search(s) and TWO_DOUBLES.search(s)


def part1(s):
    s = s.strip()
    while True:
        s = increment_str(s)
        if is_valid(s):
            return s


def part2(s):
    return part1(part1(s))


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

    print("Part 1 (hxbxxyzz)")
    print(part1(real_input()))
    print()

    print("Part 2 (hxcaabcc)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
