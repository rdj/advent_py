#!/usr/bin/env python3

from colors import color
from typing import NamedTuple


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


def do_part1(s, target_steps=64):
    maze = s.splitlines()
    src = set()
    h, w = len(maze), len(maze[0])

    for y in range(h):
        for x in range(w):
            if maze[y][x] == 'S':
                src.add(Point(x,y))
                break

    for _ in range(target_steps):
        dst = set()
        for p in src:
            for n in p.neighbors():
                if not (0 <= n.y < h and
                        0 <= n.x < w):
                    continue
                if maze[n.y][n.x] != '#':
                    dst.add(n)
        src = dst

    return len(src)


def part1(s):
    return do_part1(s)


def part2(s):
    return "TODO"


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (16)")
    print(do_part1(ExampleInput1, 6))

    print()
    print("Part 1 (3572)")
    print(part1(real_input()))

    print()
    print("Example Part 2")
    print(part2(ExampleInput1))

    print()
    print("Part 2")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
