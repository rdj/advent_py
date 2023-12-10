#!/usr/bin/env python3

import math

from collections import defaultdict
from functools import cached_property
from typing import NamedTuple

ExampleInput0 = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

ExampleInput1 = """\
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

ExampleInput2 = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

ExampleInput3 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

ExampleInput4 = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

class Point(NamedTuple):
    x: int
    y: int

    def neighbors(self):
        return (self + d for d in DIRECTIONS)

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

DIRECTIONS = tuple(sorted((
    NORTH, WEST, EAST, SOUTH
)))

CONNECTIONS = {
    '.' : (),
    '|' : tuple(sorted((NORTH, SOUTH))),
    '-' : tuple(sorted((WEST, EAST))),
    'J' : tuple(sorted((NORTH, WEST))),
    'L' : tuple(sorted((NORTH, EAST))),
    '7' : tuple(sorted((WEST, SOUTH))),
    'F' : tuple(sorted((EAST, SOUTH))),
}

# When we double the area, the pipe stays one square wide and connects through
# the upper-left of each quad
DOUBLED = {
    '.' : ('..',
           '..'),
    '|' : ('|.',
           '|.'),
    '-' : ('--',
           '..'),
    'L' : ('L-',
           '..'),
    'J' : ('J.',
           '..'),
    '7' : ('7.',
           '|.'),
    'F' : ('F-',
           '|.'),
}

class Grid:
    def __init__(self, s):
        self.grid = s.splitlines()
        assert self.start
        assert self.start_is_like

    @cached_property
    def height(self):
        return len(self.grid)

    @cached_property
    def width(self):
        return len(self.grid[0])

    def get(self, p):
        if p.x < 0 or p.x >= self.width or p.y < 0 or p.y >= self.height:
            return None
        if p == self.start:
            return self.start_is_like
        return self.grid[p.y][p.x]

    def connections(self, p):
        if tile := self.get(p):
            return [p + c for c in CONNECTIONS[tile]]
        return []

    def neighbors(self, p):
        return [n for n in p.neighbors() if 0 <= n.x < self.width and 0 <= n.y < self.height]

    @cached_property
    def first_steps(self):
        firsts = []
        for p in self.start.neighbors():
            if self.start in self.connections(p):
                firsts.append(p)
        assert(2 == len(firsts))
        return tuple(firsts)

    @cached_property
    def start(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 'S':
                    return Point(x, y)
        raise Exception("No start tile")

    @cached_property
    def start_is_like(self):
        start_connections = tuple(sorted([f - self.start for f in self.first_steps]))
        for k, v in CONNECTIONS.items():
            if v == start_connections:
                return k
        assert False, "Start connections unmapped"

    def __repr__(self):
        return "\n".join(str(line) for line in self.grid)


def part1(s):
    g = Grid(s)
    firsts = g.first_steps

    dists = defaultdict(lambda : math.inf)
    for first in firsts:
        last = g.start
        cur = first
        steps = 0

        while cur != g.start:
            steps += 1
            dists[cur] = min(dists[cur], steps)
            dest = [c for c in g.connections(cur) if c != last][0]
            last = cur
            cur = dest

    return max(dists.values())


def part2(s):
    g = Grid(s)

    # Discover the loop, similar to part 1 but no need to go both ways
    loop = [g.start]
    last = g.start
    cur = g.first_steps[0]
    while cur != g.start:
        loop.append(cur)
        dest = [c for c in g.connections(cur) if c != last][0]
        last = cur
        cur = dest
    loop = set(loop)

    # Create a new grid with 2x dimensions, leaving the pipe just 1 wide so
    # stuff can fit in between
    x2loop = set()
    x2grid = [list('.' * g.width * 2) for _ in range(g.height * 2)]
    for psrc in loop:
        x2pipe = DOUBLED[g.get(psrc)]
        for dy in range(2):
            for dx in range(2):
                pdst = Point(2*psrc.x + dx, 2*psrc.y + dy)
                c = x2pipe[dy][dx]
                if c != '.':
                    x2loop.add(pdst)
                x2grid[pdst.y][pdst.x] = c

    # Fix the start square, could have skipped this but it was super helpful
    # when printing and debugging
    for dy in range(2):
        for dx in range(2):
            p = Point(g.start.x*2 + dx, g.start.y*2 + dy)
            if x2grid[p.y][p.x] == g.start_is_like:
                x2grid[p.y][p.x] = 'S'
                break

    x2grid = Grid("\n".join("".join(_) for _ in x2grid))


    # Pretty inefficient BFS just goes around and marks everything reachable
    # from the edges
    outside = set()
    def mark_outside(p):
        to_visit = [p]
        while to_visit:
            p = to_visit.pop()
            outside.add(p)
            for n in x2grid.neighbors(p):
                if n not in x2loop and n not in outside:
                    to_visit.append(n)

    for y in range(x2grid.height):
        for x in range(x2grid.width):
            p = Point(x, y)
            if p in x2loop or p in outside:
                continue
            if len(x2grid.neighbors(p)) < 4:
                mark_outside(p)

    # Go through and count up things that didn't get marked but be careful not
    # to count any phantom ground tiles that were created through our area
    # expansion
    incount = 0
    for y in range(g.height):
        for x in range(g.width):
            psrc = Point(x, y)
            pdst = Point(2*x, 2*y)
            if psrc not in loop and pdst not in outside:
                incount += 1

    return incount


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (4)")
    print(part1(ExampleInput0))

    print()
    print("Example Part 1 (8)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (6733)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (4)")
    print(part2(ExampleInput2))

    print()
    print("Example Part 2 (8)")
    print(part2(ExampleInput3))

    print()
    print("Example Part 2 (10)")
    print(part2(ExampleInput4))

    print()
    print("Part 2 (435)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
