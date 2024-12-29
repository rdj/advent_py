#!/usr/bin/env pypy3

from collections import defaultdict
from heapq import heappush, heappop
from typing import NamedTuple


ExampleInput1 = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

ExampleGridSize = 7
ExampleStepCount = 12

RealGridSize = 71
RealStepCount = 1024

NoPath = 2 << 31

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


N = Point(0, -1)
E = Point(1, 0)
S = Point(0, 1)
W = Point(-1, 0)

DIRS = [N, E, S, W]
class Grid:
    def __init__(self, size):
        self.grid = ['.'] * (size*size)
        self.template = tuple(self.grid)
        self.height = size
        self.width = size

        self.start = Point(0, 0)
        self.end = Point(size - 1, size - 1)

    def reset(self):
        self.grid = list(self.template)

    def __getitem__(self, p):
        x, y = p
        return self.grid[y * self.width + x]

    def __setitem__(self, p, v):
        x, y = p
        self.grid[y * self.width + x] = v

    def neighbors(self, p):
        return [n for n in p.neighbors() if 0 <= n.y < self.height and 0 <= n.x < self.width]

    def find_shortest_path(self):
        best_cost_to_end = NoPath
        best_known = defaultdict(lambda: NoPath)
        visited = set()

        q = []
        heappush(q, (0, self.start))

        while q:
            cost, pos = heappop(q)
            key = pos

            if cost > best_cost_to_end:
                break

            if key in visited:
                continue
            visited.add(key)

            if pos == self.end:
                best_cost_to_end = min(cost, best_cost_to_end)
                return cost

            branches = self.neighbors(pos)
            for newpos in branches:
                newcost = cost + 1
                if self[newpos] == '#':
                    continue

                newkey = newpos
                bestcost = best_known[newkey]
                if newcost > bestcost:
                    continue

                if newcost < bestcost:
                    best_known[newkey] = newcost
                    if newkey not in visited:
                        heappush(q, (newcost, newpos))

        return best_cost_to_end


def parse(s):
    return [tuple(map(int, _.split(','))) for _ in s.splitlines()]


def part1(s, size, steps):
    g = Grid(size)
    badspots = parse(s)

    for x, y in badspots[:steps]:
        g[(x, y)] = '#'

    return g.find_shortest_path()


def part2(s, size):
    g = Grid(size)
    badspots = parse(s)

    # Note this bisect/binary search finds the boundary where the condition
    # changes. After the loop `lower` is the last succeeding index and `upper`
    # is the first failing index. It does not handle the case where there is no
    # boundary; it will hallucinate the boundary at 0/1 (if all True) or
    # len-2/len-1 (if all False).
    lower = 0
    upper = len(badspots) - 1
    while upper - lower > 1:
        n = (upper - lower) // 2 + lower
        for x, y in badspots[:n+1]:
            g[(x, y)] = '#'
        if g.find_shortest_path() == NoPath:
            upper = n
        else:
            lower = n
        g.reset()
    return badspots[upper]


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (22)")
    print(part1(ExampleInput1, ExampleGridSize, ExampleStepCount))

    print()
    print("Part 1 (286)")
    print(part1(real_input(), RealGridSize, RealStepCount))

    print()
    print("Example Part 2 (6,1)")
    print(part2(ExampleInput1, ExampleGridSize))

    print()
    print("Part 2 (20,64)")
    print(part2(real_input(), RealGridSize))


if __name__ == "__main__":
    run_all()
