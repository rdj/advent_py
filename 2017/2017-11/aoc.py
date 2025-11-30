#!/usr/bin/env python3


ExamplesPart1 = (
    ("ne,ne,ne", 3),
    ("ne,ne,sw,sw", 0),
    ("ne,ne,s,s", 2),
    ("se,sw,se,sw,sw", 3),
)


# https://www.redblobgames.com/grids/hexagons/
# Axial coordinates.
# Like cubic (q, r, s) but no need to store s because s = -q-r
DIRECTIONS = {
    #      dq  dr
    'n':  ( 0, -1),
    'ne': (+1, -1),
    'se': (+1,  0),
    's' : ( 0, +1),
    'sw': (-1, +1),
    'nw': (-1,  0),
}


def go(p, d):
    dq, dr = DIRECTIONS[d]
    p[0] += dq
    p[1] += dr


# Hex manhattan is half the cubic manhattan
def manhattan(a, b=(0,0)):
    q0, r0 = a
    q1, r1 = b
    dq = q1 - q0
    dr = r1 - r0
    ds = -dq - dr
    return (abs(dq) + abs(dr) + abs(ds))//2


def parse(s):
    return s.strip().split(",")


def part1(s):
    dirs = parse(s)
    p = [0, 0]
    for d in dirs:
        go(p, d)
    return manhattan(p)


def part2(s):
    dirs = parse(s)
    far = 0
    p = [0, 0]
    for d in dirs:
        go(p, d)
        far = max(far, manhattan(p))
    return far



def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (s, x) in enumerate(ExamplesPart1):
        print(f"Example Part 1.{i} ({x})")
        print(part1(s))
        print()

    print("Part 1 (818)")
    print(part1(real_input()))
    print()

    print("Part 2 (1596)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
