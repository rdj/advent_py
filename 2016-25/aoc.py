#!/usr/bin/env pypy3

from enum import IntEnum, auto
from itertools import count


class Op(IntEnum):
    CPY = auto()
    INC = auto()
    DEC = auto()
    JNZ = auto()
    OUT = auto()


def regnum(alpha):
    return ord(alpha) - ord("a")


def parse(s):
    prog = []
    for line in s.splitlines():
        op, *args = line.split()
        match op := Op[op.upper()]:
            case Op.CPY:
                prog.append((op, args[0], regnum(args[1])))

            case Op.INC | Op.DEC:
                prog.append((op, regnum(args[0])))

            case Op.JNZ:
                prog.append((op, args[0], int(args[1])))

            case Op.OUT:
                prog.append((op, args[0]))

    return tuple(prog)


def run(prog, r=[0] * 4):
    lastout = 1
    ticks = 0

    def val(maybelit):
        if maybelit.isalpha():
            return r[regnum(maybelit)]
        return int(maybelit)

    ip = 0
    while 0 <= ip < len(prog):
        ticks += 1
        if ticks > 100_000:
            return 0

        op, *args = prog[ip]
        match op:
            case Op.CPY:
                r[args[1]] = val(args[0])

            case Op.INC:
                r[args[0]] += 1

            case Op.DEC:
                r[args[0]] -= 1

            case Op.OUT:
                out = val(args[0])
                if out == lastout:
                    return ticks
                lastout = out

            case Op.JNZ:
                if val(args[0]) != 0:
                    ip += args[1]
                    continue
        ip += 1

    raise Exception("Program should run forever")


def part1(s):
    prog = parse(s)
    for n in count():
        t = run(prog, [n, 0, 0, 0])
        if t == 0:
            return n


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Part 1")
    print(part1(real_input()))


if __name__ == "__main__":
    run_all()
