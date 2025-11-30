#!/usr/bin/env python3

from enum import IntEnum
from itertools import count


ExampleInput1 = """\
s1,x3/4,pe/b
"""

class Op(IntEnum):
    SPIN = 0
    SWAPIDX = 1
    SWAPVAL = 2

OPS = {
    "s": Op.SPIN,
    "x": Op.SWAPIDX,
    "p": Op.SWAPVAL,
}

def parse(s):
    ops = []
    for s in s.strip().split(","):
        op, s = OPS[s[0]], s[1:]
        if op == Op.SPIN:
            ops.append((op, int(s)))
            continue

        a, b = s.split("/")
        if op == Op.SWAPIDX:
            a, b = int(a), int(b)
        ops.append((op, a, b))
    return tuple(ops)


def dance(ops, d, start):
    size = len(d)
    for (op, *args) in ops:
        match op:
            case Op.SPIN:
                start = (start - args[0]) % size

            case Op.SWAPVAL:
                a, b = args
                d[a], d[b] = d[b], d[a]

            case Op.SWAPIDX:
                ai, bi = args
                ai = (ai + start) % size
                bi = (bi + start) % size
                keys = list(d.keys())
                values = list(d.values())
                a = keys[values.index(ai)]
                b = keys[values.index(bi)]
                d[a], d[b] = d[b], d[a]

        # print(f"{Op(op).name} {args}")
        # print(tostr(d, start))
    return start


def iv(size):
    return {chr(ord("a") + i): i for i in range(size)}


def tostr(d, start):
    size = len(d)
    r = {v: k for k, v in d.items()}
    return "".join([r[(start + i) % size] for i in range(size)])


def part1(s, size=16):
    d = iv(size)
    start = dance(parse(s), d, 0)
    return tostr(d, start)


def part2(s, size=16):
    ops = parse(s)
    d = iv(size)
    start = 0

    # The example repeats every four cycles, so that seems like a big clue.
    # Find the cycle length of the real input.
    seen = {}
    for i in count():
        if (state := tostr(d, start)) in seen:
            break
        seen[state] = i
        start = dance(ops, d, start)

    nth = 1_000_000_000 % i
    return {i: k for k, i in seen.items()}[nth]


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (baedc)")
    print(part1(ExampleInput1, size=5))

    print()
    print("Part 1 (lbdiomkhgcjanefp)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (abcde [not given])")
    print(part2(ExampleInput1, size=5))

    print()
    print("Part 2 (ejkflpgnamhdcboi)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
