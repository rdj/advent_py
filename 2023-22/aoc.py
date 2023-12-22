#!/usr/bin/env python3

from colors import color
from typing import NamedTuple
import functools as ft


ExampleInput1 = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

def norm(x):
    return abs(x)//x if x else 0


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    # INCLUSIVE
    def range(self, other):
        u = (other - self).unit()
        p = self
        while True:
            yield p
            if p == other:
                break
            p = p + u

    def unit(self):
        return Point(norm(self.x), norm(self.y), norm(self.z))


DOWN = Point(0, 0, -1)
UP = Point(0, 0, 1)


def try_move(bricks, all_points, b):
    for p in b:
        all_points.remove(p)

    cur = b
    while all(p.z > 1 for p in cur):
        newb = [p + DOWN for p in cur]
        if any(p in all_points for p in newb):
            break
        cur = newb

    for p in cur:
        all_points.add(p)

    if cur == b:
        return False

    b.clear()
    b += cur
    return True


def try_explode(all_points, b):
    if any(p.z == 1 for p in b):
        return False

    for p in b:
        all_points.remove(p)

    below = [p + DOWN for p in b]
    explode = all(p not in all_points for p in below)

    if not explode:
        for p in b:
            all_points.add(p)
        return False

    return True


def drop_bricks(bricks, all_points):
    moved = True
    while moved:
        moved = False
        for b in bricks:
            if try_move(bricks, all_points, b):
                moved = True

def parse(s):
    bricks = []

    for i, line in enumerate(s.splitlines()):
        start, end = line.split('~')
        start = Point(*map(int, start.split(',')))
        end = Point(*map(int, end.split(',')))

        brick = [p for p in start.range(end)]
        bricks.append(brick)

    return bricks


def part1(s):
    bricks = parse(s)
    bricks.sort(key=lambda b: min(p.z for p in b))

    all_points = set(p for b in bricks for p in b)

    drop_bricks(bricks, all_points)

    all_points = {}
    for i, b in enumerate(bricks):
        for p in b:
            all_points[p] = i

    above = []
    below = []
    for i, b in enumerate(bricks):
        na = set()
        nb = set()
        for p in b:
            pup = p + UP
            if pup in all_points:
                j = all_points[pup]
                if j != i:
                    na.add(j)
            pdn = p + DOWN
            if pdn in all_points:
                j = all_points[pdn]
                if j != i:
                    nb.add(j)
        above.append(na)
        below.append(nb)

    count = 0
    for a in above:
        if len(a) == 0:
            count += 1
            continue

        if all(len(below[i]) > 1 for i in a):
            count += 1

    return count


def fallcount(bricks, all_points, b):
    bricks = bricks.copy()
    all_points = all_points.copy()

    bricks.remove(b)
    for p in b:
        all_points.remove(p)

    count = 0
    exploded = True
    while exploded:
        exploded = False
        for b in bricks:
            if try_explode(all_points, b):
                count += 1
                exploded = True
                bricks.remove(b)
                break
    return count


def part2(s):
    bricks = parse(s)
    bricks.sort(key=lambda b: min(p.z for p in b))
    all_points = set(p for b in bricks for p in b)

    drop_bricks(bricks, all_points)

    total = 0
    for i, b in enumerate(bricks):
        f = fallcount(bricks, all_points, b)
        total += f

    return total


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1")
    print(part1(ExampleInput1))

    print()
    print("Part 1")
    print(part1(real_input()))

    print()
    print("Example Part 2")
    print(part2(ExampleInput1))

    print()
    print("Part 2")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
