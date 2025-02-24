#!/usr/bin/env pypy3

from collections import deque


ExampleInput1 = """\
3
"""


def parse(s):
    return int(s.strip())


# This feels like a number theory problem but last time I thought that it was
# really a simulation problem, so I guess we start with simulation
def part1(s):
    step = parse(s)

    d = deque([0])
    for n in range(1, 2018):
       d.rotate(-step-1)
       d.appendleft(n)

    return d[1]


# They made it too big to simulate but now we are watching a fixed location
# (after 0), so we can just compute each step and only keep track of values
# that land in that location, completely ignoring the rest of the structure.
def part2(s):
    step = parse(s)

    oneth = None

    pos = 0
    for n in range(1, 50_000_001):
        pos = (pos + step) % n + 1
        if pos == 1:
            oneth = n

    return oneth


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (638)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (777)")
    print(part1(real_input()))

    print()
    print("Part 2")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
