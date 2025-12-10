#!/usr/bin/env python3

from itertools import combinations
from shapely import Polygon
from shapely.geometry import box

MultiLineExample = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

ExamplesPart1 = (
    (MultiLineExample, 50),
)

ExamplesPart2 = (
    (MultiLineExample, 24),
)


def parse(s):
    return [tuple(map(int, line.split(","))) for line in s.splitlines()]


def absdiff(a, b):
    if a > b:
        return a - b
    return b - a


def area(a, b):
    x0, y0 = a
    x1, y1 = b

    return (1 + absdiff(x0, x1)) * (1 + absdiff(y0, y1))


def makerect(a, b):
    x1, y1 = a
    x2, y2 = b
    return box(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))


def part1(s):
    points = parse(s)
    return max(area(a, b) for a,b in combinations(points, 2))


def part2(s):
    points = parse(s)

    poly = Polygon(points + [points[0]])

    rects = [(-area(a, b), a, b) for a, b in combinations(points, 2)]
    rects.sort()

    for _, a, b in rects:
        if poly.contains(makerect(a, b)):
            return area(a, b)


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

    print("Part 1 (4745816424)")
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

    print("Part 2 (1351617690)")
    before = time.perf_counter_ns()
    result = part2(real_input())
    elapsed = time.perf_counter_ns() - before
    print(f"{result} ({elapsed//1_000_000} ms)")


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('part2(real_input())', sort="cumulative")
    run_all()
