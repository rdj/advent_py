#!/usr/bin/env python3

from collections import deque
from functools import reduce


ExampleInput1 = """\
3,4,1,5
"""

ExamplesPart2 = (
    ("", "a2582a3a0e66e6e86e3812dcb672a272"),
    ("AoC 2017", "33efeb34ea91902bb2f59c9920caa6cd"),
    ("1,2,3", "3efbe78a8d82f29979031a4aa0b16a9d"),
    ("1,2,4", "63960835bcdc130f0b66d7ff4f6a5a8e"),
)

def parse1(s):
    return tuple(map(int, s.split(",")))


def run(inputs, start, rounds):
    a = deque(start)

    cur = 0
    skip = 0
    for _ in range(rounds):
        for n in inputs:
            b = deque()
            for _ in range(n):
                b.appendleft(a.popleft())
            a.extend(b)
            a.rotate(-skip)
            skip += 1

    # Restore the "original" order of the list, as though we did everything
    # in-place in an array
    a.rotate(rounds*sum(inputs) + (skip * (skip-1)) // 2)
    return list(a)


def part1(s, start=range(256)):
    a = run(parse1(s), start, 1)
    return a[0] * a[1]


def parse2(s):
    a = list(map(ord, s.strip()))
    return a + [17, 31, 73, 47, 23]


def part2(s):
    a = run(parse2(s), range(256), 64)

    blocks = []
    while a:
        chunk, a = a[:16], a[16:]
        blocks.append(reduce(lambda a, b: a ^ b, chunk))

    return "".join(f"{b:02x}" for b in blocks)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (12)")
    print(part1(ExampleInput1, start=range(5)))

    print()
    print("Part 1 (212)")
    print(part1(real_input()))
    print()

    for i, (s, x) in enumerate(ExamplesPart2):
        print(f"Example Part 2.{i+1}: ({x})")
        print(part2(s))
        print()

    print("Part 2 (96de9657665675b51cd03f0b3528ba26)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
