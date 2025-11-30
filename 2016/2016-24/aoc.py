#!/usr/bin/env python3

import re
from collections import deque


ExampleInput1 = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""


def parse(s):
    maze = s.splitlines()
    start = None
    need = 0

    for y, line in enumerate(maze):
        need += len(re.findall(r"\d", line))
        try:
            x = line.index("0")
            start = (x, y)
        except ValueError:
            pass

    return maze, start, need


def find_shortest_path_len(maze, start, need, backToStart=False):
    q = deque()
    q.append((0, ((0,), start)))

    visited = set()

    goal = need
    if backToStart:
        goal += 1

    while q:
        steps, key = q.popleft()

        if key in visited:
            continue
        visited.add(key)

        inv, (x, y) = key

        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            x1, y1 = x + dx, y + dy
            t = maze[y1][x1]
            if t == "#":
                continue
            ni = inv
            if t.isdigit():
                d = int(t)
                if d not in ni:
                    ni = tuple(sorted(ni + (d,)))
                if backToStart and d == 0 and len(ni) == need:
                    ni = tuple(ni + (0,))
                if len(ni) == goal:
                    return steps + 1

            nk = (ni, (x1, y1))
            q.append((steps + 1, nk))

    return "NO SOLUTION FOUND"


def part1(s):
    return find_shortest_path_len(*parse(s))


def part2(s):
    return find_shortest_path_len(*parse(s), backToStart=True)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (14)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (490)")
    print(part1(real_input()))

    print()
    print("Part 2 (744)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
