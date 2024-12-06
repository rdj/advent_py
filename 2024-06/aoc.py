#!/usr/bin/env python3

from typing import NamedTuple


ExampleInput1 = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
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


N = Point(0, -1)
E = Point(1, 0)
S = Point(0, 1)
W = Point(-1, 0)

DIRECTIONS = [N, E, S, W]
FACING = ['^', '>', 'v', '<']


class Grid:
    def __init__(self, s):
        self.tiles = [list(_) for _ in s.splitlines()]
        self.height = len(self.tiles)
        self.width = len(self.tiles[0])

    def in_bounds(self, p):
        return (0 <= p.x < self.width and
                0 <= p.y < self.height)

    def points(self):
        return (Point(x, y) for x in range(self.width) for y in range(self.height))

    def find_start(self):
        for p in self.points():
            t = self.tiles[p.y][p.x]
            if t in FACING:
                return p, FACING.index(t)
        raise Exception()

    def find_path(self):
        start, facing = self.find_start()

        p = start
        d = DIRECTIONS[facing]
        visited = set()
        while True:
            visited.add((p, d))
            dst = p + d
            if not self.in_bounds(dst):
                break
            if (dst, d) in visited:
                return None
            t = self.tiles[dst.y][dst.x]
            if t == '#':
                d = turn90(d)
                continue
            p = dst

        return visited


def turn90(d):
    return DIRECTIONS[(DIRECTIONS.index(d) + 1) % len(DIRECTIONS)]


def part1(s):
    g = Grid(s)
    path = g.find_path()
    return len(set(_[0] for _ in path))


def part2(s):
    g = Grid(s)

    path = g.find_path()
    uniqs = set(_[0] for _ in path)

    loops = 0
    for p in uniqs:
        if g.tiles[p.y][p.x] == '.':
            g.tiles[p.y][p.x] = '#'
            if g.find_path() == None:
                loops += 1
            g.tiles[p.y][p.x] = '.'

    return loops


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (41)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (5212)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (6)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1767)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
