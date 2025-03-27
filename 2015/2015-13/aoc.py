#!/usr/bin/env pypy3

from collections import defaultdict
from itertools import permutations


MultiLineExample = """\
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""


ExamplesPart1 = (
    (MultiLineExample, 330),
)


def parse(s):
    d = {}
    for line in s.splitlines():
        toks = line.split()
        a = toks[0]
        sign = 1 if toks[2] == "gain" else -1
        delta = int(toks[3]) * sign
        b = toks[-1][:-1]
        d[(a, b)] = delta
    return d


def score(spec, p):
    p = p + (p[0],)
    pairs = zip(p, p[1:])

    total = 0
    for a, b in pairs:
        total += spec[(a, b)]
        total += spec[(b, a)]

    return total


def part1(s):
    spec = parse(s)
    names = set(k[0] for k in spec.keys())

    # Permutations are equivalent under rotation and reflection; not sure if we
    # need to bother optimizing or not. Later: Nope.
    return max(score(spec, p) for p in permutations(names))


def part2(s):
    spec = parse(s)
    names = set(k[0] for k in spec.keys())

    spec = defaultdict(int, spec)
    names.add("Myself")

    return max(score(spec, p) for p in permutations(names))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1):
        c = part1(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 (709)")
    print(part1(real_input()))
    print()

    print("Part 2 (668)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
