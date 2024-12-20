#!/usr/bin/env pypy3

from collections import defaultdict
from heapq import heappush, heappop
from typing import NamedTuple


ExampleInput1 = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        x, y = other
        return Point(self.x + x, self.y + y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def neighbors(self):
        return [self + d for d in DIRS]

    def manhattan(self, other):
        x0, y0 = self
        x1, y1 = other
        return abs(x0 - x1) + abs(y0 - y1)


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

        for y in range(self.height):
            for x in range(self.width):
                match self.grid[y][x]:
                    case 'S':
                        self.start = Point(x, y)

                    case 'E':
                        self.end = Point(x, y)

    def __getitem__(self, p):
        x, y = p
        return self.grid[y][x]

    def neighbors(self, p):
        return [n for n in p.neighbors() if 0 <= n.y < self.height and 0 <= n.x < self.width]

    def find_distances(self):
        visited = set()
        best_known = defaultdict(lambda: 2 << 31)

        q = []
        heappush(q, (0, self.end))
        best_known[self.end] = 0

        while q:
            cost, pos = heappop(q)
            key = pos

            if key in visited:
                continue
            visited.add(key)

            branches = self.neighbors(pos)
            for newpos in branches:
                if self[newpos] == '#':
                    continue

                newcost = cost + 1
                newkey = newpos
                bestcost = best_known[newkey]
                if newcost > bestcost:
                    continue

                if newcost < bestcost:
                    best_known[newkey] = newcost
                    if newkey not in visited:
                        heappush(q, (newcost, newpos))

        return dict(best_known)

    def find_cheats1(self):
        cheats = 0
        dists = self.find_distances()
        for pos, cost in dists.items():
            for n in [pos + d + d for d in DIRS]:
                if n not in dists:
                    continue
                savings = cost - dists[n] - 2
                if savings > 100:
                    cheats += 1
        return cheats


    def find_cheats(self, cheatlen):
        cheats = 0
        dists = self.find_distances()
        for (x0, y0), cost in dists.items():
            for dy in range(-cheatlen, cheatlen+1):
                maxdx = cheatlen - abs(dy)
                for dx in range(-maxdx, maxdx+1):
                    x1, y1 = dest = (x0 + dx, y0 + dy)
                    if not (0 <= x1 < self.width and 0 <= y1 < self.height):
                        continue
                    if self.grid[y1][x1] == "#":
                        continue

                    destcost = dists[dest]
                    md = abs(dy) + abs(dx)
                    savings = cost - destcost - md
                    if savings >= 100:
                        cheats +=1

        return cheats

def part1(s):
    g = Grid(s)
    return g.find_cheats1()


def part2(s):
    g = Grid(s)
    return g.find_cheats(20)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Part 1 (1463)")
    print(part1(real_input()))

    print()
    print("Part 2 (985332)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
