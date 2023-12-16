#!/usr/bin/env python3

from typing import NamedTuple

# fuck backslashes so hard
ExampleInput1 = """\
.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....
"""

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __lt__(self, other):
        if self.y != other.y:
            return self.y < other.y
        return self.x < other.x

NORTH = Point(0, -1)
WEST = Point(-1, 0)
EAST = Point(1, 0)
SOUTH = Point(0, 1)

# . empty space
# / \ mirror, have to think about how it rotates
#     / : N<>E S<>W
#     \ : N<>W S<>E
# - | splitter, entering from "pointy end" does nothing, flat side splits
#     - : E>E W>W N>E+W S>E+W
#     | : N>N S>S E>N+S W>N+S

class Tile:
    def __init__(self, p, c):
        self.p = p
        self.c = c
        self.visits = set()

    def is_dupe(self, indir):
        return indir in self.visits

    def is_energized(self):
        return len(self.visits) > 0

    def visit(self, indir):
        self.visits.add(indir)
        match self.c:
            case '.':
                return (indir,)
            case '/':
                if indir == NORTH:
                    return (EAST,)
                if indir == EAST:
                    return (NORTH,)
                if indir == SOUTH:
                    return (WEST,)
                if indir == WEST:
                    return (SOUTH,)
                raise Exception(f"Unknown direction #{indir}")
            case '\\':
                if indir == NORTH:
                    return (WEST,)
                if indir == WEST:
                    return (NORTH,)
                if indir == SOUTH:
                    return (EAST,)
                if indir == EAST:
                    return (SOUTH,)
                raise Exception(f"Unknown direction #{indir}")
            case '-':
                if indir == EAST or indir == WEST:
                    return (indir,)
                else:
                    return (EAST, WEST)
            case '|':
                if indir == NORTH or indir == SOUTH:
                    return (indir,)
                else:
                    return (NORTH, SOUTH)


def parse(s):
    tiles = []
    for y, line in enumerate(s.splitlines()):
        tiles.append([Tile(Point(x,y), c) for x,c in enumerate(line)])
    return tiles


INITIAL = (Point(0, 0), EAST,)


def part1(s):
    return do_it(s, INITIAL)


def do_it(s, start):
    tiles = parse(s)
    assert len(tiles) == len(tiles[0]), f"{len(tiles)} != {len(tiles[0])}"
    size = len(tiles)
    beams = [start]
    while beams:
        p, v = beams.pop()
        tile = tiles[p.y][p.x]
        if tile.is_dupe(v):
            continue
        outs = tile.visit(v)
        for out in outs:
            p0 = p + out
            if 0 <= p0.x < size and 0 <= p0.y < size:
                beams.append((p + out, out))

    total = 0
    for y in range(size):
        for x in range(size):
            if tiles[y][x].is_energized():
                total += 1

    return total


def part2(s):
    size = len(s.splitlines())

    vals = []
    for x in range(size):
        vals.append(do_it(s, (Point(x, 0), SOUTH)))
        vals.append(do_it(s, (Point(x, size - 1), NORTH)))
    for y in range(size):
        vals.append(do_it(s, (Point(0, y), EAST)))
        vals.append(do_it(s, (Point(size - 1, y), WEST)))

    return max(vals)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (46)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (6906)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (51)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (7330)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
