#!/usr/bin/env pypy3

from more_itertools import chunked


ExampleInput1 = """\
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
"""


import re


def parse(s):
    s = re.sub(r"^ *I[nf].*?\n", "", s, flags=re.MULTILINE)
    s = re.sub(r" steps", "", s)
    s = re.sub(r"^.*?(\S+)\S$", r"\1", s, flags=re.MULTILINE)
    s = re.sub(r"right", "1", s)
    s = re.sub(r"left", "-1", s)
    s = re.sub("[A-Z]", lambda m: str(ord(m[0]) - ord("A")), s)

    blocks = [list(map(int, block)) for block in map(str.splitlines, s.split("\n\n"))]
    intro, *blocks = blocks

    start, steps = intro
    states = [list(chunked(block, 3)) for block in blocks]

    return start, steps, states


def part1(s):
    start, steps, states = parse(s)

    tape = [0] * (steps * 2 + 1)
    pos = len(tape)//2 + 1
    state = states[0]

    for _ in range(steps):
        v, m, s =  state[tape[pos]]
        tape[pos] = v
        pos += m
        state = states[s]

    return sum(tape)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (3)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (4230)")
    print(part1(real_input()))


if __name__ == "__main__":
    run_all()
