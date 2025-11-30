#!/usr/bin/env python3

from collections import defaultdict
from enum import IntEnum, auto


ExampleInput1 = """\
..#
#..
...
"""


class State(IntEnum):
    Clean = 0
    Weakened = auto()
    Infected = auto()
    Flagged = auto()


def parse(s):
    lines = s.splitlines()
    start = (len(lines[0])//2, len(lines)//2)
    infected = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                infected.add((x, y))
    return infected, start


def part1(s):
    infected, (x, y) = parse(s)
    dx, dy = 0, -1
    infections = 0

    for _ in range(10_000):
        if (x, y) in infected:
            dx, dy = -dy, dx
            infected.remove((x, y))
        else:
            dx, dy = dy, -dx
            infected.add((x, y))
            infections += 1
        x += dx
        y += dy

    return infections


def part2(s):
    infected, (x, y) = parse(s)
    dx, dy = 0, -1
    infections = 0

    state = defaultdict(lambda: State.Clean, {k: State.Infected for k in infected})

    for _ in range(10_000_000):
        match s := state[(x, y)]:
            case State.Clean:
                dx, dy = dy, -dx

            case State.Weakened:
                infections += 1
                pass

            case State.Infected:
                dx, dy = -dy, dx

            case State.Flagged:
                dx, dy = -dx, -dy

        state[(x, y)] = State((s + 1) % len(State))
        x += dx
        y += dy

    return infections


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (5587)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (5322)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (2511944)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (2512079)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
