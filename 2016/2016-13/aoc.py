#!/usr/bin/env python3

from heapq import heappush, heappop


ExampleInput1 = """\
10
"""


def parse(s):
    return int(s.strip())


# Caching this is actually slower
def is_wall(n, p):
    x, y = p
    if x < 0 or y < 0:
        return True
    return ((x*x + 3*x + 2*x*y + y + y*y + n).bit_count() % 2) != 0


def shortest_path_len(n, goal):
    visited = set()

    max_explore = 2 << 31 - 1
    if goal is None:
        max_explore = 50

    q = []
    heappush(q, (0, (1, 1)))

    while q:
        cost, pos = heappop(q)

        if pos in visited:
            continue
        visited.add(pos)

        if pos == goal:
            return cost

        for dx, dy in ((0, 1), (0, -1), (-1, 0), (1, 0)):
            npos = (pos[0] + dx, pos[1] + dy)
            ncost = cost + 1

            if ncost > max_explore:
                continue

            if is_wall(n, npos):
                continue
            if npos in visited:
                continue
            heappush(q, (ncost, npos))

    assert(goal is None)
    return len(visited)


def part1(s, goal=(31, 39)):
    return shortest_path_len(parse(s), goal)


def part2(s):
    return shortest_path_len(parse(s), goal=None)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (11)")
    print(part1(ExampleInput1, (7, 4)))

    print()
    print("Part 1 (90)")
    print(part1(real_input()))

    print()
    print("Part 2 (135)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
