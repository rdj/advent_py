#!/usr/bin/env pypy3

from itertools import product

ExampleInput1 = """\
ULL
RRDDD
LURDL
UUUUD
"""


def findcode(s, keypad):
    padlen = len(keypad[0]) + 2
    keys = []
    keys += [[None] * padlen]
    for k in keypad:
        keys += [[None] + k + [None]]
    keys += [[None] * padlen]

    for y, x in product(range(len(keys)), range(len(keys[0]))):
        if str(keys[y][x]) == "5":
            break

    code = ""
    for line in s.splitlines():
        for d in line:
            match d:
                case "L":
                    if keys[y][x-1] != None:
                        x -= 1

                case "R":
                    if keys[y][x+1] != None:
                        x += 1

                case "U":
                    if keys[y-1][x] != None:
                        y -= 1

                case "D":
                    if keys[y+1][x] != None:
                        y += 1

        code += str(keys[y][x])

    return code


def part1(s):
    keypad = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    return findcode(s, keypad)


def part2(s):
    keypad = [
        [None, None,   1, None, None],
        [None,    2,   3,    4, None],
        [   5,    6,   7,    8,    9],
        [None,  "A", "B",  "C", None],
        [None, None, "D", None, None]
    ]
    return findcode(s, keypad)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (1985)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (76792)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (5DB3)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (A7AC3)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
