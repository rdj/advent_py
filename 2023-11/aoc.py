#!/usr/bin/env python3

import itertools as it

ExampleInput1 = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

class Point:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


def do_part1(s, delta=1):
    tiles = [list(_) for _ in s.splitlines()];
    h = len(tiles)
    w = len(tiles[0])

    galaxies = []
    for y in range(h):
        for x in range(w):
            if tiles[y][x] == '#':
                galaxies.append(Point(x, y))

    dy = 0
    for y in range(h):
        if all('.' == tiles[y][x] for x in range(w)):
            for g in galaxies:
                if g.y > y + dy:
                    g.y += delta
            dy += delta

    dx = 0
    for x in range(w):
        if all('.' == tiles[y][x] for y in range(h)):
            for g in galaxies:
                if g.x > x + dx:
                    g.x += delta
            dx += delta

    return sum(a.manhattan(b) for a,b in it.combinations(galaxies, 2))


def part1(s):
    return do_part1(s)


def part2(s):
    return do_part1(s, delta=1000000 - 1)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (9536038)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (x10) (1030)")
    print(do_part1(ExampleInput1, delta=9))

    print()
    print("Example Part 2 (x100) (8410)")
    print(do_part1(ExampleInput1, delta=99))

    print()
    print("Part 2 (447744640566)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
