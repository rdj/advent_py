#!/usr/bin/env pypy3

from collections import defaultdict
from itertools import product, islice


ExamplesPart1 = (
    ("1", 0),
    ("12", 3), # 2 + 1
    ("23", 2), # 2 + 0
    ("1024", 31),
)


def parse(s):
    return int(s.strip())


def part1(s):
    n = parse(s)
    if n == 1:
        return 0

    ring = (int((n - 1) ** 0.5) + 1) // 2

    ringstart = (ring * 2 - 1)
    ringstart *= ringstart
    ringstart += 1

    ringend = (ring * 2 + 1)
    ringend *= ringend

    delta = (ringend + 1 - ringstart) // 4

    corners = [ringend - n * delta for n in range(4)]
    mids = [c - delta // 2 for c in corners]
    dist = min(abs(n - m) for m in mids)

    return ring + dist


def icorners():
    n = 1
    nsq = 1
    while True:
        n += 2 # odds only

        prevsq = nsq
        nsq = n*n

        delta = (nsq - prevsq) // 4
        corners = [nsq - (3-x) * delta for x in range(4)]
        yield from corners


def ispiral():
    n = 1
    x, y = 0, 0
    yield x, y

    corners = icorners()

    while True:
        n += 1
        x += 1
        dx, dy = 0, -1
        yield x, y

        for _ in range(4):
            corner = next(corners)
            while n < corner:
                n += 1
                x += dx
                y += dy
                yield x, y
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
