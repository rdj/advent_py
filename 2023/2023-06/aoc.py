#!/usr/bin/env python3

import math
import re

from functools import reduce
from operator import mul


ExampleInput1 = """\
Time:      7  15   30
Distance:  9  40  200
""".strip()


def parse(s):
    lines = s.splitlines();
    times = [int(_) for _ in lines[0].split()[1:]]
    distances = [int(_) for _ in lines[1].split()[1:]]
    return list(zip(times, distances))

def part1(s):
    races = parse(s)

    results = []

    for r in races:
        t, d = r
        wins = 0
        for n in range(t):
            if (t - n) * n > d:
                wins += 1
        results.append(wins)

    return reduce(mul, results, 1)


def part2(s):
    t, d = [int(re.sub(r'\s+','', line).split(':')[-1]) for line in s.splitlines()]

    # We're asked to find the values of x where
    #
    #   x * (t - x) > d
    #
    # This can be rewritten in the form of a quadratic:
    #
    #   -x**2 + t*x - d > 0
    #
    # So the bounds will be the (closest integers to) the roots of the
    # quadratic equation:
    #
    #   a*x**2 + b*x + c = 0, given a = -1, b = t, c = -d
    #
    # Which, by middle school math, can be found using the:
    #  Q U A D R A T I C
    #    F O R M U L A
    #
    # If you've forgotten Mrs. Felke's algebra class:
    #   https://en.wikipedia.org/wiki/Quadratic_formula
    #
    #   x = ( -b ± sqrt(b**2 - 4*a*c) ) / 2*a
    #

    a = -1
    b = t
    c = -d

    # First figure the determinant (the part under the radical). It, uh,
    # determines what kinds of roots the equation has. Negative determinate
    # means no real roots, which would be bad. Zero means one real root, which
    # would be real weird for this puzzle. Positive means two real roots,
    # that's what we want, then the space between them is our solution.

    det = b * b - 4 * a * c
    assert( det > 0 )

    rad = math.sqrt(det)
    r0 = ( -b + rad ) / 2*a
    r1 = ( -b - rad ) / 2*a

    # In theory you should be a little more careful about this, but we know the
    # puzzle is designed to work out, so we can just sweep some things under
    # the rug here like making sure these in fact bound the solution space
    # (rather than the non-solution space) and rounding each number towards the
    # middle.
    return math.floor(math.fabs(r0 - r1))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read().strip()


def run_all():
    print("Example Part 1 (288)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (281600)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (71503)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (33875953)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
