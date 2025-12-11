#!/usr/bin/env python3

from functools import cache
import re


MultiLineExample = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

ExamplesPart1 = (
    (MultiLineExample, 5),
)


MultiLineExample2 = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""

ExamplesPart2 = (
    (MultiLineExample2, 2),
)


class Graph:
    def __init__(self, s):
        self.parse(s)

    def parse(self, s):
        self.spec = {}

        for line in s.splitlines():
            src, dsts = line.split(": ")
            self.spec[src] = dsts.split()

    @cache
    def path_count(self, src, dst):
        if src == dst:
            return 1

        nodes = self.spec[src] if src in self.spec else None
        if not nodes:
            return 0

        return sum(self.path_count(n, dst) for n in nodes)


def part1(s):
    return Graph(s).path_count('you', 'out')


def part2(s):
    G = Graph(s)
    G_no_dac = Graph(re.sub(r'^dac:.*?$', '', s))
    G_no_fft = Graph(re.sub(r'^fft:.*?$', '', s))

    svr_to_dac = G_no_fft.path_count('svr', 'dac')
    dac_to_fft = G.path_count('dac', 'fft')
    fft_to_out = G_no_dac.path_count('fft', 'out')

    svr_to_fft = G_no_dac.path_count('svr', 'fft')
    fft_to_dac = G.path_count('fft', 'dac')
    dac_to_out = G_no_fft.path_count('dac', 'out')

    return svr_to_dac * dac_to_fft * fft_to_out + svr_to_fft * fft_to_dac * dac_to_out


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    import time

    for i, (a, b) in enumerate(ExamplesPart1):
        c = part1(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 (746)")
    before = time.perf_counter_ns()
    result = part1(real_input())
    elapsed = time.perf_counter_ns() - before
    print(f"{result} ({elapsed//1_000_000} ms)")
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (370500293582760)")
    before = time.perf_counter_ns()
    result = part2(real_input())
    elapsed = time.perf_counter_ns() - before
    print(f"{result} ({elapsed//1_000_000} ms)")


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('part2(real_input())', sort="cumulative")
    run_all()
