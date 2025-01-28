#!/usr/bin/env pypy3


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

from collections import defaultdict


def go(p, d):
    dq, dr = DIRECTIONS[d]
    p[0] += dq
    p[1] += dr


def neighbors(p):
    for dq, dr in DIRECTIONS.values():
        yield (p[0] + dq, p[1] + dr)


# https://www.redblobgames.com/grids/hexagons/
DIRECTIONS = {
    'nw': ( 0, -1),
    'ne': (+1, -1),
    'e':  (+1,  0),
    'se': ( 0, +1),
    'sw': (-1, +1),
    'w':  (-1,  0),
}

WHITE = False
BLACK = True

def parse(s):
    points = defaultdict(bool)

    for line in s.splitlines():
        line = re.sub(r"(e|w|nw|ne|sw|se)", r"\1 ", line)

        p = [0, 0]
        for d in line.split():
            go(p, d)
        p = tuple(p)
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
            for n in neighbors(t):
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
