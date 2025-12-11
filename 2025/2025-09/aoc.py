#!/usr/bin/env python3

from itertools import combinations
from more_itertools import sliding_window
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


def part1(s):
    points = parse(s)
    return max(area(a, b) for a,b in combinations(points, 2))


def part2(s):
    return part2_shapely(s)


def sorted_candidates(points):
    rects = [(-area(a, b), a, b) for a, b in combinations(points, 2)]
    rects.sort()
    return rects


def makerect_shapely(a, b):
    x1, y1 = a
    x2, y2 = b
    return box(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))


def part2_shapely(s): # runtime ~1200ms
    points = parse(s)

    poly = Polygon(points + [points[0]])

    for _, a, b in sorted_candidates(points):
        if poly.contains(makerect_shapely(a, b)):
            return area(a, b)


def makerect(a, b):
    x1, y1 = a
    x2, y2 = b
    xmin, xmax = sorted((x1, x2))
    ymin, ymax = sorted((y1, y2))

    return [
        (xmin, ymin),
        (xmax, ymin),
        (xmax, ymax),
        (xmin, ymax)
    ]


# https://math.stackexchange.com/questions/3259950/determing-if-two-line-segments-intersect-using-cross-products
# https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c
    return (cy-ay)*(bx-ax) > (by-ay)*(cx-ax)


def intersect(a, b, c, d):
    return ccw(a,c,d) != ccw(b,c,d) and ccw(a,b,c) != ccw(a,b,d)


# Insets the rectangle by 1 unit. If the inset rectangle does not cross any of
# the polygon's edges, it must lie entirely within the polygon. Note that the
# problem definition might technically allow degenerate "zero-width" rectangles
# with non-zero area. This method assumes that such a rectangle will not be the
# largest area.
def inner_intersect(a, b, points):
    tl, _, br, _ = makerect(a, b)
    inr = makerect((tl[0] + 1, tl[1] + 1), (br[0] - 1, br[1] -1))
    inr = inr + [inr[0]]
    points = points + (points[0],)

    for a, b in sliding_window(inr, 2):
        for c, d in sliding_window(points, 2):
            if intersect(a, b, c, d):
                return True

    return False


def part2_nolib(s): # runtime ~8-9 seconds
    points = tuple(parse(s))

    for _, a, b in sorted_candidates(points):
        if not inner_intersect(a, b, points):
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
