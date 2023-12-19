#!/usr/bin/env python3

from colors import color
from math import prod


ExampleInput1 = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


class Workflows:
    def __init__(self, s):
        self.flows = {}
        self.accepted = []
        self.rejected = []
        for line in s.splitlines():
            if line == "":
                break
            name, rest = line.split('{')
            rest = rest[:-1]
            rest = rest.split(',')
            self.flows[name] = rest

    def is_accepted(self, p):
        return self.run(p, 'in') == 'A'

    def run(self, p, name):
        if name in ('A', 'R'):
            return name
        for step in self.flows[name]:
            if not ':' in step:
                return self.run(p, step)

            step, out = step.split(':')

            var = step[0]
            op = step[1]
            num = int(step[2:])

            result = (p[var] < num if op == '<' else p[var] > num)
            if result:
                return self.run(p, out)
        raise Exception("Ran out of steps")

    def part2(self):
        xmas = {k: (0, 4001) for k in 'xmas'}
        ranges = self.find_accepted_ranges(xmas, 'in')
        return sum(count_xmas(_) for _ in self.accepted)

    def find_accepted_ranges(self, xmas, name):
        if name == 'A':
            self.accepted.append(xmas)
            return
        if name == 'R':
            self.rejected.append(xmas)
            return

        for step in self.flows[name]:
            if not ':' in step:
                self.find_accepted_ranges(xmas, step)
                return

            step, out = step.split(':')

            var = step[0]
            op = step[1]
            num = int(step[2:])

            inrange = xmas[var]
            assert(inrange[0] <= num <= inrange[1])

            xmas2 = xmas.copy()
            if op == '<':
                xmas2[var] = (inrange[0], num)
                xmas[var] = (num - 1, inrange[1])
            else:
                xmas2[var] = (num, inrange[1])
                xmas[var] = (inrange[0], num + 1)

            assert rangelen(inrange) == rangelen(xmas2[var]) + rangelen(xmas[var])

            self.find_accepted_ranges(xmas2, out)

        raise Exception("Did not accept or reject")


def rangelen(r):
    return r[1] - r[0] - 1


def count_xmas(xmas):
    return prod(rangelen(r) for r in xmas.values())


def parse_parts(s):
    _, partstr = s.split("\n\n")
    parts = []
    for line in partstr.splitlines():
        d = {}
        for pair in line[1:-1].split(','):
            n, v = pair.split('=')
            d[n] = int(v)
        parts.append(d)
    return parts


def part1(s):
    flows = Workflows(s)
    parts = parse_parts(s)

    good = [p for p in parts if flows.is_accepted(p)]

    total = 0
    for p in good:
        total += sum(p.values())
    return total


def part2(s):
    return Workflows(s).part2()


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (19114)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (350678)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (167409079868000)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (124831893423809)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
