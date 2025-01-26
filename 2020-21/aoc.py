#!/usr/bin/env pypy3

from collections import Counter
from functools import reduce
import re
import operator as op


ExampleInput1 = """\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""


def parse(s):
    d = {}
    counts = Counter()

    for line in s.splitlines():
        ings, algs = line.split(" (contains ")
        ings = ings.split()
        counts.update(ings)
        algs = re.sub(r"[^\w\s]", "", algs)
        for alg in algs.split():
            if alg in d:
                d[alg] &= set(ings)
            else:
                d[alg] = set(ings)

    return d, counts


def part1(s):
    d, counts = parse(s)
    safe = counts.keys() - reduce(op.or_, d.values())
    return sum(counts[s] for s in safe)


def part2(s):
    d, _ = parse(s)
    result = []

    while d:
        for alg, ings in d.items():
            if len(ings) == 1:
                break
        ing = ings.pop()
        result += [(alg, ing)]
        del d[alg]
        for s in d.values():
            if ing in s:
                s.remove(ing)

    return ",".join([ing for _, ing in sorted(result)])


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (5)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (2461)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (mxmxvkd,sqjhc,fvjkl)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (ltbj,nrfmm,pvhcsn,jxbnb,chpdjkf,jtqt,zzkq,jqnhd)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
