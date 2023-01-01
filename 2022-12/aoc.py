#!/usr/bin/env python3

from collections import deque
from typing import NamedTuple

ExampleInput1 = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""


class Point(NamedTuple):
    x: int
    y: int

    def neighbors(self):
        return (self + d for d in DIRECTIONS)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


DIRECTIONS = (
    Point(1, 0),  # East
    Point(0, 1),  # South
    Point(-1, 0),  # West
    Point(0, -1),  # North
)


class Maze:

    def __init__(self, rows, start, end):
        self.rows = rows
        self.start = start
        self.end = end

    def in_bounds(self, p):
        return (0 <= p.x < len(self.rows[0]) and 0 <= p.y < len(self.rows))

    def shortest_path_length(self, reverse=False):
        if reverse:
            start = self.end
            def endfn(p): return self.rows[p.y][p.x] == "a"
            def moveokfn(hfrom, hto): return hfrom <= hto + 1
        else:
            start = self.start
            def endfn(p): return p == self.end
            def moveokfn(hfrom, hto): return hto <= hfrom + 1

        visited = set()
        q = deque()
        q.append((0, start))

        while len(q) > 0:
            cost, pos = q.popleft()
            if pos in visited:
                continue
            visited.add(pos)

            if endfn(pos):
                return cost

            ph = self.rows[pos.y][pos.x]

            for n in pos.neighbors():
                if not self.in_bounds(n) or n in visited:
                    continue

                nh = self.rows[n.y][n.x]
                if not moveokfn(ord(ph), ord(nh)):
                    continue

                q.append((cost + 1, n))


def parse(s):
    start, end = None, None
    rows = []
    for y, s in enumerate(s.splitlines()):
        if start is None and (x := s.find("S")) != -1:
            start = Point(x, y)
            s = s.replace("S", "a")
        if end is None and (x := s.find("E")) != -1:
            end = Point(x, y)
            s = s.replace("E", "z")
        rows.append(s)
    assert start is not None, "Found no start tile"
    assert end is not None, "Found no end tile"
    return Maze(rows, start, end)


def part1(s):
    maze = parse(s)
    return maze.shortest_path_length()


def part2(s):
    maze = parse(s)
    return maze.shortest_path_length(reverse=True)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (31)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (497)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (29)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (492)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
