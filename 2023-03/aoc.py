#!/usr/bin/env python3

import re

from collections import defaultdict
from functools import cached_property
from typing import NamedTuple

ExampleInput1 = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".strip()


class Point(NamedTuple):
    x: int
    y: int

    def neighbors_manhattan(self):
        return (self + d for d in DIRECTIONS_MANHATTAN)

    def neighbors_all(self):
        return (self + d for d in DIRECTIONS_MANHATTAN + DIRECTIONS_DIAGONAL)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


NORTH = Point(0, -1)
EAST = Point(1, 0)
SOUTH = Point(0, 1)
WEST = Point(-1, 0)

DIRECTIONS_MANHATTAN = (
    NORTH, EAST, SOUTH, WEST
)

DIRECTIONS_DIAGONAL = (
    NORTH + EAST, SOUTH + EAST, SOUTH + WEST, NORTH + WEST
)


class Entry:
    location: Point
    value: str

    def __init__(self, location, value):
        self.location = location
        self.value = value

    def __repr__(self):
        return f"Entry('{self.value}' @ ({self.location.x}, {self.location.y}))"

    def contains(self, p):
        return p in self.coverage

    @cached_property
    def coverage(self):
        return [self.location + Point(n, 0) for n in range(len(self.value))]

    def is_point_adjacent(self, p):
        return p in self.neighbors

    @cached_property
    def neighbors(self):
        return set(n for p in self.coverage for n in p.neighbors_all())


def parse(s):
    grid = s.strip().splitlines()
    entries = []
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == '.':
                continue
            if entries and entries[-1].contains(Point(c, r)):
                continue

            value = grid[r][c]
            if value.isdigit():
                value = re.match(r'\d+', grid[r][c:])[0]
            entries.append(Entry(Point(c, r), value))
    return entries


def part1(s):
    entries = parse(s)

    numbers = [e for e in entries if e.value.isnumeric()]
    symbols = [e for e in entries if not e.value.isnumeric()]

    matched = [n for n in numbers if any(n.is_point_adjacent(s.location) for s in symbols)]

    return sum(int(e.value) for e in matched)


def part2(s):
    entries = parse(s)

    numbers = [e for e in entries if e.value.isnumeric()]
    gears = [e for e in entries if e.value == '*']

    result = 0
    for g in gears:
        matches = [n for n in numbers if n.is_point_adjacent(g.location)]
        if len(matches) > 2:
            raise Exception(f"Too many numbers touch gear {g}")
        if len(matches) == 2:
            result += int(matches[0].value) * int(matches[1].value)

    return result


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read().strip()


def run_all():
    print("Example Part 1 (4361)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (521515)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (467835)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (69527306)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
