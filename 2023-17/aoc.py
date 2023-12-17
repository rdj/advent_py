#!/usr/bin/env python3

from heapq import heappush, heappop
from typing import NamedTuple

PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'

ExampleInput1 = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

import functools as ft

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
        return [self + d for d in DIRECTIONS]

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


UP = Point(0, -1)
RIGHT = Point(1, 0)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)

DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

NEXT_DIRS = {
    UP: (UP, RIGHT, LEFT),
    DOWN: (DOWN, RIGHT, LEFT),
    RIGHT: (RIGHT, UP, DOWN),
    LEFT: (LEFT, UP, DOWN),
}


class Maze:
    def __init__(self, s):
        self.tiles = []
        for line in s.splitlines():
            self.tiles.append([int(_) for _ in line])
        assert(len(self.tiles) == len(self.tiles[0]))
        self.size = len(self.tiles)

    def in_bounds(self, p):
        return (0 <= p.x < self.size and
                0 <= p.y < self.size)

    def neighbors(self, p):
        return [n for n in p.neighbors() if self.in_bounds(n)]

    def find_best_path(self):
        start = Point(0, 0)
        goal = Point(self.size - 1, self.size - 1)

        best_known = {}#defaultdict(lambda: math.inf)
        best_known[(start, DOWN, 0)] = 0
        best_known[(start, RIGHT, 0)] = 0

        visited = set()

        q = []
        heappush(q, (0, 0, [start], DOWN, 0, []))
        heappush(q, (0, 0, [start], RIGHT, 0, []))

        # Heuristic cost for A-star is a best case _underestimate_ of the
        # remaining distance to goal. For 99% of grid-based pathfinding, this
        # is just going to be the manhattan distance.
        def h(p):
            return goal.manhattan(p)

        while q:
            _, cost, path, facing, steps, moves = heappop(q)
            pos = path[-1]

            if (pos, facing, steps) in visited:
                continue
            visited.add((pos, facing, steps))

            if pos == goal:
                # self.dump(path, moves)
                # print(cost)
                # print(sum(self.tiles[p.y][p.x] for p in path[1:]))
                # print(moves)
                return cost

            dirs = NEXT_DIRS[facing]
            for d in dirs:
                if steps == 3 and d == facing:
                    continue

                n = pos + d
                if not self.in_bounds(n):
                    continue

                newpath = path + [n]
                newcost = cost + self.tiles[n.y][n.x]
                newsteps = 1
                if d == facing:
                    newsteps = steps + 1
                key = (n, d, newsteps)
                if key in visited:
                    continue
                if key not in best_known or newcost < best_known[key]:
                    best_known[key] = cost
                    heappush(q, (newcost + h(n), newcost, newpath, d, newsteps, moves + [d]))

        raise Exception("goal not reached")

    def dump(self, path, moves):
        move_into = dict(zip(path[1:], moves))
        for y in range(self.size):
            for x in range(self.size):
                p = Point(x, y)
                if p in move_into:
                    print(RED, end='')
                    match move_into[p]:
                        case Point(1, 0):
                            print('>', end='')
                        case Point(-1, 0):
                            print('<', end='')
                        case Point(0, 1):
                            print('v', end='')
                        case Point(0, -1):
                            print('^', end='')
                    print(RESET, end='')
                else:
                    print(self.tiles[y][x], end='')
            print()


def part1(s):
    maze = Maze(s)
    return maze.find_best_path()


def part2(s):
    return "TODO"


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1")
    print(part1(ExampleInput1))

    print()
    print("Part 1")
    import cProfile
    cProfile.run('print(part1(real_input()))')

    print()
    print("Example Part 2")
    print(part2(ExampleInput1))

    print()
    print("Part 2")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
