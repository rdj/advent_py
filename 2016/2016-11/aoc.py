#!/usr/bin/env pypy3

import re

from collections import defaultdict
from heapq import heappush, heappop
from itertools import count


ExampleInput1 = """\
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
"""


def parse(s):
    counter = count()

    d = defaultdict(lambda: next(counter))
    chips = [None] * 32
    gens = [None] * 32

    for i, line in enumerate(s.splitlines()):
        for m in re.finditer(r"(\w+)-compatible microchip", line):
            name, = m.groups()
            chips[d[name]] = i
        for m in re.finditer(r"(\w+) generator", line):
            name, = m.groups()
            gens[d[name]] = i

    n = next(counter)
    return (*chips[:n], *gens[:n])


# Rules are:
#  elevator
#   - must move one floor up/down per step
#   - must not be empty
#   - can hold 1-2 items
#  microchips are fried if exposed to non-matching generators

def is_valid(stuff):
    N = len(stuff)//2
    chips, gens = stuff[:N], stuff[N:]

    for i in range(len(chips)):
        if chips[i] == gens[i]:
            # Safe, paired with its generator
            continue
        if any(g == chips[i] for g in gens):
            # Fried, non-matching generator is here
            return False
    return True


def next_states(state):
    src, start = state

    for dst in (src - 1, src + 1):
        if dst < 0 or dst > 3:
            continue
        downward = src > dst
        upward = not downward

        if min(start) > dst:
            continue

        for i in range(len(start)):
            if start[i] == src:
                imv = start[:i] + (dst,) + start[i+1:]
                if downward and is_valid(imv):
                    yield (dst, imv)
                    continue

                moved_two = False
                for j in range(i + 1, len(start)):
                    if start[j] == src:
                        jmv = imv[:j] + (dst,) + imv[j+1:]
                        if is_valid(jmv):
                            yield (dst, jmv)
                            moved_two = True
                if upward and not moved_two and is_valid(imv):
                    yield (dst, imv)


# Chip/Generator pairs are interchangeable, so collapse all equivalent states
# when pruning
def keyify(state):
    el, state = state
    N = len(state)//2
    key = (el, tuple(sorted([(state[i], state[N+i]) for i in range(N)])))
    return key


def solve(init):
    END = (3, (3,) * len(init))

    q = []
    heappush(q, (0, (0, init)))

    visited = set()

    while q:
        steps, state = heappop(q)
        key = keyify(state)

        if key in visited:
            continue
        visited.add(key)

        if state == END:
            return steps

        for b in next_states(state):
            if keyify(b) not in visited:
                heappush(q, (steps + 1, b))

    return "NO SOLUTION FOUND"


def part1(s):
    init = parse(s)
    return solve(init)


def part2(s):
    init = parse(s)
    N = len(init)//2
    chips, gens = init[:N], init[N:]
    chips += (0, 0)
    gens += (0, 0)
    return solve(chips + gens)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (11)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (31)")
    print(part1(real_input()))

    print()
    print("Part 2 (55)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
