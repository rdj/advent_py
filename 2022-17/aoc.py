#!/usr/bin/env python3

from typing import NamedTuple

ExampleInput1 = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

CAVE_WIDTH = 7
MARGIN_LEFT = 2
MARGIN_BOTTOM = 3


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


class Shape:
    def __init__(self, offsets):
        self.offsets = tuple(Point(*p) for p in offsets)
        self.height = max(y for (_, y) in offsets) + 1
        self.width = max(x for (x, _) in offsets) + 1

    def __repr__(self):
        s = []
        for y in range(self.height - 1, -1, -1):
            if len(s):
                s.append("\n")
            for x in range(self.width):
                if Point(x, y) in self.offsets:
                    s.append("#")
                else:
                    s.append(".")
        return "".join(s)

    def at(self, p):
        return [o + p for o in self.offsets]


SHAPES = tuple(Shape(_) for _ in (
    #   @@@@
    ((0, 0), (1, 0), (2, 0), (3, 0)),

    #   .@.
    #   @@@
    #   .@.
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),

    #   ..@
    #   ..@
    #   @@@
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),

    #   @
    #   @
    #   @
    #   @
    ((0, 0), (0, 1), (0, 2), (0, 3)),

    #   @@
    #   @@
    ((0, 0), (1, 0), (0, 1), (1, 1)),
))

LEFT = Point(-1, 0)
RIGHT = Point(1, 0)
DOWN = Point(0, -1)


class Cave:
    def __init__(self):
        self.state = set()
        self.height = 0

    def __repr__(self):
        s = []
        for y in range(self.height - 1, -1, -1):
            if len(s):
                s.append("\n")
            for x in range(CAVE_WIDTH):
                if Point(x, y) in self.state:
                    s.append("#")
                else:
                    s.append(".")
        return "".join(s)

    def _legal_pt(self, p):
        return (
            0 <= p.x < CAVE_WIDTH
            and 0 <= p.y
            and p not in self.state
        )

    def is_legal_placement(self, shape, point):
        points = shape.at(point)
        if any(not self._legal_pt(p) for p in points):
            return None
        return points

    def place(self, shape, point):
        for p in shape.at(point):
            self.height = max(self.height, p.y + 1)
            self.state.add(p)


def simulate(moves, wanted):
    cave = Cave()
    cursor = 0

    for r in range(wanted):
        s = SHAPES[r % len(SHAPES)]
        p = Point(MARGIN_LEFT, cave.height + MARGIN_BOTTOM)

        while True:
            delta = None
            m = moves[cursor % len(moves)]
            cursor += 1
            match m:
                case "<":
                    delta = LEFT
                case ">":
                    delta = RIGHT
                case _:
                    raise Exception(f"Unknown move: {m}")

            n = p + delta
            if cave.is_legal_placement(s, n):
                p = n

            delta = DOWN
            n = p + delta
            if cave.is_legal_placement(s, n):
                p = n
            else:
                cave.place(s, p)
                break
    return cave.height


def part1(s):
    return simulate(s.strip(), 2022)


def part2(s):
    return "TODO"
    # return simulate(s.strip(), 1_000_000_000_000)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (3068)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (3048)")
    print(part1(real_input()))

    print()
    print("Example Part 2")
    print(part2(ExampleInput1))

    print()
    print("Part 2")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
