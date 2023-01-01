#!/usr/bin/env python3

import functools as ft
import itertools as it
import operator

ExampleInput1 = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""


def parse(s):
    return (eval(L) for L in s.splitlines() if L != "")


def paircmp(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a - b

    if isinstance(a, list) and isinstance(b, list):
        for a_, b_ in it.zip_longest(a, b):
            if a_ is None:
                return -1
            if b_ is None:
                return 1
            if r := paircmp(a_, b_):
                return r
        return 0

    if isinstance(a, int):
        a = [a]
    if isinstance(b, int):
        b = [b]
    return paircmp(a, b)


def part1(s):
    pairs = iter(parse(s))
    return sum(
        i
        for i, (a, b) in enumerate(zip(pairs, pairs), start=1)
        if paircmp(a, b) < 0
    )


def part2(s):
    DIVS = ([[2]], [[6]])
    pairs = list(parse(s))
    pairs += DIVS
    pairs.sort(key=ft.cmp_to_key(paircmp))
    return ft.reduce(operator.mul, (pairs.index(d) + 1 for d in DIVS))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (13)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (4821)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (140)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (21890)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
