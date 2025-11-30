#!/usr/bin/env python3

from itertools import count


ExampleInput1 = """\
0    2    7     0
"""


def parse(s):
    return list(map(int, s.strip().split()))


def run(s):
    a = parse(s)
    seen = {}

    for steps in count():
        if (state := tuple(a)) in seen:
            return steps, seen[state]
        seen[state] = steps

        i = a.index(max(a))
        n, a[i] = a[i], 0
        for _ in range(n):
            i = (i + 1) % len(a)
            a[i] += 1


def part1(s):
    last, first = run(s)
    return last


def part2(s):
    last, first = run(s)
    return last - first


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (5)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (3156)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (4)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1610)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
