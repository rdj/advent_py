#!/usr/bin/env python3

import numpy as np
from scipy.signal import convolve2d


MultiLineExample = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""

ExamplesPart1 = (
    (MultiLineExample, 4),
)

ExamplesPart2 = (
    (MultiLineExample, 17),
)


def parse(s):
    return np.array([[int(c == "#") for c in line] for line in s.splitlines()], dtype=int)


def part1(s, steps=100, cornersStuck=False):
    a = parse(s)
    if cornersStuck:
        w, h = a.shape
        a[0][0] = a[0][w-1] = a[h-1][0] = a[h-1][w-1] = 1

    # I misread the rules and it turns out this isn't great for 2d convolusion,
    # but I wanted to try using it
    kernel = np.ones((3, 3), dtype=int)
    kernel[1][1] = 0

    for i in range(steps):
        n = convolve2d(a, kernel, mode="same")
        for i in range(len(a)):
            for j in range(len(a[0])):
                if a[i][j]:
                    a[i][j] = int(2 <= n[i][j] <= 3)
                else:
                    a[i][j] = int(n[i][j] == 3)
        if cornersStuck:
            a[0][0] = a[0][w-1] = a[h-1][0] = a[h-1][w-1] = 1

    return a.sum()


def part2(s, steps=100):
    return part1(s, steps, True)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1):
        c = part1(a, 4)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 (814)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a, 5)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (924)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
