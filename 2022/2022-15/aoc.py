#!/usr/bin/env python3

import functools as ft
import re

from more_itertools import chunked, sliding_window
from typing import NamedTuple


ExampleInput1 = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""


def allints(s):
    return [int(_) for _ in re.findall(r"-?\d+", s)]


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    @ft.cache
    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

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


def parse(s):
    points = []
    for L in s.splitlines():
        points.append([Point(a, b) for a, b in chunked(allints(L), 2)])
    return points


def compact(ranges):
    ranges.sort()
    after = []
    cur = list(ranges[0])
    for r in ranges[1:]:
        if cur[1] + 1 >= r[0]:
            cur[1] = max(cur[1], r[1])
        else:
            after.append(tuple(cur))
            cur = list(r)
    after.append(tuple(cur))

    return after


def row_ranges(equipment, row):
    ranges = []

    for s, b in equipment:
        d = s.manhattan(b)
        d -= abs(s.y - row)

        if d >= 0:
            r = (s.x - d, s.x + d)
            ranges.append(r)

    ranges = compact(ranges)

    return ranges


def part1(s, row):
    equipment = parse(s)
    ranges = row_ranges(equipment, row)

    total = sum(b + 1 - a for a, b in ranges)
    bcount = len({y for _, (_, y) in equipment if y == row})

    return total - bcount


def part2(s, maxcoord):
    equipment = parse(s)
    for y in range(maxcoord):
        ranges = row_ranges(equipment, y)
        if len(ranges) == 2:
            return 4000000 * (ranges[0][1] + 1) + y
    assert False


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (26)")
    print(part1(ExampleInput1, 10))

    print()
    print("Part 1 (4961647)")
    print(part1(real_input(), 2000000))

    print()
    print("Example Part 2 (56000011)")
    print(part2(ExampleInput1, 20))

    print()
    print("Part 2 (12274327017867)")
    print(part2(real_input(), 4000000))


if __name__ == "__main__":
    run_all()
