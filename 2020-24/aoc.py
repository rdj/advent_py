#!/usr/bin/env pypy3

## Things I used in previous years

# from colors import color  ## pip install py-colors
# from collections import Counter
# from collections import defaultdict
# from collections import deque
# from colors import color
# from enum import Enum
# from fractions import Fraction
# from functools import cached_property
# from functools import lru_cache
# from functools import reduce
# from functools import reduce, partial
# from heapq import heappush, heappop
# from itertools import pairwise
# from math import prod
# from more_itertools import chunked, sliding_window
# from multiprocessing import Pool
# from numpy import transpose
# from operator import mul
# from pathlib import Path
# from typing import NamedTuple
# import cProfile
# import functools as ft
# import itertools as it
# import math
# import networkx as nx
# import operator as op
# import pygraphviz as pgv
# import re
# import sympy


ExampleInput1 = """\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
"""


import re

from collections import Counter, defaultdict
from typing import NamedTuple


class HexPoint(NamedTuple):
    q: int
    r: int
    s: int

    def __add__(self, other):
        q0, r0, s0 = self
        q1, r1, s1 = other
        return HexPoint(q0+q1, r0+r1, s0+s1)

    def __repr__(self):
        q, r, s = self
        return f"({q}, {r}, {s})"

    def neighbors(self):
        return [self + d for d in DIRECTIONS.values()]


# https://www.redblobgames.com/grids/hexagons/
DIRECTIONS = {
    'nw': ( 0, -1, +1),
    'ne': (+1, -1,  0),
    'e':  (+1,  0, -1),
    'se': ( 0, +1, -1),
    'sw': (-1, +1,  0),
    'w':  (-1,  0, +1),
}

WHITE = False
BLACK = True

def parse(s):
    points = defaultdict(bool)

    for line in s.splitlines():
        line = re.sub(r"(e|w|nw|ne|sw|se)", r"\1 ", line)

        p = HexPoint(0, 0, 0)
        for d in line.split():
            p += DIRECTIONS[d]
        points[p] = not points[p]

    return points


def part1(s):
    return sum(parse(s).values())


def part2(s):
    tiles = parse(s)

    for day in range(100):
        ncount = defaultdict(int)
        for t, isblack in tiles.items():
            if not isblack:
                continue
            for n in t.neighbors():
                ncount[n] += 1

        newtiles = defaultdict(bool)
        for t, n in ncount.items():
            isblack = tiles[t]
            if isblack and (n == 0 or n > 2):
                newtiles[t] = WHITE
            elif not isblack and n == 2:
                newtiles[t] = BLACK
            else:
                newtiles[t] = isblack

        tiles = newtiles

    return sum(tiles.values())


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (10)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (322)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (2208)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (3831)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
