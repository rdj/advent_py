#!/usr/bin/env pypy3

import re


def parse(s):
    return tuple(map(int, re.findall(r"\d+", s)))


def part1(s):
    tr, tc = parse(s)

    # Use 0-indexing for everything, unlike the the problem text. So the top
    # left corner is 0,0 and it hosts the n=0 value of the sequence.
    tr -= 1
    tc -= 1

    dr = tr + tc
    drn = dr * (dr + 1) // 2
    n = drn + tc

    BASE = 252533
    EXP = 33554393
    return (20151125 * pow(BASE, n, EXP)) % EXP


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Part 1 (8997277)")
    print(part1(real_input()))


if __name__ == "__main__":
    run_all()
