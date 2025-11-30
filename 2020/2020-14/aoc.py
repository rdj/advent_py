#!/usr/bin/env python3


import re


ExampleInput1 = """\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""

ExampleInput2 = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""


ALL_ONES = 2**37 - 1

MASK = 0
MEM = 1


def parse(s):
    lines = s.splitlines()

    prog = []
    for line in s.splitlines():
        a, b = line.split(" = ")
        if a == "mask":
            ormask = 0
            andmask = 0
            exbits = []
            for i, c in enumerate(reversed(b)):
                match c:
                    case "0":
                        andmask |= 1 << i
                    case "1":
                        ormask |= 1 << i
                    case "X":
                        exbits.append(i)
            andmask ^= ALL_ONES
            prog.append((MASK, (ormask, andmask, exbits)))
        else:
            p = int(re.sub(r"[^\d]", "", a))
            prog.append((MEM, (p, int(b))))

    return prog


def part1(s):
    prog = parse(s)
    ormask, andmask = None, None
    mem = {}

    for op, code in prog:
        if op == MASK:
            ormask, andmask, _ = code
            continue

        p, d = code
        d |= ormask
        d &= andmask
        mem[p] = d

    return sum(mem.values())


def apply_exbits(p, exbits):
    if len(exbits) == 0:
        return [p]

    b, rest = exbits[0], exbits[1:]
    return apply_exbits(p & (ALL_ONES ^ 1 << b), rest) + apply_exbits(p | 1 << b, rest)


def part2(s):
    prog = parse(s)

    ormask, exbits = None, None
    mem = {}

    for op, code in prog:
        if op == MASK:
            ormask, _, exbits = code
            continue

        p, d = code

        p |= ormask
        for pa in apply_exbits(p, exbits):
            mem[pa] = d

    return sum(mem.values())


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (165)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (8471403462063)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (208)")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (2667858637669)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
