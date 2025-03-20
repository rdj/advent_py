#!/usr/bin/env pypy3

import numpy as np


ExamplesPart1 = (
    ("turn on 0,0 through 999,999", 1_000_000),
    ("toggle 0,0 through 999,0", 1000),
    ("turn off 499,499 through 500,500", 0),
)

ExamplesPart2 = (
    ("turn on 0,0 through 0,0", 1),
    ("toggle 0,0 through 999,999", 2_000_000),
)


def parse(s):
    prog = []
    for line in s.splitlines():
        toks = line.split()
        op, toks = toks[0], toks[1:]
        if op == "turn":
            op, toks = toks[0], toks[1:]
        prog.append((op, tuple(int(_) for _ in toks[0].split(",")), tuple(int(_) for _ in toks[-1].split(","))))
    return prog


def part1(s):
    prog = parse(s)
    a = np.zeros((1000, 1000), dtype=bool)
    for (op, (i0, j0), (i1, j1)) in prog:
        ir = slice(i0, i1+1)
        jr = slice(j0, j1+1)
        match op:
            case "on":
                a[ir,jr] = True
            case "off":
                a[ir,jr] = False
            case "toggle":
                a[ir,jr] = np.logical_not(a[ir,jr])

    return a.sum()


def part2(s):
    prog = parse(s)
    a = np.zeros((1000, 1000), dtype=int)
    for (op, (i0, j0), (i1, j1)) in prog:
        ir = slice(i0, i1+1)
        jr = slice(j0, j1+1)
        match op:
            case "on":
                a[ir,jr] = np.add(a[ir,jr], 1)
            case "off":
                a[ir,jr] = np.maximum(np.add(a[ir,jr], -1), 0)
            case "toggle":
                a[ir,jr] = np.add(a[ir,jr], 2)

    return a.sum()


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

    print("Part 1 (400410)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (> 15343601)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
