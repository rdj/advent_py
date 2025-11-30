#!/usr/bin/env python3

from functools import cache


ExampleInput1 = """\
125 17
"""


def parse(s):
    return [int(_) for _ in s.splitlines()[0].split()]


# Naive implementation, works for part 1
def transform(state):
    xstate = []
    for n in state:
        if n == 0:
            xstate.append(1)
            continue

        ns = str(n)
        nsl = len(ns)
        if nsl % 2 == 0:
            xstate.append(int(ns[:nsl//2]))
            xstate.append(int(ns[nsl//2:]))
            continue

        xstate.append(2024 * n)
    return xstate


def part1(s):
    # state = parse(s)
    # for _ in range(25):
    #     state = transform(state)
    # return len(state)
    return sum(count_splits(n, 25) for n in parse(s))


@cache
def count_splits(n, iters):
    if iters == 0:
        return 1

    if n == 0:
        return count_splits(1, iters - 1)

    ns = str(n)
    nsl = len(ns)
    if nsl % 2 == 0:
        return (
            count_splits(int(ns[:nsl//2]), iters - 1) +
            count_splits(int(ns[nsl//2:]), iters - 1)
        )

    return count_splits(2024 * n, iters - 1)


def part2(s):
    return sum(count_splits(x, 75) for x in parse(s))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (55312)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (200446)")
    print(part1(real_input()))

    print()
    print("Part 2 (238317474993392)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
