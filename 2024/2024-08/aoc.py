#!/usr/bin/env pypy3

from collections import defaultdict
from itertools import combinations
from typing import NamedTuple


ExampleInput1 = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
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


def parse(s):
    ants = defaultdict(list)
    grid = s.splitlines()
    width, height = len(grid[0]), len(grid)
    for y in range(height):
        for x in range(width):
            match grid[y][x]:
                case '.':
                    continue
                case f:
                    ants[f].append(Point(x, y))
    return ants, lambda p: 0 <= p.x < width and 0 <= p.y < height


def count_antinodes(s, limit):
    nodes, in_bounds = parse(s)
    antis = set()

    def add_points(start, delta):
        cur = start
        for _ in range(limit):
            antis.add(cur)
            cur += delta
            if not in_bounds(cur):
                break

    for f, coords in nodes.items():
        for a, b in combinations(coords, 2):
            add_points(a, a - b)
            add_points(b, b - a)

    return len(antis)


def part1(s):
    return count_antinodes(s, 1)


def part2(s):
    return count_antinodes(s, 2**32)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (14)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (273)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (34)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1017)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
