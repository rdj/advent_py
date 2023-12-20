#!/usr/bin/env python3

from colors import color
from collections import deque
from typing import NamedTuple
import math

ExampleInput1 = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

ExampleInput2 = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""


class Pulse(NamedTuple):
    src: str
    dst: str
    sig: int

    def __repr__(self):
        return f"{self.src} -{'high' if self.sig else 'low'}-> {self.dst}"


class PulseNetwork:
    def __init__(self, s):
        self.connections = {}
        self.flipflops = {}
        self.conjunctions = {}
        self.queue = deque()
        self.high_count = 0
        self.low_count = 0
        self.allon = []

        for line in s.splitlines():
            src, dst = line.split(' -> ')

            sym = None
            if src != 'broadcaster':
                sym = src[0]
                src = src[1:]
            dst = tuple(dst.split(', '))

            self.connections[src] = dst
            match sym:
                case '%':
                    self.flipflops[src] = False
                case '&':
                    self.conjunctions[src] = {}

        for src, dst in self.connections.items():
            for d in dst:
                if d in self.conjunctions:
                    self.conjunctions[d][src] = False

    def dispatch(self, p):
        if p.sig:
            self.high_count += 1
        else:
            self.low_count += 1

        if p.dst == 'broadcaster':
            for d in self.connections[p.dst]:
                self.queue.append(Pulse(p.dst, d, p.sig))
            return

        # % flip-flop, initially off, ignore high, low flips it; flipping on sends high, flipping off sends low
        if p.dst in self.flipflops:
            if p.sig:
                return
            sig = not self.flipflops[p.dst]
            self.flipflops[p.dst] = sig
            for d in self.connections[p.dst]:
                self.queue.append(Pulse(p.dst, d, sig))
            return

        # & conjunction, remembers most recent pulse from each connected input (default low); on receive, update memory, if pulses high for all inputs, send low; else send high
        if p.dst in self.conjunctions:
            self.conjunctions[p.dst][p.src] = p.sig
            sig = not all(self.conjunctions[p.dst].values())
            if not sig and p.dst not in self.allon:
                self.allon.append(p.dst)
            for d in self.connections[p.dst]:
                self.queue.append(Pulse(p.dst, d, sig))
            return

        # Note: there are "untyped outputs"

    def run_until_empty(self):
        while self.queue:
            self.dispatch(self.queue.popleft())

    def push_button(self):
        assert 0 == len(self.queue)
        self.queue.append(Pulse('button', 'broadcaster', False))
        self.run_until_empty()

    def state(self):
        return tuple(self.flipflops.values())


def part1(s):
    pn = PulseNetwork(s)
    for _ in range(1000):
        pn.push_button()
    return pn.high_count * pn.low_count


def part2(s):
    pn = PulseNetwork(s)
    allon = []
    cycles = []

    n = 0
    while True:
        n += 1
        pn.push_button()
        if pn.allon != allon:
            allon = pn.allon.copy()
            cycles.append(n)
            # all of the conjunctions eventually feed into one, which is the
            # one we're trying to trigger. we're not going to find it's cycle.
            # we could analyze the graph, but I'm going to be lazy and just
            # wait until I find the other n - 1 cycles.
            if len(allon) + 1 == len(pn.conjunctions):
                break

    return math.lcm(*cycles)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (32000000)")
    print(part1(ExampleInput1))

    print()
    print("Example 2 Part 1 (11687500)")
    print(part1(ExampleInput2))

    print()
    print("Part 1 (899848294)")
    print(part1(real_input()))

    print()
    print("Part 2 (247454898168563)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
