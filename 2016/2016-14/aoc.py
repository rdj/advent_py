#!/usr/bin/env pypy3

import _md5
import re
from collections import defaultdict
from itertools import count


ExampleInput1 = """\
abc
"""


def md5(s, rounds):
    for _ in range(rounds):
        s = _md5.md5(bytes(s, "ascii"), usedforsecurity=False).hexdigest()
    return s


def part1(s, rounds=1):
    keys = 0
    candidates = defaultdict(list)

    salt = s.strip()
    for i in count():
        h = md5(salt + str(i), rounds)

        for p, jlist in list(candidates.items()):
            jlist = [j for j in jlist if i - j <= 1000]
            candidates[p] = jlist
            if len(jlist) == 0:
                continue

            if p in h:
                candidates[p] = []

                for j in jlist:
                    keys += 1
                    #print(f"{i}: Validates key {j} using {p}")
                    if keys == 64:
                        return j

        if m := re.search(r"(.)\1\1", h):
            ch, = m.groups()
            #print(f"{i}: {ch} candidate: {h}")
            candidates[ch * 5] += [i]


def part2(s):
    return part1(s, rounds=2017)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (22728)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (16106)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (22551)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (22423)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
