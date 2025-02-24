#!/usr/bin/env pypy3

from collections import defaultdict
from itertools import count, product


ExamplesPart1 = (
    ("1", 0),
    ("12", 3), # 2 + 1
    ("23", 2), # 2 + 0
    ("1024", 31),
)


def parse(s):
    return int(s.strip())


# Example spiral:
#
#   17  16  15  14  13
#   18   5   4   3  12 .
#   19   6   1   2  11 .
#   20   7   8   9  10 .   .
#   21  22  23  24  25 26  .   .
#                  ... 49 ...  .
#                     ...  81 ...
#
# Notice the odd squares starting at one moving down-right:
#   - 1, 9, 25, 49, 81, ...
#
# Each ring of the spiral runs from an odd square + 1 to the next odd square.
# We want to number the rings based on their distance from the center.
#  - Ring 0 =           1 ...  1 = 1*1  (inclusive ranges)
#  - Ring 1 =  1 + 1 =  2 ...  9 = 3*3
#  - Ring 2 =  9 + 1 = 10 ... 25 = 5*5
#  - Ring 3 = 25 + 1 = 26 ... 49 = 7*7
#  - ...
#
def ring(n):
    if n == 0:
        return range(1, 2)
    return range(ring(n-1)[-1] + 1, (2*n + 1)*(2*n + 1) + 1)


# Each ring of the spiral starts one position to the right of the odd square
# that ended the previous ring. The new ring progresses counter-clockwise
# around the grid to end with the odd square in the bottom-right corner.
# It's easiest to find the corners by starting at the end and subtracting.
#
# For example:
#  - r = ring(1) == range(2, 10)
#    len(r) // 4 == 8 // 4 == 2
#    corners [ 9, (-2=) 7, (-2=) 5, (-2)= 3 ]
#  - r = ring(2) == range(10, 26)
#    len(r) // 4 == 16 // 4 == 4
#    corners [ 25, (-4=) 21, (-4=) 17, (=4=) 13 ]
#
def corners(n):
    r = ring(n)
    delta = len(r) // 4
    return [r[-1] - (3-x) * delta for x in range(4)]


# The shortest path to the center (and hence length of the manhattan distance)
# is going to be along a side to the nearest midpoint then towards the center.
# The distance of the ring from the center is simply its ring number. We can
# find the midpoints based on the corners.
def midpoints(n):
    corns = corners(n)
    delta = (corns[1] - corns[0]) // 2
    return [c - delta for c in corns]


def manhattan(x):
    ring = (int((x - 1) ** 0.5) + 1) // 2
    dist = min(abs(x - m) for m in midpoints(ring))
    return ring + dist


def part1(s):
    return manhattan(parse(s))


def ispiral():
    # Ring 0 is special
    n = 1
    x, y = 0, 0
    yield x, y

    # For each ring outwards ...
    for r in count(1):
        # ... start one to the right of the previous ring's end ...
        n += 1
        x += 1
        yield x, y

        # ... move upwards ...
        dx, dy = 0, -1
        for c in corners(r):
            while n < c:
                n += 1
                x += dx
                y += dy
                yield x, y
            # .. and turn counterclockwise at each corner
            dx, dy = dy, -dx


ADJACENCY = tuple(dxdy for dxdy in product((-1, 0, 1), repeat=2) if dxdy != (0,0))
def neighbors(xy):
    x, y = xy
    for dx, dy in ADJACENCY:
        yield (x+dx, y+dy)


def part2(s):
    # It's just https://oeis.org/A141481, but for fun let's compute it.
    limit = parse(s)

    d = defaultdict(int)

    coords = ispiral()
    d[next(coords)] = 1

    for c in coords:
        x = d[c] = sum(d[n] for n in neighbors(c))
        if x > limit:
            return x


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1, 1):
        print(f"Example {i} Part 1 ({b})")
        print(part1(a))
        print()

    print("Part 1 (438)")
    print(part1(real_input()))
    print()

    print("Part 2 (266330)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
