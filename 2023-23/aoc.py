#!/usr/bin/env python3

from colors import color
from heapq import heappush, heappop
from typing import NamedTuple

ExampleInput1 = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
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

    def neighbors(self):
        return (self + d for d in DIRECTIONS.values())

DIRECTIONS = {
    '>': Point(1, 0),  # East
    'v': Point(0, 1),  # South
    '<': Point(-1, 0),  # West
    '^': Point(0, -1),  # North
}

class Maze:
    def __init__(self, s):
        self.tiles = s.splitlines()
        self.height = len(self.tiles)
        self.width = len(self.tiles[0])
        for x in range(self.width):
            if self.tiles[0][x] == '.':
                self.start = Point(x, 0)
            if self.tiles[-1][x] == '.':
                self.goal = Point(x, self.height - 1)

    def in_bounds(self, p):
        return (0 <= p.x < self.width and
                0 <= p.y < self.height)

    def find_best_path(self):
        partials = [[self.start]]
        completes = []

        while partials:
            path = partials.pop()
            pos = path[-1]

            if pos == self.goal:
                completes.append(path)
                continue

            neighbors = []
            d = DIRECTIONS.get(self.tiles[pos.y][pos.x])
            if d:
                neighbors = [pos + d]
            else:
                neighbors = pos.neighbors()

            for n in neighbors:
                if (self.tiles[n.y][n.x] == '#' or
                    n in path):
                    continue
                partials.append(path + [n])

        completes.sort(key=lambda p: len(p))
        return completes[-1]


def part1(s):
    maze = Maze(s)
    path = maze.find_best_path()
    for y in range(maze.height):
        for x in range(maze.width):
            if Point(x, y) in path:
                print(color('O', '#ff0000'), end='')
            else:
                print(maze.tiles[y][x], end='')
        print()
    return len(path) - 1


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
    print(part1(real_input()))

    print()
    print("Example Part 2")
    print(part2(ExampleInput1))

    print()
    print("Part 2")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
