#!/usr/bin/env python3

from itertools import islice


# I thought for sure with coprime numbers and modular arithmetic this was going
# to be some kind of number theory or cycle detection type problem, but nope.
AFACTOR = 16807
BFACTOR = 48271
MODULUS = 2147483647
MASK = 2**16 - 1


ExampleInput1 = """\
Generator A starts with 65
Generator B starts with 8921
"""


def parse(s):
    return tuple(int(line.split()[-1]) for line in s.splitlines())


def generator(factor, x, multiple):
    while True:
        x *= factor
        x %= MODULUS
        if 0 == x % multiple:
            yield x


def run(s, stopat, multa, multb):
    iva, ivb = parse(s)
    gena = generator(AFACTOR, iva, multa)
    genb = generator(BFACTOR, ivb, multb)

    n = 0

    for a, b in islice(zip(gena, genb), stopat):
        if a & MASK == b & MASK:
            n += 1

    return n


def part1(s):
    return run(s, 40_000_000, 1, 1)


def part2(s):
    return run(s, 5_000_000, 4, 8)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (588)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (650)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (309)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (336)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
