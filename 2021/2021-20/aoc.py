#!/usr/bin/env python3

import re

from bitstring import Bits
from typing import NamedTuple


ExampleInput1 = """\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""


NEIGHBORHOOD = (
  (-1, -1), (0, -1), (1, -1),
  (-1,  0), (0,  0), (1,  0),
  (-1,  1), (0,  1), (1,  1),
)


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        x, y = other
        return Point(self.x + x, self.y + y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def neighborhood(self):
        return [self + d for d in NEIGHBORHOOD]


class ImageEnhancer:
    def __init__(self, alg, img):
        self.alg = alg
        self.img = img

        xmin = xmax = ymin = ymax = 0
        for p in img:
            xmin = min(xmin, p.x)
            xmax = max(xmin, p.x)
            ymin = min(ymin, p.y)
            ymax = max(ymax, p.y)

        self.min = Point(xmin - 1, ymin - 1)
        self.max = Point(xmax + 1, ymax + 1)

        self.expansions = 0


    def expand(self):
        offmap = self.infinite_expanse()
        self.expansions += 1

        self.min += (-1, -1)
        self.max += (1, 1)

        if offmap == "1":
            newimg = set(self.img)
            for x in (self.min.x, self.min.x + 1, self.max.x, self.max.x - 1):
                for y in range(self.min.y, self.max.y+1):
                    newimg.add((x, y))
            for y in (self.min.y, self.min.y + 1, self.max.y, self.max.y - 1):
                for x in range(self.min.x, self.max.x+1):
                    newimg.add((x, y))
            self.img = frozenset(newimg)


    def infinite_expanse(self):
        # Infinite expanse always starts dark
        if self.expansions == 0:
            return "0"
        # And if dark blocks stay dark, as in the example, no problem
        if not self.alg[0]:
            return "0"
        # If light blocks stay light, then they flip on when first expanding
        # and then stay that way
        if self.alg[-1]:
            return "1"
        # But in the real input the infinite expanse toggles
        return str(self.expansions % 2)


    def enhance(self):
        offmap = self.infinite_expanse()
        self.expand()
        newimg = set()

        for y in range(self.min.y, self.max.y+1):
            for x in range(self.min.x, self.max.x+1):
                here = Point(x, y)
                bits = []
                for p in here.neighborhood():
                    if not self.in_range(p):
                        bits.append(offmap)
                    elif p in self.img:
                        bits.append("1")
                    else:
                        bits.append("0")
                index = int("".join(bits), 2)
                if self.alg[index]:
                    newimg.add(here)

        self.img = frozenset(newimg)


    def pixelcount(self):
        return len(self.img)


    def in_range(self, p):
        return self.min.x <= p.x <= self.max.x and self.min.y <= p.y <= self.max.y


    def __repr__(self):
        dump = []
        for y in range(self.min.y, self.max.y+1):
            for x in range(self.min.x, self.max.x+1):
                if (x, y) in self.img:
                    dump.append("#")
                else:
                    dump.append(".")
            dump.append("\n")
        return "".join(dump)


def parse(s):
    alg, img = s.split("\n\n")
    alg = re.sub("\n", "", alg)
    alg = alg.translate(str.maketrans(".#", "01"))
    alg = Bits(bin=alg)

    onpx = set()
    for r, row in enumerate(img.splitlines()):
        for c, px in enumerate(row):
            if px == '#':
                onpx.add(Point(c, r))

    return ImageEnhancer(alg, frozenset(onpx))


def part1(s):
    e = parse(s)

    for _ in range(2):
        e.enhance()

    return e.pixelcount()


def part2(s):
    e = parse(s)

    for _ in range(50):
        e.enhance()

    return e.pixelcount()


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (35)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (5275)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (3351)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (16482)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
