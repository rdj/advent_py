#!/usr/bin/env python3

from math import prod


ExampleInput1 = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

def parse(s):
    ic = []
    for line in s.splitlines():
        ps, vs = line.split()
        p0 = tuple(map(int, ps.split('=')[1].split(',')))
        v0 = tuple(map(int, vs.split('=')[1].split(',')))
        ic.append((p0, v0))
    return ic


def quadcounts(ic, w=101, h=103, tmax=100, printquads=False):
    quads = [0] * 4
    for (x0, y0), (vx, vy) in ic:
        f = ((x0 + vx * tmax) % w, (y0 + vy * tmax) % h)
        q = 0
        if f[0] == w//2 or f[1] == h//2 :
            continue
        if f[0] > w//2:
            q |= 1
        if f[1] > h//2:
            q |= 2
        quads[q] += 1

    if printquads:
        print(quads)
    return quads


def part1(s, w=101, h=103):
    return prod(quadcounts(parse(s), w, h))


def part2(s, w=101, h=103):
    ic = parse(s)
    nrobots = len(ic)
    majority = nrobots // 2
    for tmax in range(10_000):
        quads = quadcounts(ic, w, h, tmax)
        if any(q > majority for q in quads):
            return tmax
    raise Exception("No solution")


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (12)")
    print(part1(ExampleInput1, 11, 7))

    print()
    print("Part 1 (214400550)")
    print(part1(real_input()))

    print()
    print("Part 2 (8149)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
