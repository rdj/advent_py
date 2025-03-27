#!/usr/bin/env pypy3

import re


MultiLineExample = """\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""

ExamplesPart1 = (
    (MultiLineExample, 1120),
)

ExamplesPart2 = (
    (MultiLineExample, 689),
)


def parse(s):
    return [[int(x) for x in re.findall(r"\d+", line)] for line in s.splitlines()]


def dist(e, t):
    v, tf, tr = e
    q, r = divmod(t, tf + tr)
    return q * v * tf + min(r, tf) * v


def part1(s, t=2503):
    return max(dist(_, t) for _ in parse(s))


def part2(s, t_end=2503):
    deer = parse(s)
    scores = [0] * len(deer)

    for t in range(1, t_end + 1):
        state = [dist(_, t) for _ in deer]
        leader = max(state)
        for i, d in enumerate(state):
            if d == leader:
                scores[i] += 1

    return max(scores)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1):
        c = part1(a, 1000)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 (2640)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a, 1000)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (1102)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
