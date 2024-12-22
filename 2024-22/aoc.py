#!/usr/bin/env pypy3

from collections import Counter
from itertools import product
from more_itertools import sliding_window


PRUNE_MODULUS = 16777216


ExampleInput1 = """\
1
10
100
2024
"""

ExampleInput2 = """\
1
2
3
2024
"""


def next_secret(n):
    a = n * 64

    n ^= a
    n %= PRUNE_MODULUS

    b = n // 32
    n ^= b
    n %= PRUNE_MODULUS

    c = n * 2048
    n ^= c
    n %= PRUNE_MODULUS

    return n


def nth_secret(a, n):
    for _ in range(n):
        a = next_secret(a)
    return a


def first_n_secrets_mod10(a, n):
    r = [a % 10]
    for _ in range(n):
        a = next_secret(a)
        r.append(a % 10)
    return tuple(r)


def compute_deltas(nums):
    deltas = []
    for a, b in sliding_window(nums, 2):
        deltas.append(b - a)
    return tuple(deltas)


def index_of_subseq(seq, want):
    for i, sub in enumerate(sliding_window(seq, len(want))):
        if sub == want:
            return i
    return None


def part1(s):
    return sum(nth_secret(int(line), 2000) for line in s.splitlines())


def all_code_results(bids, deltas):
    r = {}

    for i, code in enumerate(sliding_window(deltas, 4)):
        if code not in r:
            r[code] = bids[i+4]

    return r


def part2(s):
    seeds = tuple(map(int, s.splitlines()))
    bids = tuple(map(lambda s: first_n_secrets_mod10(s, 2000), seeds))
    deltas = tuple(map(compute_deltas, bids))

    everything = Counter()
    for i in range(len(bids)):
        everything += all_code_results(bids[i], deltas[i])

    return max(everything.values())


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (37327623)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (12759339434)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (23)")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (1405)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
