#!/usr/bin/env python3

from typing import NamedTuple

ExampleInput1 = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

CAVE_WIDTH = 7
MARGIN_LEFT = 2
MARGIN_BOTTOM = 3
CYCLE_PEEK = 20


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


LEFT = Point(-1, 0)
RIGHT = Point(1, 0)
DOWN = Point(0, -1)


class Shape:
    def __init__(self, offsets):
        self.offsets = tuple(Point(*p) for p in offsets)

    def at(self, p):
        return [o + p for o in self.offsets]


SHAPES = tuple(Shape(offsets) for offsets in (
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


class Cave:
    def __init__(self):
        self.state = set()
        self.height = 0

    def __repr__(self):
        return self.top(self.height)

    def _legal_pt(self, p):
        return (
            0 <= p.x < CAVE_WIDTH
            and 0 <= p.y
            and p not in self.state
        )

    def is_legal_placement(self, shape, point):
        return all(self._legal_pt(p) for p in shape.at(point))

    def place(self, shape, point):
        for p in shape.at(point):
            self.height = max(self.height, p.y + 1)
            self.state.add(p)

    def top(self, maxlines):
        s = []

        start = self.height - 1
        thru = max(-1, start - maxlines)

        for y in range(start, thru, -1):
            if len(s):
                s.append("\n")
            for x in range(CAVE_WIDTH):
                if Point(x, y) in self.state:
                    s.append("#")
                else:
                    s.append(".")
        return "".join(s)


class Cycle(NamedTuple):
    length: int
    shape_base: int
    height_base: int
    height_delta: int

    def _cycle_index(self, n):
        return (n - self.shape_base) % self.length

    def equivalent(self, n, m):
        return self._cycle_index(n) == self._cycle_index(m)

    def height_at(self, r):
        cycle_count = (r - self.shape_base) // self.length
        return self.height_base + cycle_count * self.height_delta


def simulate(moves, wanted):
    cave = Cave()

    cycle = None
    seen = {}

    mi = 0

    for r in range(wanted):
        si = r % len(SHAPES)

        if cycle is None:
            key = (si, mi, cave.top(CYCLE_PEEK))
            if key in seen:
                r0, h0 = seen[key]
                cycle = Cycle(
                    length=r-r0,
                    shape_base=r0,
                    height_base=h0,
                    height_delta=cave.height - h0,
                )
            else:
                seen[key] = (r, cave.height)
        elif cycle.equivalent(r, wanted):
            extra = cave.height - cycle.height_at(r)
            return cycle.height_at(wanted) + extra

        s = SHAPES[si]
        p = Point(MARGIN_LEFT, cave.height + MARGIN_BOTTOM)

        while True:
            m = moves[mi]
            mi = (mi + 1) % len(moves)

            match m:
                case "<":
                    n = p + LEFT
                case ">":
                    n = p + RIGHT
                case _:
                    assert False
            if cave.is_legal_placement(s, n):
                p = n

            n = p + DOWN
            if cave.is_legal_placement(s, n):
                p = n
            else:
                cave.place(s, p)
                break

    return cave.height


def part1(s):
    return simulate(s.strip(), 2022)


def part2(s):
    return simulate(s.strip(), 1_000_000_000_000)


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
    print("Example Part 2 (1514285714288)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1504093567249)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
