#!/usr/bin/env python3

import operator as op


CLUES = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

CLUE_OPS = {
    "children": op.eq,
    "cats": op.gt,
    "samoyeds": op.eq,
    "pomeranians": op.lt,
    "akitas": op.eq,
    "vizslas": op.eq,
    "goldfish": op.lt,
    "trees": op.gt,
    "cars": op.eq,
    "perfumes": op.eq,
}


def parse(s):
    sues = []
    for line in s.splitlines():
        label, props = line.split(": ", 1)
        n = int(label.split()[-1])

        d = {}
        for prop in props.split(", "):
            k, v = prop.split(": ")
            d[k] = int(v)
        sues.append((n, d))
    return sues


def solve(s, use_ops=False):
    sues = parse(s)

    for n, sue in sues:
        sat = True
        for k, v in sue.items():
            o = CLUE_OPS[k] if use_ops else op.eq
            if not o(v, CLUES[k]):
                sat = False
                break
        if sat:
            return n

    raise Exception("No sat")


def part1(s):
    return solve(s)


def part2(s):
    return solve(s, True)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Part 1 (103)")
    print(part1(real_input()))
    print()

    print("Part 2 (405)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
