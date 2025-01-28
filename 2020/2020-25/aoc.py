#!/usr/bin/env pypy3

from itertools import islice


ExampleInput1 = """\
5764801
17807724
"""


HANDSHAKE_SUBJECT = 7
MODULUS = 20201227


def parse(s):
    return tuple(map(int, s.splitlines()))


def transform(subject):
    n = 1
    while True:
        n *= subject
        n %= MODULUS
        yield n


def part1(s):
    card, door = parse(s)

    for i, x in enumerate(transform(HANDSHAKE_SUBJECT)):
        if x == card:
            break

    return next(islice(transform(door), i, i + 1))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (14897079)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (9620012)")
    print(part1(real_input()))


if __name__ == "__main__":
    run_all()
