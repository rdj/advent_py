#!/usr/bin/env pypy3

from collections import defaultdict
from more_itertools import sliding_window
from typing import NamedTuple


ExampleInput1 = """\
AAAA
BBCD
BBCC
EEEC
"""

ExampleInput2 = """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

ExampleInput3 = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

ExampleInput4 = """\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""

ExampleInput5 = """\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""

class Point(NamedTuple):
  x: int
  y: int

  def __add__(self, other):
      return Point(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
      return Point(self.x - other.x, self.y - other.y)

  def __repr__(self):
      return f"({self.x}, {self.y})"

  def neighbors(self):
      return [self + d for d in DIRS]


N = Point(0, -1)
E = Point(1, 0)
S = Point(0, 1)
W = Point(-1, 0)

DIRS = [N, E, S, W]

class Grid:
    def __init__(self, s):
        self.grid = s.splitlines()
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def points(self):
        return [Point(x, y) for x in range(self.width) for y in range(self.height)]

    def in_range(self, p):
        return 0 <= p.x < self.width and 0 <= p.y < self.height

    def neighbors(self, p):
        return [n for n in p.neighbors() if self.in_range(n)]

    def __getitem__(self, p):
        return self.grid[p.y][p.x]

    def populate_region(self, r, p):
        if p in r:
            return

        r.add(p)
        for n in self.neighbors(p):
            if self[p] == self[n]:
                self.populate_region(r, n)

    def discover_regions(self):
        regions = []
        seen = set()

        for p in self.points():
            if p in seen:
                continue
            r = set()
            self.populate_region(r, p)
            regions.append(r)
            seen |= r

        return regions

    def perimeter(self, r):
        return sum([len([n for n in p.neighbors() if n not in r]) for p in r])

    def sides(self, r):
        fences = {d: defaultdict(list) for d in DIRS}

        for p in r:
            for n in p.neighbors():
                if n in r:
                    continue

                d = p - n
                if d.x == 0:
                    fences[d][n.y].append(n.x)
                else:
                    fences[d][n.x].append(n.y)

        return sum(count_ranges(fence) for fence in fences.values())

def count_ranges(fence):
    t = 0
    for _, nums in fence.items():
        nums = sorted(nums)
        t += 1
        for a, b in sliding_window(nums, 2):
            if b - a > 1:
                t += 1
    return t

def part1(s):
    g = Grid(s)
    regions = g.discover_regions()
    return sum([len(r) * g.perimeter(r) for r in regions])


def part2(s):
    g = Grid(s)
    regions = g.discover_regions()
    return sum([len(r) * g.sides(r) for r in regions])


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example 1 Part 1 (140)")
    print(part1(ExampleInput1))

    print()
    print("Example 2 Part 1 (772)")
    print(part1(ExampleInput2))

    print()
    print("Example 3 Part 1 (1930)")
    print(part1(ExampleInput3))

    print()
    print("Part 1 (1434856)")
    print(part1(real_input()))

    print()
    print("Example 2 ABCD Part 2 (80)")
    print(part2(ExampleInput1))

    print()
    print("Example 2 XO Part 2 (436)")
    print(part2(ExampleInput2))

    print()
    print("Example 4 EX Part 2 (236)")
    print(part2(ExampleInput4))

    print()
    print("Example 5 ABBA Part 2 (368)")
    print(part2(ExampleInput5))

    print()
    print("Example 3 Large Part 2 (1206)")
    print(part2(ExampleInput3))

    print()
    print("Part 2 (891106)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
