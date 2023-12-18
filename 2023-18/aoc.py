#!/usr/bin/env python3

from typing import NamedTuple
from itertools import pairwise

PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'


ExampleInput1 = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __lt__(self, other):
        if self.y != other.y:
            return self.y < other.y
        return self.x < other.x

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def neighbors(self):
        return [self + d for d in DIRECTIONS]


UP = Point(0, -1)
RIGHT = Point(1, 0)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)

DIRECTIONS = (RIGHT, DOWN, LEFT, UP)

DIRECTIONS_BY_NAME = {
    'U': UP,
    'R': RIGHT,
    'D': DOWN,
    'L': LEFT
}

def decode1(s):
    offsets = []
    for line in s.splitlines():
        d, n, *_ = line.split()
        d = DIRECTIONS_BY_NAME[d]
        n = int(n)
        offsets.append((d, n))
    return offsets


def decode2(s):
    offsets = []
    for line in s.splitlines():
        _, _, color = line.split()
        d = DIRECTIONS[int(color[-2:-1])]
        n = int(color[2:-2], 16)
        offsets.append((d, n))
    return offsets


def offsets_to_points(offsets):
    points = [Point(0, 0)]
    for d, n in offsets:
        points.append(points[-1] + d * n)
    assert points[0] == points[-1] # Shoelace wants the first vertex repeated, conveniently
    return points


def shoelace(points):
    return sum(one.x * two.y - two.x * one.y for one, two in pairwise(points)) // 2


def perimeter(offsets):
    return sum(_[1] for _ in offsets)


def part1(s):
    offsets = decode1(s)
    points = offsets_to_points(offsets)
    return shoelace(points) + perimeter(offsets) // 2 + 1

# Ok so we created a Simple Polygon:
#   https://en.wikipedia.org/wiki/Simple_polygon
#
# So to calculate the area we need:
#   https://en.wikipedia.org/wiki/Shoelace_formula
#
# I should have guessed from all the clues in part 1 that we were going to need
# to do something like this.
#
# The formula is going to undercount because it essentially doesn't count half
# the edge, so we'll need to add that back in.
def part2(s):
    offsets = decode2(s)
    points = offsets_to_points(offsets)
    return shoelace(points) + perimeter(offsets) // 2 + 1

def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (62)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (67891)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (952408144115)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (94116351948493)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
