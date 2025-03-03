#!/usr/bin/env pypy3

from enum import IntEnum, auto


ExampleInput1 = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
"""


class Op(IntEnum):
    CPY = auto()
    INC = auto()
    DEC = auto()
    JNZ = auto()


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

    return tuple(prog)


def run(prog, r=[0] * 4):
    ip = 0

    def val(maybelit):
        if maybelit.isalpha():
            return r[regnum(maybelit)]
        return int(maybelit)

    while 0 <= ip < len(prog):
        op, *args = prog[ip]
        match op:
            case Op.CPY:
                r[args[1]] = val(args[0])

            case Op.INC:
                r[args[0]] += 1

            case Op.DEC:
                r[args[0]] -= 1

            case Op.JNZ:
                if val(args[0]) != 0:
                    ip += args[1]
                    continue
        ip += 1

    return r[0]


def part1(s):
    return run(parse(s))


def part2(s):
    return run(parse(s), [0, 0, 1, 0])


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (42)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (318117)")
    print(part1(real_input()))

    print()
    print("Part 2 (9227771)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
