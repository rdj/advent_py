#!/usr/bin/env python3

import re
from collections import defaultdict
from more_itertools import batched


ExampleInput1 = """\
p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>
"""

ExampleInput2 = """\
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
"""


def parse(s):
    results = []
    for line in s.splitlines():
        nums = map(int, re.sub("[^0-9-]", " ", line).split())
        results.append(list(map(list, batched(nums, n=3))))
    return results


# I just manually binary searched for the t value where part 1 stablized
BigT = 152


def part1(s):
    results = []

    for i, (p, v, a) in enumerate(parse(s)):
        m = 0
        for j in range(3):
            m += abs(a[j]*BigT**2 + v[j]*BigT + p[j])
        results.append((m, i))

    return sorted(results)[0][1]


# Ok, so I tried doing this with math, both with z3 and sympy and it's just too
# slow. So I guess they want us to simulate it. I guess I will see what BigT
# value gives a stable result for part1 and then try that many ticks of
# simulation for part2. Kinda hate it though.
def part2(s):
    parts = parse(s)
    eliminated = [False] * len(parts)

    for t in range(BigT):
        locs = defaultdict(list)

        for i, (p, v, a) in enumerate(parts):
            if eliminated[i]:
                continue

            for j in range(3):
                v[j] += a[j]
                p[j] += v[j]
            locs[tuple(p)] += [i]

        for li in locs.values():
            if len(li) > 1:
                for i in li:
                    eliminated[i] = True

    return len(eliminated) - sum(eliminated)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (0)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (376)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (1)")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (574)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
