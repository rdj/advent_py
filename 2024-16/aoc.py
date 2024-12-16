#!/usr/bin/env pypy3

from collections import defaultdict
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

    def find_best(self):
        best_cost_to_end = 2 << 31
        best_known = defaultdict(lambda: (2 << 31, set()))
        visited = set()

        q = []
        heappush(q, (0, self.start, E))

        best_paths = []

        while q:
            cost, pos, facing = heappop(q)
            key = (pos, facing)

            if cost > best_cost_to_end:
                break

            if key in visited:
                continue
            visited.add(key)

            if pos == self.end:
                best_cost_to_end = min(cost, best_cost_to_end)
                continue

            left, right = rot90(facing)
            branches = (
                (cost + 1, pos + facing, facing),
                (cost + 1000, pos, left),
                (cost + 1000, pos, right),
            )
            for b in branches:
                newcost, newpos, newfacing = b
                if self[newpos] == '#':
                    continue

                newkey = (newpos, newfacing)
                bestcost, bestprev = best_known[newkey]
                if newcost > bestcost:
                    continue

                if newcost < bestcost:
                    best_known[newkey] = (newcost, set([(pos,facing)]))
                else:
                    bestprev.add((pos, facing))
                if newkey not in visited:
                    heappush(q, b)

        return (best_cost_to_end, self.build_covered(best_cost_to_end, best_known))

    def build_covered(self, best_cost_to_end, best_known):
        covered_states = set()
        for (pos, facing), (cost, prev) in best_known.items():
            if pos == self.end and cost == best_cost_to_end:
                r_build_covered(covered_states, best_known, (pos, facing))

        covered_points = set([pos for pos, _ in covered_states])
        return covered_points

def r_build_covered(covered, best_known, src):
    covered.add(src)

    for state, (cost, prev) in best_known.items():
        if state == src:
            for state in prev:
                if state not in covered:
                    r_build_covered(covered, best_known, state)
    return covered

def part1(s):
    g = Grid(s)
    cost, covered = g.find_best()
    return cost


def part2(s):
    g = Grid(s)
    cost, covered = g.find_best()
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
