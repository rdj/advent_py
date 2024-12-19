#!/usr/bin/env pypy3

from functools import cache


ExampleInput1 = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

def parse(s):
    bits, patterns = s.split("\n\n")
    bits = bits.split(", ")
    patterns = tuple(patterns.splitlines())
    bits.sort(lambda s: -len(s))
    bits = tuple(bits)
    return bits, patterns

@cache
def canfit(bits, pattern):
    if len(pattern) == 0:
        return True
    for b in bits:
        if pattern.startswith(b):
            if (canfit(bits, pattern[len(b):])):
                return True
    return False

@cache
def numfit(bits, pattern):
    if len(pattern) == 0:
        return 1
    c = 0
    for b in bits:
        if pattern.startswith(b):
            c += numfit(bits, pattern[len(b):])
    return c


def part1(s):
    bits, patterns = parse(s)
    c = 0
    for p in patterns:
        can = canfit(bits, p)
        c += int(can)
    return c


def part2(s):
    bits, patterns = parse(s)
    c = 0
    for p in patterns:
        can = numfit(bits, p)
        c += int(can)
    return c


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1")
    print(part1(ExampleInput1))

    print()
    print("Part 1")
    print(part1(real_input()))

    print()
    print("Example Part 2")
    print(part2(ExampleInput1))

    print()
    print("Part 2")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
