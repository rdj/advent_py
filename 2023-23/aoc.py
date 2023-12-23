#!/usr/bin/env python3

from colors import color
from heapq import heappush, heappop
import itertools as it
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

    def build_graph(self):
        partials = [[self.start]]
        segments = []
        nodes = set()
        nodes.add(self.goal)

        while partials:
            path = partials.pop()
            pos = path[-1]

            if pos in nodes:
                segments.append(path)
                continue

            neighbors = [n for n in pos.neighbors() if self.tiles[n.y][n.x] != '#' and n not in path]
            match len(neighbors):
                case 0:
                    print(f"{pos=}")
                    print(f"{path=}")
                    print(f"{segments=}")
                    print(f"{visited=}")
                    raise Exception(f"dead end")
                case 1:
                    path.append(neighbors[0])
                    partials.append(path)
                case _:
                    nodes.add(pos)
                    segments.append(path)
                    for n in neighbors:
                        partials.append([pos, n])

        nodes.add(self.start)
        return nodes, segments

    def build_edges(self):
        nodes, segments = self.build_graph()

        edges = {n: {} for n in nodes}
        for s in segments:
            a, b = s[0], s[-1]
            cost = len(s) - 1
            edges[a][b] = cost
            edges[b][a] = cost
        return edges


    def find_best_path2(self):
        edges = self.build_edges()
        partials = [[self.start]]
        completes = []

        while partials:
            path = partials.pop()
            pos = path[-1]

            if pos == self.goal:
                completes.append(path)
                continue

            neighbors = edges[pos].keys()
            for n in neighbors:
                if n in path:
                    continue
                partials.append(path + [n])

        costs = []
        for s in completes:
            cost = 0
            for a, b in it.pairwise(s):
                cost += edges[a][b]
            costs.append(cost)

        costs.sort()
        return costs[-1]



def part1(s):
    maze = Maze(s)
    path = maze.find_best_path()
    # for y in range(maze.height):
    #     for x in range(maze.width):
    #         if Point(x, y) in path:
    #             print(color('O', '#ff0000'), end='')
    #         else:
    #             print(maze.tiles[y][x], end='')
    #     print()
    return len(path) - 1


def part2(s):
    maze = Maze(s)
    return maze.find_best_path2()


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (94)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (2318)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (154)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (6426)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()

