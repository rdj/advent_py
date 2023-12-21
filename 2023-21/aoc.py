#!/usr/bin/env python3

from colors import color
from typing import NamedTuple
import functools as ft
from collections import defaultdict


ExampleInput1 = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

ExampleRDJ = """\
.........
.#.......
......#..
.........
....S....
.........
.##......
.........
.........
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
    def __init__(self, s, infinite=False):
        self.maze = s.splitlines()
        self.infinite = infinite
        self.height = len(self.maze)
        self.width = len(self.maze[0])

    def __getitem__(self, key):
        return self.maze[key]

    def find_start(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 'S':
                    return Point(x, y)


    @ft.cache
    def neighbors(self, p):
        nlist = []
        for n in p.neighbors():
            if not (0 <= n.x < self.width and 0 <= n.y < self.height):
                if not self.infinite:
                    continue
            if self.maze[n.y % self.height][n.x % self.width] == '#':
                continue
            nlist.append(n)
        return tuple(nlist)


def count_destinations(s_or_maze, target_steps=64, start=None):
    maze = s_or_maze
    if not isinstance(maze, Maze):
        maze = Maze(maze)
    if not start:
        start = maze.find_start()
    src = set([start])

    for _ in range(target_steps):
        dst = set()
        for p in src:
            for n in maze.neighbors(p):
                dst.add(n)
        src = dst

    return len(src)


def part1(s, step_count=64, infinite=False):
    maze = Maze(s, infinite)
    return count_destinations(maze, step_count)


def part2(s, step_count=26501365):
    maze = Maze(s)

    start = maze.find_start()
    size = maze.height

    expensive_asserts = True

    # the maze is square, has an odd size, and the start is in the exact middle
    assert start.x == start.y
    assert maze.find_start().x * 2 + 1 == maze.height == maze.width

    # there is a border of unobstructed stuff all the way around
    # not in the example, but in the real input, the center row/col are also clear
    for y in range(size):
        assert maze[y][0] != '#'
        assert maze[y][size -1] != '#'
        assert maze[y][start.x] != '#'
    for x in range(size):
        assert maze[0][x] != '#'
        assert maze[size -1][x] != '#'
        assert maze[start.y][x] != '#'

    # once enough steps have run, the maze reaches a steady state where it flip
    # flops between two counts
    big_enough = 130
    big_enough_center = big_enough
    center_even = count_destinations(maze, big_enough)
    center_odd = count_destinations(maze, big_enough + 1)
    if expensive_asserts:
        assert center_even == count_destinations(maze, big_enough + 2)
        assert center_odd == count_destinations(maze, big_enough + 3)

    # if you start in the middle of the edge, you reach the same steady state,
    # but with the parity reversed (it takes longer)
    big_enough = 196
    big_enough_edge = big_enough
    edge_even = count_destinations(maze, big_enough, Point(0, start.y))
    edge_odd = count_destinations(maze, big_enough + 1, Point(0, start.y))
    if expensive_asserts:
        assert sorted((center_even, center_odd)) == sorted((edge_even, edge_odd))
        assert edge_even == count_destinations(maze, big_enough, Point(size - 1, start.y))
        assert edge_even == count_destinations(maze, big_enough, Point(start.x, 0))
        assert edge_even == count_destinations(maze, big_enough, Point(start.x, size - 1))
        assert edge_odd == count_destinations(maze, big_enough + 1, Point(size - 1, start.y))
        assert edge_odd == count_destinations(maze, big_enough + 1, Point(start.x, 0))
        assert edge_odd == count_destinations(maze, big_enough + 1, Point(start.x, size - 1))

    # starting on a corner yields the same steady state, same parity as central
    # square (it takes even longer)
    big_enough = 260
    big_enough_corner = big_enough
    corner_even = count_destinations(maze, big_enough, Point(0, 0))
    corner_odd = count_destinations(maze, big_enough + 1, Point(0, 0))
    if expensive_asserts:
        assert sorted((center_even, center_odd)) == sorted((corner_even, corner_odd))
        assert corner_even == count_destinations(maze, big_enough, Point(0, size - 1))
        assert corner_odd == count_destinations(maze, big_enough + 1, Point(0, size - 1))
        assert corner_even == count_destinations(maze, big_enough, Point(size - 1, 0))
        assert corner_odd == count_destinations(maze, big_enough + 1, Point(size - 1, 0))
        assert corner_even == count_destinations(maze, big_enough, Point(size - 1, size - 1))
        assert corner_odd == count_destinations(maze, big_enough + 1, Point(size - 1, size - 1))

    # it will take (size / 2 + 1) steps to get to the edge of the center maze
    # then there will be center + 4 edge mazes
    # after it will take (size + 1) more steps to cross and reach new mazes
    # then there will be uh
    # NOTE: I'm a little worried about crosstalk between adjacent mazes (?)

    # ok graph paper for a bit, with size = 5, we access mazes at these steps (upper right quadrant):
    #
    # 23 26 31 36 41 46
    # 18 21 26 31 36 41
    # 13 16 21 26 31 36
    # 08 11 16 21 26 31
    # 03 06 11 16 21 26
    # 00 03 08 13 18 23
    #
    # center start: 1
    # edge-start:   4 * ((n + 2) // 5) if n > 2
    # corner-start: 4 * x * (x + 1) / 2 where x = (n - 1) // 5 if n > 5  (4 * sum of first x integers)

    centers = 1
    center_result = None
    if step_count < big_enough_center:
        center_result = count_destinations(maze, step_count)
    else:
        center_result = center_odd if step_count % 2 else center_even

    edges = 0
    edges_result = 0
    d_first_edge = (size - 1) // 2
    if step_count > d_first_edge:
        edges, edge_age  = divmod((step_count + d_first_edge), size)
        edges *= 4
        print(f"{edges=} {edge_age=}")

        while edges > 0 and edge_age < big_enough_edge:
            for s in ((Point(start.x, 0), Point(start.x, size - 1), Point(0, start.y), Point(size - 1, start.y))):
                edges_result += count_destinations(maze, edge_age, s)
            edges -= 4
            edge_age += size

        if edges > 0:
            print(f"Edge interiors {edges=} {edge_odd=} {edge_even=} {step_count=}")
        edges_result += edges * (edge_odd if edge_age % 2 else edge_even)

    corners = 0
    corners_result = 0
    if step_count > size:
        diagonal_length, corner_age = divmod((step_count - 1), size)
        corners = diagonal_length * (diagonal_length + 1) // 2
        corners *= 4
        print(f"{corners=} {diagonal_length=} {corner_age=}")

        while corners > 0 and corner_age < big_enough_corner:
            for s in (Point(0, 0), Point(0, size - 1), Point(size - 1, 0), Point(size - 1, size - 1)):
                corners_result += diagonal_length * count_destinations(maze, corner_age, s)
            corners -= diagonal_length * 4
            diagonal_length -= 1
            corner_age += size

        if corners > 0:
            print(f"Corner interiors {corners=} {corner_odd=} {corner_even=} {step_count=}")
        corners_result += corners * (corner_odd if corner_age % 2 else corner_even)


    result = center_result + edges_result + corners_result

    print(result, "=", center_result, "(center) +", edges_result, "(edges) +", corners_result, "(corners)")

    # 590782959877036 is too low
    # 590800516088076 is wrong
    # 1181589207387618 is too high
    return result


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (16)")
    print(count_destinations(ExampleInput1, 6))

    print()
    print("Part 1 (3572)")
    print(part1(real_input()))

    # Example is terrible because it has the centerline blocked
    # print()
    # print("Example Part 2")
    # for a, b in ((6, 16), (10, 50), (50, 1594), (100, 6536), (500, 167004), (1000, 668697), (5000, 16733044)):
    #     print(f"{a} -> {b}")
    #     print(part2(ExampleInput1, a))

    for n in range(208, 211):
        comp = part2(ExampleRDJ, n)
        sim = part1(ExampleRDJ, n, True)
        fg = None
        if comp != sim:
            fg = 'red'
        print(color(f"RDJ {n} : Computed {comp} Simulated {sim}", fg))

    # print()
    # print("Part 2")
    # print(part2(real_input()))


if __name__ == "__main__":
    run_all()
