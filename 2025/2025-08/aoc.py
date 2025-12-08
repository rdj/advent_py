#!/usr/bin/env python3

from collections import defaultdict
from itertools import combinations
from itertools import islice
from math import prod

MultiLineExample = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

ExamplesPart1 = (
    (MultiLineExample, 40),
)

ExamplesPart2 = (
    (MultiLineExample, 25272),
)


def parse(s):
    return [tuple(map(int, line.split(","))) for line in s.splitlines()]


def dist(a, b):
    x0, y0, z0 = a
    x1, y1, z1 = b
    xd = x1 - x0
    yd = y1 - y0
    zd = z1 - z0
    return xd*xd + yd*yd + zd*zd # can compare without doing the root


def part1(s, stopafter=1000):
    points = parse(s)
    distances = [(dist(a, b), a, b) for a, b in combinations(points, 2)]
    distances.sort()

    nets = defaultdict(set)
    p2n = {}
    idnext = 1

    connections = 0

    for _, a, b in distances:
        dst = None
        na = p2n[a] if a in p2n else None
        nb = p2n[b] if b in p2n else None

        if na and nb:
            if na != nb:
                dst = na
                src = nets[nb]
                del nets[nb]
                nets[na] |= src
                for p in src:
                    p2n[p] = na
        else:
            dst = na or nb
            if not dst:
                dst = idnext
                idnext += 1

            nets[dst].add(a)
            nets[dst].add(b)
            p2n[a] = dst
            p2n[b] = dst

        if stopafter:
            connections += 1
            if stopafter and connections == stopafter:
                return prod(islice(reversed(sorted(map(len, nets.values()))), 0, 3))
        elif dst:
            if len(nets[dst]) == len(points):
                return a[0] * b[0]


def part2(s):
    return part1(s, 0)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    import time

    for i, (a, b) in enumerate(ExamplesPart1):
        c = part1(a, 10)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 (81536)")
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

    print("Part 2 (7017750530)")
    before = time.perf_counter_ns()
    result = part2(real_input())
    elapsed = time.perf_counter_ns() - before
    print(f"{result} ({elapsed//1_000_000} ms)")


if __name__ == "__main__":
    run_all()
