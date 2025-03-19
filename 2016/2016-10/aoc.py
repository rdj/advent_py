#!/usr/bin/env pypy3

import re
from math import prod


ExampleInput1 = """\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
"""

MAXBOTS = 255
GETS = re.compile("value (\d+) goes to bot (\d+)")
GIVES = re.compile("bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)")


class Part1Exception(Exception):
    def __init__(self, i):
        self.i = i


class Botnet:
    def __init__(self, part1=None):
        self.bots = [None] * MAXBOTS
        self.rules = [None] * MAXBOTS
        self.outputs = [None] * MAXBOTS
        self.part1 = part1

    def run(self, lines):
        for line in lines.splitlines():
            if m := GIVES.match(line):
                i, dstlow, ilow, dsthigh, ihigh = m.groups()
                i = int(i)
                if self.rules[i] is not None:
                    raise Exception(f"Rule redefinition for bot {i}")
                self.rules[i] = (dstlow, int(ilow), dsthigh, int(ihigh))

        for line in lines.splitlines():
            if m := GETS.match(line):
                v, i = map(int, m.groups())
                self.gets(i, v)


    def gets(self, i, v, dst="bot"):
        if dst == "output":
            self.outputs[i] = v
            return

        if self.bots[i] is None:
            self.bots[i] = v
            return

        if self.part1 == sorted([v, self.bots[i]]):
            raise Part1Exception(i)

        if self.rules[i] is None:
            raise Exception(f"Got a second value for bot {i} but no rule")

        dstlow, ilow, dsthigh, ihigh = self.rules[i]
        vlow, vhigh = sorted([v, self.bots[i]])
        self.bots[i] = None

        self.gets(ilow, vlow, dstlow)
        self.gets(ihigh, vhigh, dsthigh)


def part1(s, want=[17, 61]):
    botnet = Botnet(part1=want)
    try:
        botnet.run(s)
    except Part1Exception as e:
        return e.i


def part2(s):
    botnet = Botnet()
    botnet.run(s)
    return prod(botnet.outputs[:3])


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (2)")
    print(part1(ExampleInput1, want=[2, 5]))

    print()
    print("Part 1 (113)")
    print(part1(real_input()))

    print()
    print("Part 2 (12803)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
