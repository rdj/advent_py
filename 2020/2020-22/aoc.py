#!/usr/bin/env python3


from math import prod


ExampleInput1 = """\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""

ExampleInput2 = """\
Player 1:
43
19

Player 2:
2
29
14
"""


def parse(s):
    return [list(map(int, b.splitlines()[1:])) for b in s.split("\n\n")]


def score(d):
    return sum(map(prod, enumerate(reversed(d), start=1)))


def game(p0, p1, recursive):
    seen = set()

    while p0 and p1:
        state = (tuple(p0), tuple(p1))
        if state in seen:
            return 0, score(p0)
        seen.add(state)

        a, p0 = p0[0], p0[1:]
        b, p1 = p1[0], p1[1:]

        if recursive and len(p0) >= a and len(p1) >= b:
            pwin, _ = game(p0[:a], p1[:b], True)
        else:
            pwin = int(b > a)

        if pwin == 0:
            p0 += [a, b]
        else:
            p1 += [b, a]

    if p0:
        return 0, score(p0)
    else:
        return 1, score(p1)


def part1(s):
    return game(*parse(s), False)[1]


def part2(s):
    return game(*parse(s), True)[1]


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (306)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (34127)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (291)")
    print(part2(ExampleInput1))

    print()
    print("Example 2 Part 2 (105)")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (32054)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
