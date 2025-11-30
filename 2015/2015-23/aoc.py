#!/usr/bin/env python3

import re
from enum import IntEnum, auto


class Op(IntEnum):
    HLF = auto()
    TPL = auto()
    INC = auto()
    JMP = auto()
    JIE = auto()
    JIO = auto()


def parse(s):
    prog = []
    for line in s.splitlines():
        line = re.sub(",", "", line)
        op, *args = line.split()
        match op := Op[op.upper()]:
            case Op.HLF | Op.TPL | Op.INC:
                prog.append((op, 0 if args[0] == "a" else 1))

            case Op.JMP:
                prog.append((op, int(args[0])))

            case Op.JIE | Op.JIO:
                prog.append((op, 0 if args[0] == "a" else 1, int(args[1])))

    return tuple(prog)


def run(prog, regs=None):
    if regs is None:
        regs = [0, 0]

    ip = 0
    while 0 <= ip < len(prog):
        # print(regs)
        # print(f"{ip=}", prog[ip])
        op, *args = prog[ip]
        match op:
            case Op.HLF:
                regs[args[0]] //= 2

            case Op.TPL:
                regs[args[0]] *= 3

            case Op.INC:
                regs[args[0]] += 1

            case Op.JMP:
                ip += args[0]
                continue

            case Op.JIE:
                if regs[args[0]] % 2 == 0:
                    ip += args[1]
                    continue

            case Op.JIO:
                if regs[args[0]] == 1:
                    ip += args[1]
                    continue

        ip += 1

    return regs


def part1(s):
    return run(parse(s))[1]


def part2(s):
    return run(parse(s), [1, 0])[1]


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Part 1 (184)")
    print(part1(real_input()))
    print()

    print("Part 2 (231)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
