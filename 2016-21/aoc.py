#!/usr/bin/env pypy3

from collections import deque
from enum import IntEnum, auto
from itertools import permutations


ExampleInput1 = """\
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
"""


class Op(IntEnum):
    SWAP_POS = auto()
    SWAP_VAL = auto()
    ROTATE_LEFT = auto()
    ROTATE_RIGHT = auto()
    ROTATE_VAL = auto()
    REVERSE_POS = auto()
    MOVE_POS = auto()


def parse(s):
    prog = []
    for line in s.splitlines():
        toks = line.split()
        match toks[:2]:
            case ["swap", "position"]:
                prog.append((Op.SWAP_POS, int(toks[2]), int(toks[-1])))

            case ["swap", "letter"]:
                prog.append((Op.SWAP_VAL, toks[2], toks[-1]))

            case ["rotate", "left"]:
                prog.append((Op.ROTATE_LEFT, int(toks[2]), None))

            case ["rotate", "right"]:
                prog.append((Op.ROTATE_RIGHT, int(toks[2]), None))

            case ["rotate", "based"]:
                prog.append((Op.ROTATE_VAL, toks[-1], None))

            case ["reverse", "positions"]:
                prog.append((Op.REVERSE_POS, int(toks[2]), int(toks[-1])))

            case ["move", "position"]:
                prog.append((Op.MOVE_POS, int(toks[2]), int(toks[-1])))


    return prog


def run(prog, seed):
    d = deque(seed)

    # I dunno what part 2 might be, but it seems like our maximum possible seed
    # is not that long, so I think probably just using a deque will be fine

    for op, a, b in prog:
        match op:
            case Op.SWAP_POS:
                d[a], d[b] = d[b], d[a]

            case Op.SWAP_VAL:
                ai, bi = d.index(a), d.index(b)
                d[ai], d[bi] = d[bi], d[ai]

            case Op.ROTATE_LEFT:
                d.rotate(-a)

            case Op.ROTATE_RIGHT:
                d.rotate(a)

            case Op.ROTATE_VAL:
                ai = d.index(a)
                if ai >= 4:
                    ai += 1
                d.rotate(ai + 1)

            case Op.REVERSE_POS:
                d.rotate(-a)
                tmp = []
                for _ in range(a, b+1):
                    tmp.append(d.popleft())
                for c in tmp:
                    d.appendleft(c)
                d.rotate(a)

            case Op.MOVE_POS:
                c = d[a]
                d.remove(c)
                d.insert(b, c)

    return "".join(d)


def part1(s, seed="abcdefgh"):
    return run(parse(s), seed)


# 8! is only like 40k
def part2(s):
    prog = parse(s)
    for p in permutations("abcdefgh"):
        p = "".join(p)
        out = run(prog, p)
        if out == "fbgdceah":
            return p
    return "NO SOLUTION FOUND"


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (decab)")
    print(part1(ExampleInput1, seed="abcde"))

    print()
    print("Part 1 (bfheacgd)")
    print(part1(real_input()))

    print()
    print("Part 2 (gcehdbfa)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
