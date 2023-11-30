#!/usr/bin/env python3

import re

from more_itertools import chunked, sliding_window
from typing import NamedTuple


ExampleInput1 = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""


def allints(s):
    return [int(_) for _ in re.findall(r"\d+", s)]


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def _n(x):
        return abs(x)/x if x else 0

    # INCLUSIVE
    def range(self, other):
        u = (other - self).unit()
        p = self
        while True:
            yield p
            if p == other:
                break
            p = p + u

    def unit(self):
        return Point(*map(Point._n, self))


class Cave:
    START = Point(500, 0)
    STEPS = (
        Point(0, 1),
        Point(-1, 1),
        Point(1, 1),
    )

    def __init__(self, initial):
        self.state = initial
        self.maxy = max((p.y for p in self.state))

    def simulate(self, floor=False):
        x = 0
        while self.simulate_one(floor):
            x += 1
        return x

    def simulate_one(self, floor=False):
        p = Cave.START
        if p in self.state:
            return False
        while p.y < self.maxy + 1:
            for s in Cave.STEPS:
                n = p + s
                if n not in self.state:
                    p = n
                    break
            else:
                self.state[p] = "o"
                return True
        if floor:
            self.state[p] = "o"
            return True
        return False


def parse(s):
    cave = {}

    for L in s.splitlines():
        pts = [Point(a, b) for a, b in chunked(allints(L), 2)]
        for a, b in sliding_window(pts, 2):
            for p in a.range(b):
                cave[p] = "#"

    return Cave(cave)


def part1(s):
    cave = parse(s)
    return cave.simulate()


def part2(s):
    cave = parse(s)
    return cave.simulate(floor=True)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (24)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (779)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (93)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (27426)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
