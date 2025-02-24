#!/usr/bin/env pypy3

import operator
from collections import defaultdict


ExampleInput1 = """\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
"""


OPS = {
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    'inc': operator.add,
    'dec': operator.sub,
}


def parse(s):
    prog = []
    for linetoks in map(str.split, s.splitlines()):
        prog.append(tuple((reg, OPS[op], int(lit)) for reg, op, lit in (linetoks[:3], linetoks[4:])))
    return tuple(prog)


def run(s):
    env = defaultdict(int)
    prog = parse(s)
    maxever = 0 # All registers start at 0, so it's a safe default
    for incdec, cond in prog:
        r, op, lit = cond
        if op(env[r], lit):
            r, op, lit = incdec
            env[r] = op(env[r], lit)
            maxever = max(maxever, env[r])

    return max(env.values()), maxever


def part1(s):
    return run(s)[0]


def part2(s):
    return run(s)[1]


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (1)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (5102)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (10)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (6056)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
