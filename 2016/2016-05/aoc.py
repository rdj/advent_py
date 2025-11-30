#!/usr/bin/env python3

import _md5
import re
from itertools import count, islice

ExampleInput1 = "abc"


def md5(s):
    return _md5.md5(s, usedforsecurity=False).hexdigest()


def pwiter(s):
    s = bytes(s.strip(), "ascii")
    for n in count():
        d = md5(s + bytes(str(n), "ascii"))
        if m := re.match(r"00000(.)(.)", d):
            yield m[1], m[2]


def part1(s):
    return "".join([a[0] for a in islice(pwiter(s), 8)])


def part2(s):
    a = [None] * 8
    it = pwiter(s)
    while any(c is None for c in a):
        i, c = next(it)
        try:
            i = int(i)
        except ValueError:
            continue

        if 0 <= i < 8 and a[i] is None:
            a[i] = c
    return "".join(a)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (18f47a30)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (2414bc77)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (05ace8e3)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (437e60fc)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
