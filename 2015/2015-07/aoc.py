#!/usr/bin/env pypy3

from collections import deque


ExamplePart1 = """\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""


Ops = {
    "COPY": lambda args: args[0],
    "AND": lambda args: args[0] & args[1],
    "OR": lambda args: args[0] | args[1],
    "LSHIFT": lambda args: (args[0] << args[1]) & 0xFFFF,
    "RSHIFT": lambda args: args[0] >> args[1],
    "NOT": lambda args: ~args[0] & 0xFFFF,
}



def parse(s):
    state = {}
    prog = []

    for line in s.splitlines():
        inst, dst = line.split(" -> ")
        try:
            state[dst] = int(inst)
        except ValueError:
            toks = inst.split()
            match len(toks):
                case 1:
                    prog.append((dst, Ops["COPY"], (toks[0],)))

                case 2:
                    prog.append((dst, Ops[toks[0]], (toks[1],)))

                case 3:
                    prog.append((dst, Ops[toks[1]], (toks[0], toks[-1])))

    return state, prog


def run(state, prog):
    prog = deque(prog)

    def resolve(a):
        if a.isalpha():
            return state[a]
        else:
            return int(a)

    while prog:
        dst, op, args = inst = prog.popleft()
        try:
            args = tuple(resolve(a) for a in args)
        except (ValueError, KeyError):
            prog.append(inst)
            continue

        state[dst] = op(args)

    return state


def part1(s):
    return run(*parse(s))["a"]


def part2(s):
    state, prog = parse(s)
    state1 = run(state.copy(), prog)
    state["b"] = state1["a"]
    run(state, prog)
    return state["a"]


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print(f"Example Part 1)")
    print(run(*parse(ExamplePart1)))
    print()

    print("Part 1 (46065)")
    print(part1(real_input()))
    print()

    print("Part 2 (14134)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
