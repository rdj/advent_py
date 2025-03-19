#!/usr/bin/env pypy3

import numpy as np


ExampleInput1 = """\
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""

def parse(s):
    prog = []
    for line in s.splitlines():
        op, *toks = line.split()
        match op:
            case "rect":
                prog.append((op, *map(int, toks[0].split("x"))))

            case "rotate":
                prog.append((toks[0], int(toks[1].split("=")[1]), int(toks[-1])))

    return prog


def run(prog, dim):
    arr = np.zeros(dim, int)
    for op, a, b in prog:
        match op:
            case "rect":
                arr[slice(b), slice(a)] = 1

            case "row":
                arr[a] = np.roll(arr[a], b)

            case "column":
                arr[slice(None), a] = np.roll(arr[slice(None), a], b)
    return arr


def part1(s, dim=(6, 50)):
    prog = parse(s)
    arr = run(prog, dim)
    return arr.sum()


def part2(s):
    out = []
    for row in run(parse(s), (6, 50)):
        for n in row:
            if n == 1:
                out.append("▮")
            else:
                out.append(" ")
        out.append("\n")
    return "".join(out)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1")
    print(part1(ExampleInput1, (3, 7)))

    print()
    print("Part 1 (119)")
    print(part1(real_input()))

    print()
    print("Part 2 (ZFHFSFOGPO)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
