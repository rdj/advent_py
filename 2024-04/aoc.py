#!/usr/bin/env python3

from collections import defaultdict
from typing import NamedTuple


ExampleInput1 = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
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
NE = N + E
NW = N + W
SE = S + E
SW = S + W

DIRECTIONS = (N, E, S, W, NE, NW, SE, SW)

INTERCARDS = (NE, NW, SE, SW)

class Grid:
    def __init__(self, s):
        self.tiles = s.splitlines()
        self.height = len(self.tiles)
        self.width = len(self.tiles[0])

    def in_bounds(self, p):
        return (0 <= p.x < self.width and
                0 <= p.y < self.height)

    def is_xmas(self, start, direction):
        return self.is_word('XMAS', start, direction)

    def is_mas(self, start, direction):
        return self.is_word('MAS', start, direction)

    def is_word(self, word, start, direction):
        if word == '':
            return True
        if not self.in_bounds(start):
            return False
        return self.tiles[start.y][start.x] == word[0] and self.is_word(word[1:], start + direction, direction)


def part1(s):
    g = Grid(s)

    count = 0
    for y in range(g.height):
        for x in range(g.width):
            for d in DIRECTIONS:
                if g.is_xmas(Point(x, y), d):
                    count += 1
    return count


def part2(s):
    g = Grid(s)

    centers = defaultdict(list)
    for y in range(g.height):
        for x in range(g.width):
            for d in INTERCARDS:
                start = Point(x, y)
                if g.is_mas(start, d):
                    centers[start + d].append(d)

    return len([_ for _ in centers.values() if len(_) == 2])


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (18)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (2685)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (9)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (2048)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
