#!/usr/bin/env pypy3

from collections import defaultdict
from itertools import combinations


ExampleInput1 = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

def find_antennas(grid):
    ants = defaultdict(list)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            match grid[y][x]:
                case '.':
                    continue
                case f:
                    ants[f].append((x, y))
    return ants


def part1(s):
    g = s.splitlines()
    w, h = len(g[0]), len(g)
    nodes = find_antennas(g)
    antis = set()
    for f, coords in nodes.items():
        for a, b in combinations(coords, 2):
            dx = b[0] - a[0]
            dy = b[1] - a[1]
            antis.add((a[0] - dx, a[1] - dy))
            antis.add((b[0] + dx, b[1] + dy))

    return sum(1 for p in antis if 0 <= p[0] < w and 0 <= p[1] < h)


def part2(s):
    g = s.splitlines()
    w, h = len(g[0]), len(g)
    in_bounds = lambda p: 0 <= p[0] < w and 0 <= p[1] < h
    nodes = find_antennas(g)
    antis = set()
    for f, coords in nodes.items():
        for a, b in combinations(coords, 2):
            dx = b[0] - a[0]
            dy = b[1] - a[1]

            cur = a
            while True:
                antis.add(cur)
                cur = (cur[0] - dx, cur[1] - dy)
                if not in_bounds(cur):
                    break

            cur = b
            while True:
                antis.add(cur)
                cur = (cur[0] + dx, cur[1] + dy)
                if not in_bounds(cur):
                    break

    return sum(1 for _ in antis)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (14)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (273)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (34)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1017)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
