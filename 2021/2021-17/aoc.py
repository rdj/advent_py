#!/usr/bin/env python3

from itertools import count


ExampleInput1 = """\
target area: x=20..30, y=-10..-5
"""


def parse(s):
    xs, ys = s.strip().split(": ")[-1].split(", ")
    xmin, xmax = map(int, xs.split("=")[-1].split(".."))
    ymin, ymax = map(int, ys.split("=")[-1].split(".."))

    assert(0 < xmin < xmax)
    assert(ymin < ymax < 0)

    return range(xmin, xmax + 1), range(ymin, ymax + 1)


def sumrange(a, b):
    return (b - a + 1) * (a + b) // 2


def xvhits(xv, xr):
    for step in count():
        if step > xv:
            return False
        x = sumrange(max(0, xv - step), xv)
        if x in xr:
            return True
        if x >= xr.stop:
            return False


def hits(xv, yv, xr, yr):
    for step in count():
        x = sumrange(max(0, xv - step), xv)
        y = sumrange(yv - step, yv)
        if x in xr and y in yr:
            return True
        if x >= xr.stop or y < yr.start:
            return False


def allhits(s):
    xr, yr = parse(s)

    for xv in range(xr.stop):
        if xvhits(xv, xr):
            # Why -yr.start as the upper bound?
            #
            # This simulation is ideal-physicsy enough that when the projectile
            # falls back to y=0 its dy will be the same magnitude as its
            # initial dy (opposite sign). If |dy| is greater than the distance
            # to the bottom of the y target zone, it will overshoot.
            for yv in range(min(0, yr.start), -yr.start):
                if hits(xv, yv, xr, yr):
                    yield yv


def part1(s):
    return max(map(lambda yv: sumrange(min(0, yv), yv), allhits(s)))


def part2(s):
    return sum(1 for _ in allhits(s))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (45)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (4950)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (112)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1477)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
