#!/usr/bin/env python3

import numpy as np


ExampleInput1 = """\
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
"""


InitialStatePattern = ".#./..#/###"


ROTATIONS = (
    lambda a: a,
    lambda a: np.rot90(a),
    lambda a: np.rot90(np.rot90(a)),
    lambda a: np.rot90(np.rot90(np.rot90(a))),
)

FLIPPED_ROTATIONS = tuple(map(lambda r: lambda a: np.fliplr(r(a)), ROTATIONS))

ORIENTATIONS = ROTATIONS + FLIPPED_ROTATIONS


def orientations(a):
    for o in ORIENTATIONS:
        yield o(a)


def pata(pat):
    pat = pat.translate(str.maketrans(".#", "01"))
    return np.array(
        [list(line) for line in pat.split("/")],
        np.uint8
    )


def atup(a):
    return tuple(tuple(map(int, row)) for row in a)


def parse(s):
    rules = {}

    for line in s.splitlines():
        a, b = line.split(" => ")
        a = pata(a)
        b = pata(b)
        for o in orientations(a):
            rules[atup(o)] = b

    return rules


def xform(rules, a):
    size = a.shape[0]

    if 0 == size % 2:
        astep = 2
    else:
        assert(0 == size % 3)
        astep = 3

    steps = size // astep
    bstep = astep + 1
    b = np.zeros((steps * bstep,)*2, np.uint8)

    for j in range(steps):
        ajslice = slice(astep*j, astep*(j+1))
        bjslice = slice(bstep*j, bstep*(j+1))
        for i in range(steps):
            aislice = slice(astep*i, astep*(i+1))
            bislice = slice(bstep*i, bstep*(i+1))

            b[bjslice, bislice] = rules[atup(a[ajslice, aislice])]

    return b


def part1(s, n=5):
    rules = parse(s)

    a = pata(InitialStatePattern)

    for _ in range(n):
        a = xform(rules, a)

    return np.sum(a)


# I thought I would have to do some trick like identify identical subblocks but
# numpy just solves it in like 2 seconds, so I guess not.
def part2(s):
    return part1(s, n=18)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1")
    print(part1(ExampleInput1, n=2))

    print()
    print("Part 1")
    print(part1(real_input()))

    print()
    print("Part 2")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
