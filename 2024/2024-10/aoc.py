#!/usr/bin/env python3

from typing import NamedTuple
from functools import cache


ExampleInput1 = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
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


class TrailMap:
    def __init__(self, s):
        h = []
        lines = s.splitlines()
        fake_line = [-1] * (len(lines[0]) + 2)
        h.append(fake_line)
        for line in lines:
            h.append([-1] + [int(_) for _ in line] + [-1])
        h.append(fake_line)

        self.alts = h
        self.height = len(self.alts)
        self.width = len(self.alts[0])

    def points(self):
        return (Point(x, y) for x in range(self.width) for y in range(self.height))

    def __getitem__(self, p):
        return self.alts[p.y][p.x]

    def get_total_score(self):
        return sum(self.get_score(p) for p in self.points() if self[p] == 0)

    def get_score(self, p):
        return len(self.get_reachable_nines(p))

    @cache
    def get_reachable_nines(self, p):
        h = self[p]
        if h == -1:
            return set()
        if h == 9:
            return set([p])

        reachable = set()
        for n in p.neighbors():
            if self[n] == h + 1:
                reachable |= self.get_reachable_nines(n)
        return reachable

    def get_total_rating(self):
        return sum(self.get_rating(p) for p in self.points() if self[p] == 0)

    @cache
    def get_rating(self, p):
        h = self[p]
        if h == -1:
            return 0
        if h == 9:
            return 1

        return sum(self.get_rating(n) for n in p.neighbors() if self[n] == h + 1)


def part1(s):
    return TrailMap(s).get_total_score()


def part2(s):
    return TrailMap(s).get_total_rating()


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (36)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (482)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (81)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1094)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
