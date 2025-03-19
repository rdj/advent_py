#!/usr/bin/env pypy3

import re
from itertools import permutations


USED = 0
FREE = 1

def parse(s):
    d = {}
    intpat = re.compile(r"\d+")
    for line in s.splitlines()[2:]:
        x, y, _, used, free, _ = list(map(int, re.findall(intpat, line)))
        d[(x,y)] = (used, free)
    return d


def part1(s):
    nodes = parse(s)

    def viable(a, b):
        return a[USED] > 0 and a[USED] <= b[FREE]

    return sum(1 for a, b in permutations(nodes.values(), 2) if viable(a, b))


def find_xmax_hole_and_wall(s):
    nodes = parse(s)

    xmax = 0

    # One empty node, the "hole"
    hole = None
    holesize = None
    for pos, (used, free) in nodes.items():
        xmax = max(xmax, pos[0])
        if used == 0:
            assert(hole is None)
            hole = pos
            holesize = free

    # The "wall" is an unbroken horizontal line with a gap on the left that
    # extends all the way to the right edge
    walls = []
    for pos, (used, free) in nodes.items():
        if used > holesize:
            walls.append(pos)
    wall = (min(w[0] for w in walls), walls[0][1])
    r = range(wall[0], xmax+1)
    assert(len(r) == len(walls))
    for x in r:
        assert((x, wall[1]) in walls)

    # The hole is under the wall
    assert(hole[0] > wall[0])
    assert(hole[1] > wall[1])

    return xmax, hole, wall


# The puzzle text for part 2 posits a lot of potential constraints on the
# problem. But it uses an minimally small example grid that's not very useful.
# Let's look at the real input data and what constraints we can find that the
# puzzle hints at, and if that will make it solvable.
#
# I printed the pairs discovered in part1, and it turns out there's only one
# valid destination node, which is the single empty node. We will call this
# node the "hole".
#
# So the mechanic for moving stuff is going to be very similar to the classic
# children's sliding tile game that has a single missing tile that you use to
# move around the other tiles:
#
#    https://en.wikipedia.org/wiki/Sliding_puzzle
#
# Almost every node's data fits in the hole, but there are a few exceptions
# where the used space exceeds the hole size. We will call these nodes "walls".
#
# I printed out the location of the wall nodes, and it turns out it's a single
# big wall that goes almost but not quite all the way across the grid.
#
# The hole is underneath the wall.
#
# The general look of our puzzle then is:
#
#         G..........D     [G]oal, [D]ata, [H]ole, [W]all
#         ............
#         ............
#         ...WWWWWWWWW
#         ............
#         .......H....
#
# The puzzle can be solved in a couple of stages.
#
# 1. Move H around the wall and up into the position left of D.
#
#         G.XXXXXXXXXD   X = Path of H
#         ..X.........
#         ..X.........
#         ..XWWWWWWWWW
#         ..X.........
#         ..XXXXXH....
#
# 2. Move the data left a square, then move H back around to the left:
#
#         G........XDH
#         .........XXX
#
# That process is repeated until D ends up in the leftmost square.
#
# So we can reduce the problem to the width of the grid, the y-coordinate and
# width of the wall section, and the initial position of the hole.
#
def part2(s):
    xmax, (xhole, yhole), (xwall, ywall) = find_xmax_hole_and_wall(s)

    steps = 0

    # Wall moves into the column to the left of the wall edge
    steps += xhole - (xwall - 1)

    # Hole moves to the first row
    steps += yhole

    # Wall moves to the left of the data's starting location
    steps += xmax - xwall

    # Data has to move to the goal
    steps += xmax

    # Hole "recovers", circling around D after each step but final
    steps += (xmax - 1) * 4

    return steps


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Part 1 (892)")
    print(part1(real_input()))
    print()

    print("Part 2 (227)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
