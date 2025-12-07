#!/usr/bin/env python3

from functools import cache

MultiLineExample = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

ExamplesPart1 = (
    (MultiLineExample, 21),
)

ExamplesPart2 = (
    (MultiLineExample, 40),
)


def parse(s):
    start = None
    splitters = []

    lines = s.splitlines()
    h = len(lines)
    w = len(lines[0])

    for y in range(h):
        for x in range(w):
            match lines[y][x]:
                case '^':
                    splitters.append((x, y))
                case 'S':
                    start = (x, y)

    return start, set(splitters)


def part1(s):
    start, splitters = parse(s)
    visited = set()

    maxy = max(map(lambda p: p[1], splitters))

    q = [start]
    while q:
        p = q.pop()
        if p in visited:
            continue
        visited.add(p)

        x, y = p
        if p in splitters:
            q.append((x-1, y))
            q.append((x+1, y))
        elif y + 1 <= maxy:
            q.append((x, y+1))

    return len(visited & splitters)


def part2(s):
    start, splitters = parse(s)
    maxy = max(map(lambda p: p[1], splitters))

    @cache
    def paths_from(p):
        x, y = p
        if y > maxy:
            return 1

        if p in splitters:
            return paths_from((x-1, y)) + paths_from((x+1, y))

        return paths_from((x, y+1))

    return paths_from(start)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    import time
    for i, (a, b) in enumerate(ExamplesPart1):
        c = part1(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 (1566)")
    before = time.perf_counter_ns()
    result = part1(real_input())
    elapsed = time.perf_counter_ns() - before
    print(f"{result} ({elapsed//1_000_000} ms)")
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (5921061943075)")
    before = time.perf_counter_ns()
    result = part2(real_input())
    elapsed = time.perf_counter_ns() - before
    print(f"{result} ({elapsed//1_000_000} ms)")


if __name__ == "__main__":
    run_all()
