#!/usr/bin/env python3

from enum import IntEnum, auto


ExampleInput1 = """\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
"""


class Op(IntEnum):
    CPY = auto()
    INC = auto()
    DEC = auto()
    JNZ = auto()
    TGL = auto()


def regnum(alpha):
    return ord(alpha) - ord("a")


def parse(s):
    prog = []
    for line in s.splitlines():
        op, *args = line.split()
        # Code is self-modifying so, unlike 2016-12, must delay int/reg eval
        match op := Op[op.upper()]:
            case Op.CPY:
                prog.append([op, args[0], args[1]])

            case Op.INC | Op.DEC:
                prog.append([op, args[0]])

            case Op.JNZ:
                prog.append([op, args[0], args[1]])

            case Op.TGL:
                prog.append([op, args[0]])

    return tuple(prog)


TOGGLES = {
    Op.CPY: Op.JNZ,
    Op.INC: Op.DEC,
    Op.DEC: Op.INC,
    Op.JNZ: Op.CPY,
    Op.TGL: Op.INC,
}


def run(prog, r=[0] * 4, optimize=False):
    ip = 0

    def val(maybelit):
        if maybelit.isalpha():
            return r[regnum(maybelit)]
        return int(maybelit)

    # from collections import Counter
    # counter = Counter()

    while 0 <= ip < len(prog):
        # Hot spot N-squared loop (4(567)89)
        #
        #     3: cpy 0 a
        #     4: cpy b c
        #     5: inc a
        #     6: dec c
        #     7: jnz c -2
        #     8: dec d
        #     9: jnz d -5
        #
        # In pseudocode:
        #
        #    3: a = 0
        #    #### OUTER LOOP
        #    4: c = b
        #    #### INNER LOOP
        #    5: a++
        #    6: c--
        #    7: if c: goto 5
        #    ####
        #    8: d--
        #    9: if d: goto 4
        #    ####
        #
        # Or, in python:
        #
        #     a = 0
        #     for _ in range(d):
        #         for _ in range(b):
        #             a += 1
        #     c = d = 0
        #
        # Which is equivalent to multiplication, as hinted:
        #
        #     a = d * b
        #     c = d = 0

        if optimize and ip == 3:
            r[0] = r[3] * r[1]
            r[2] = r[3] = 0
            ip = 10

        # if sum(counter.values()) > 10_000:
        #     print(counter)
        #     raise Exception("STOPPING")
        # counter[ip] += 1

        op, *args = prog[ip]
        match op:
            case Op.CPY:
                if args[1].isalpha():
                    rb = regnum(args[1])
                    r[rb] = val(args[0])

            case Op.INC:
                if args[0].isalpha():
                    ra = regnum(args[0])
                    r[ra] += 1

            case Op.DEC:
                if args[0].isalpha():
                    ra = regnum(args[0])
                    r[ra] -= 1

            case Op.JNZ:
                if val(args[0]) != 0:
                    ip += val(args[1])
                    continue

            case Op.TGL:
                tip = ip + val(args[0])
                if 0 <= tip < len(prog):
                    tgl = prog[tip]
                    tgl[0] = TOGGLES[tgl[0]]

        ip += 1

    return r[0]


def part1(s):
    return run(parse(s), [7, 0, 0, 0])


def part2(s):
    # Ugh of course this is a read and understand the assembly code problem.
    # Puzzle hints that you need to find some hard loop that can be optimized
    # into a multplication. But computers are fast now and just running it
    # finished in 2 minutes, so it was done before I finished thinking about
    # how to solve it in the intended way.
    #
    # But I guess I'm doing this for fun, so I went ahead and did it anyway.
    return run(parse(s), [12, 0, 0, 0], optimize=True)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (3)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (11340)")
    print(part1(real_input()))

    print()
    print("Part 2 (479007900)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
