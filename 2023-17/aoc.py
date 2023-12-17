#!/usr/bin/env python3

from heapq import heappush, heappop
from typing import NamedTuple

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

ExampleInput2 = """\
111111111111
999999999991
999999999991
999999999991
999999999991
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
        self.height = len(self.tiles)
        self.width = len(self.tiles[0])

    def in_bounds(self, p):
        return (0 <= p.x < self.width and
                0 <= p.y < self.height)

    def find_best_path(self, can_change_dir=0, must_change_dir=3):
        start = Point(0, 0)
        goal = Point(self.width - 1, self.height - 1)

        best_known = {}
        best_known[(start, DOWN, 0)] = 0
        best_known[(start, RIGHT, 0)] = 0

        visited = set()

        q = []
        heappush(q, (0, 0, start, DOWN, 0))
        heappush(q, (0, 0, start, RIGHT, 0))

        # Heuristic cost for A-star is a best case _underestimate_ of the
        # remaining distance to goal. For 99% of grid-based pathfinding, this
        # is just going to be the manhattan distance. Leaving this comment
        # because I *always* forget this and think this should be an upper
        # rather than lower bound of the remaining cost.
        def h(p):
            return goal.manhattan(p)

        while q:
            _, cost, pos, facing, steps = heappop(q)
            key = (pos, facing, steps)

            if key in visited:
                continue
            visited.add(key)

            if pos == goal:
                if steps < can_change_dir:
                    continue
                return cost

            dirs = NEXT_DIRS[facing]
            for d in dirs:
                if steps < can_change_dir and d != facing:
                    continue
                if steps == must_change_dir and d == facing:
                    continue

                n = pos + d
                if not self.in_bounds(n):
                    continue

                newcost = cost + self.tiles[n.y][n.x]
                newsteps = 1
                if d == facing:
                    newsteps = steps + 1
                newkey = (n, d, newsteps)
                if newkey in visited:
                    continue
                if newkey not in best_known or newcost < best_known[newkey]:
                    best_known[key] = cost
                    heappush(q, (newcost + h(n), newcost, n, d, newsteps))

        raise Exception("goal not reached")


def part1(s):
    maze = Maze(s)
    return maze.find_best_path()


def part2(s):
    maze = Maze(s)
    return maze.find_best_path(4, 10)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (102)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (1039)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (94)")
    print(part2(ExampleInput1))

    print()
    print("Example Part 2 (71)")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (1201)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
