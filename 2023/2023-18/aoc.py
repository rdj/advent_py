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

# The instructions draw a Simple Polygon:
#   https://en.wikipedia.org/wiki/Simple_polygon
#
# We can calculate the area with Shoelace:
#   https://en.wikipedia.org/wiki/Shoelace_formula
#
# But just using shoelace is going to undercount the lava squares, which are
# supposed to include the trench as well as the interior. Think about a simple
# square case:
#  ......
#  .#####.  R 4   Vertices: (0, 0) (4, 0) (4, 4) (0, 4)
#  .#####.  D 4   Shoelace: 16
#  .#####.  L 4   Lava Squares: 25
#  .#####.  U 4
#  .#####.
#  .......
#
# So it looks like about half of the exterior points get left out, because the
# point "x, y" is just the lower left corner of that square of area in normal
# cartesian coordinates, and we're working with weird integer-sized squares.
#
# Originally, I just intuitively added on half the perimeter, and that was off
# by one, so I slapped +1 on there, got the solutions and moved on.
#
# But it was bugging me, so I went back and read more of the Wikipedia page for
# Simple Polygon. Right there next to Shoelace it talks about Pick's Theorem:
#   https://en.wikipedia.org/wiki/Pick%27s_theoremformula
#
# Pick's theorem, which only works for integer coorindates (hint hint), defines
# a relationship between the area, interior integer points, and exterior
# integer points, usually expressed in terms of the Area:
#   area = interior_points + boundary_points / 2 - 1
#
# We know the area and can count the boundary_points, so we can solve for the
# interior points, and our puzzle solution is the sum of the interior and
# boundary points.
#  interior_points = area - boundary_points / 2 + 1
#
# Incidentally, one extra step yields my original formula for the solution:
#  interior_points + boundary_points = area + boundary_points / 2 + 1
#
def compute_lava_squares(offsets):
    vertices = offsets_to_points(offsets)
    area = shoelace(vertices)
    boundary_points = perimeter(offsets)
    interior_points = area - boundary_points // 2 + 1
    return boundary_points + interior_points

def part1(s):
    return compute_lava_squares(decode1(s))


def part2(s):
    return compute_lava_squares(decode2(s))


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
