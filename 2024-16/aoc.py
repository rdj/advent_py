#!/usr/bin/env python3

from heapq import heappush, heappop
from typing import NamedTuple

ExampleInput1 = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

ExampleInput2 = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
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

DIRS = [N, E, S, W]

def rot90(d):
    if d.x == 0:
        return (E, W)
    if d.y == 0:
        return (N, S)

class Grid:
    def __init__(self, s):
        self.grid = s.splitlines()
        self.height = len(self.grid)
        self.width = len(self.grid[0])

        self.start = None
        self.end = None
        for y in range(self.height):
            try:
                x = self.grid[y].index('S')
                self.start = Point(x, y)
            except ValueError:
                pass
            try:
                x = self.grid[y].index('E')
                self.end = Point(x, y)
            except ValueError:
                pass
            if self.start != None and self.end != None:
                break
        if self.start == None or self.end == None:
            raise Exception("Did not find start")

    def points(self):
        return [Point(x, y) for x in range(self.width) for y in range(self.height)]

    def __getitem__(self, p):
        return self.grid[p.y][p.x]

    def find_best_paths(self):
        return self.find_best(True)

    def find_best_path(self):
        return self.find_best(False)[0][0]


    def find_best(self, allpaths):
        best_known = {}
        best_known[(self.start, E)] = 0

        visited = set()

        q = []
        heappush(q, (0, self.start, E, (self.start,)))

        best_paths = []

        while q:
            cost, pos, facing, path = heappop(q)
            key = (pos, facing)

            if len(best_paths) > 0:
                if cost > best_paths[0][0]:
                    break

            if not allpaths:
                if key in visited:
                    continue
                visited.add(key)

            if pos == self.end:
                best_paths.append((cost, path))
                best_paths.sort()
                continue

            left, right = rot90(facing)
            branches = (
                (cost + 1, pos + facing, facing, path + (pos + facing,)),
                (cost + 1000, pos, left, path),
                (cost + 1000, pos, right, path),
            )
            for b in branches:
                newcost, newpos, newfacing, newpath = b
                newkey = (newpos, newfacing)
                if self[newpos] == '#':
                    continue
                if not allpaths:
                    if newkey in visited:
                        continue
                should_pursue = newkey not in best_known or newcost < best_known[newkey]
                if allpaths:
                    should_pursue = newkey not in best_known or newcost <= best_known[newkey]
                if should_pursue:
                    best_known[newkey] = newcost
                    heappush(q, b)

        best_cost = min(cost for cost, *_ in best_paths)
        return [_ for _ in best_paths if _[0] == best_cost]


def part1(s):
    g = Grid(s)
    return g.find_best_path()


def part2(s):
    g = Grid(s)
    best = g.find_best_paths()
    covered = set()
    for _, path in best:
        covered.update(path)
    return len(covered)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example 1 Part 1 (7036)")
    print(part1(ExampleInput1))

    print()
    print("Example 2 Part 1 (11048)")
    print(part1(ExampleInput2))

    print()
    print("Part 1 (98416)")
    print(part1(real_input()))

    print()
    print("Example 1 Part 2 (45)")
    print(part2(ExampleInput1))

    print()
    print("Example 2 Part 2 (64)")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (471)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
