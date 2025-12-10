#!/usr/bin/env python3

from heapq import heappush, heappop
import re
import z3


MultiLineExample = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""

ExamplesPart1 = (
    (MultiLineExample, 7),
)

ExamplesPart2 = (
    (MultiLineExample, 33),
)


def parse(s):
    spec = []
    for line in s.splitlines():
        m = re.search(r'^\[(.*?)\] (\(.*\)) \{(.*)\}$', line)
        g = m.groups()
        dst = tuple(c=='#' for c in g[0])

        buttons = []
        for bs in g[1].split():
            buttons.append(tuple(map(int, bs[1:-1].split(','))))

        jolts = tuple(map(int, g[2].split(',')))

        spec.append((dst,tuple(buttons), jolts))
    return spec


def solve1(p):
    dst, buttons, _ = p

    visited = set()

    q = []
    heappush(q, (0, tuple([False] * len(dst))))

    while q:
        cost, state = heappop(q)

        if state in visited:
            continue
        visited.add(state)

        if state == dst:
            return cost

        for b in buttons:
            nstate = list(state)
            for i in b:
                nstate[i] = not nstate[i]

            nstate = tuple(nstate)
            ncost = cost + 1

            if nstate in visited:
                continue
            heappush(q, (ncost, nstate))

    raise Exception("No solution found")


def part1(s):
    return sum(solve1(p) for p in parse(s))


def solve2(p):
    _, buttons, jolts = p

    opt = z3.Optimize()

    zvars = []
    for i in range(len(buttons)):
        v = z3.Int(chr(ord('a') + i))
        zvars.append(v)
        opt.add(v >= 0)

    for i in range(len(jolts)):
        evars = []
        for j in range(len(buttons)):
            if i in buttons[j]:
                evars.append(zvars[j])
        opt.add(jolts[i] == sum(evars))

    opt.minimize(sum(zvars))
    if opt.check() == z3.sat:
        m = opt.model()
        return sum(m[v].as_long() for v in zvars)

    raise Exception("unsat")


def part2(s):
    return sum(solve2(p) for p in parse(s))


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

    print("Part 1 (488)")
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

    print("Part 2 (18771)")
    before = time.perf_counter_ns()
    result = part2(real_input())
    elapsed = time.perf_counter_ns() - before
    print(f"{result} ({elapsed//1_000_000} ms)")


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('part2(real_input())', sort="cumulative")
    run_all()
