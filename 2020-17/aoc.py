#!/usr/bin/env python3


import numpy as np


ExampleInput1 = """\
.#.
..#
###
"""


def parse(s):
    return [[c == '#' for c in line] for line in s.splitlines()]


def dump(a):
    s = []
    for z in range(len(a)):
        s.append(f"z={z}\n")
        xy = a[:, :, z]
        for y in range(len(a)):
            for x in range(len(a)):
                s.append("#" if xy[x, y] else ".")
            s.append("\n")
    print("".join(s))


def run(iv, niter, ndim):
    size = max(len(iv), len(iv[0])) + 2*niter
    if 0 == size % 2:
        size += 1
    src = np.zeros([size] * ndim, bool)

    for y in range(len(iv)):
        for x in range(len(iv[0])):
            idx = (x + niter, y + niter) + (niter,)*(ndim-2)
            src[idx] = iv[y][x]

    dst = np.empty_like(src)
    for i in range(niter):
        it = np.nditer(src, flags=["multi_index"])
        for c in it:
            p = it.multi_index
            slc = tuple([slice(v-1 if v-1 > 0 else 0, v+2 if v+2 < size else size) for v in p])
            trues = np.count_nonzero(src[slc])
            if c:
                dst[p] = (2 <= trues - 1 <= 3)
            else:
                dst[p] = (3 == trues)
        src, dst = dst, src

    return src.sum()


def part1(s):
    return run(parse(s), 6, 3)


def part2(s):
    return run(parse(s), 6, 4)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (112)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (276)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (848)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (2136)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
