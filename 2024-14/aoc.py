#!/usr/bin/env pypy3

from collections import defaultdict
from math import prod
from more_itertools import sliding_window


ExampleInput1 = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

def parse(s):
    ic = []
    for line in s.splitlines():
        ps, vs = line.split()
        p0 = tuple(map(int, ps.split('=')[1].split(',')))
        v0 = tuple(map(int, vs.split('=')[1].split(',')))
        ic.append((p0, v0))
    return ic


def part1(s, w=101, h=103):
    tmax = 100
    ic = parse(s)
    quads = [0] * 4
    for (x0, y0), (vx, vy) in sorted(ic):
        f = ((x0 + vx * tmax) % w, (y0 + vy * tmax) % h)
        q = 0
        if f[0] == w//2 or f[1] == h//2 :
            continue
        if f[0] > w//2:
            q |= 1
        if f[1] > h//2:
            q |= 2
        quads[q] += 1

    return prod(quads)


def print_tree(fd, tmax, w, h):
    s = []
    for y in range(h):
        for x in range(w):
            match fd[(x, y)]:
                case 0:
                    s.append('.')
                case n:
                    s.append(str(n))
        s.append("\n")
    print("".join(s))
    print(f"{tmax=}")


LONG_RUN = 10

# I actually just dumped the first 10,000 print_tree outputs to a file and
# grepped for a long row of non-dots in a row, but then I came back and
# implemented that strategy in code
def part2(s, w=101, h=103):
    ic = parse(s)

    tmax = 1
    while True:
        fd = defaultdict(int)
        for (x0, y0), (vx, vy) in ic:
            f = ((x0 + vx * tmax) % w, (y0 + vy * tmax) % h)
            fd[f] += 1

        run = 0
        for (x0, y0), (x1, y1) in sliding_window(sorted(fd.keys()), 2):
            if x0 == x1 and y1 - y0 <= 1:
                run += 1
                if run >= LONG_RUN:
                    #print_tree(fd, tmax, w, h)
                    return tmax
            else:
                run = 0
        tmax += 1


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (12)")
    print(part1(ExampleInput1, 11, 7))

    print()
    print("Part 1 (214400550)")
    print(part1(real_input()))

    print()
    print("Part 2 (8149)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
