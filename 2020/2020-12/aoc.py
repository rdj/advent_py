#!/usr/bin/env pypy3

from typing import NamedTuple


ExampleInput1 = """\
F10
N3
F7
R90
F11
"""


def absdiff(a, b):
    if a > b:
        return a - b
    return b - a


class Point(NamedTuple):
    x:int
    y:int

    def __add__(self, other):
        x0, y0 = self
        x1, y1 = other
        return Point(x0 + x1, y0 + y1)

    def __mul__(self, scalar):
        return Point(scalar * self.x, scalar * self.y)

    def __rmul__(self, scalar):
        return Point(scalar * self.x, scalar * self.y)

    def manhattan(self, other):
        x0, y0 = self
        x1, y1 = other
        return absdiff(x0, x1) + absdiff(y0, y1)


NORTH = Point(0, 1)
EAST  = Point(1, 0)
SOUTH = Point(0, -1)
WEST  = Point(-1, 0)

DIRS = (NORTH, EAST, SOUTH, WEST)

DIRNAMES = { "N": NORTH, "E": EAST, "S": SOUTH, "W": WEST }


def parse(s):
    return tuple((line[0], int(line[1:])) for line in s.splitlines())


def rot(d, deg):
    x, y = d
    for _ in range(deg % 360 // 90):
        x, y = y, -x
    return Point(x, y)


def part1(s):
    pos = Point(0, 0)
    face = EAST

    for c, n in parse(s):
        match c:
            case 'F':
                pos += n * face

            case 'R':
                face = rot(face, n)

            case 'L':
                face = rot(face, -n)

            case d if d in DIRNAMES:
                pos += n * DIRNAMES[d]

    return pos.manhattan((0, 0))


def part2(s):
    pos = Point(0, 0)
    vec = Point(10, 1)

    for c, n in parse(s):
        match c:
            case 'F':
                pos += n * vec

            case 'R':
                vec = rot(vec, n)

            case 'L':
                vec = rot(vec, -n)

            case d if d in DIRNAMES:
                vec += n * DIRNAMES[d]

    return pos.manhattan((0, 0))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (25)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (636)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (286)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (26841)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
