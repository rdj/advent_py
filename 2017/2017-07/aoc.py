#!/usr/bin/env pypy3

from collections import defaultdict


ExampleInput1 = """\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
"""


def parse(s):
    kids = defaultdict(list)
    parents = {}
    weights = {}

    for line in s.splitlines():
        req, *opt = line.split(" -> ")

        name, weight = req.split()
        weight = int(weight[1:-1])

        weights[name] = weight

        if not opt:
            continue

        for kid in opt[0].split(", "):
            kids[name].append(kid)
            parents[kid] = name

    return kids, parents, weights


def bottom(kids, parents):
    return (set(kids.keys()) - set(parents.keys())).pop()


def part1(s):
    kids, parents, *_ = parse(s)
    return bottom(kids, parents)


def part2(s):
    kids, parents, weights = parse(s)
    root = bottom(kids, parents)

    # Caching this is not a net gain
    def subtotal(n):
        sub = weights[n]
        if n in kids:
            sub += sum(subtotal(k) for k in kids[n])
        return sub

    def balance(n, delta=None):
        d = defaultdict(list)
        for k in kids[n]:
            d[subtotal(k)] += [k]

        if len(d) < 2:
            return weights[n] + delta

        assert(len(d) == 2)
        for w, ns in d.items():
            if len(ns) == 1:
                badw = w
                bad = ns[0]
            else:
                goodw = w

        delta = goodw - badw
        return balance(bad, delta)

    return balance(root)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (tknk)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (qibuqqg)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (60)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (1079)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
