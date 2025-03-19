#!/usr/bin/env pypy3

from math import prod
import re

ExampleInput1 = """\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""

def parse(s):
    arr = []
    for line in s.splitlines():
        ints = list(map(int, re.findall(r"-?\d+", line)))
        arr.append((ints[1], ints[-1]))
    return tuple(arr)


########################################################################
## Extended Euclidean Algorithm (for Bézout coefficient)
## https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
def extended_gcd(a, b):
    (old_r, r) = (a, b)
    (old_s, s) = (1, 0)
    (old_t, t) = (0, 1)

    while r != 0:
       quotient = old_r // r
       (old_r, r) = (r, old_r - quotient * r)
       (old_s, s) = (s, old_s - quotient * s)
       (old_t, t) = (t, old_t - quotient * t)

    # gcd, x, y
    return old_r, old_s, old_t


########################################################################
## Multiplicative Inverse Mod (Modular Multiplicative Inverse)
## https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
def multiplicative_inverse_mod(n, modulus):
    _, x, _ = extended_gcd(n, modulus)
    return x % modulus


########################################################################
## Chinese Remainder Theorum
##
## Given pairs of coprime moduli and desired remainders, finds the smallest
## integer that simultaneously yields the desired remainders for all moduli.
##
## https://en.wikipedia.org/wiki/Chinese_remainder_theorem
## https://www.math.gordon.edu/ntic/ntic/section-using-crt.html
def chinese_remainer_theorum(moduli, remainders):
    target_mod = prod(moduli)
    complement_mods = [target_mod//mod for mod in moduli]
    inverses = [multiplicative_inverse_mod(comp, mod) for comp, mod in zip(complement_mods, moduli)]
    n = sum(prod(rem_comp_inv) for rem_comp_inv in zip(remainders, complement_mods, inverses)) % target_mod
    return n


# We have a set of discs with a distance (i+1), modulus (m) and start
# position (s).
#
# Notably, the moduli are all prime numbers.
#
# We want to choose a launch time (t0) so that the disc is at position 0
# when the ball arrives.
#
# The ball will arrive at t = t0 + (i+1).
#
# The disc position is given by (s + t) % m.
#
# So at the time of arrival: (s + t0 + i + 1) % m == 0.
#
# Rewriting, t0 % m == -(s + i + 1) % m
#
# There aren't very many discs, and who knows what part 2 is, but this is a
# straightforward application of the Chinese Remainder Theorum, which I
# already learned for a previous (future) Advent of Code (2020-13).
#
# Later: it turns out this was small enough brute force simluation would have
# been fine. Even back in 2016 when this problem written, redditors made the
# leaderboards with brute force. Several people chimed in about using Chinese
# Remainder Theorum via Mathematica (or pen and paper), and I sort of wonder of
# those comments gave the author the idea for the 2020 problem which was too
# big to brute force.
def solve(discs):
    moduli = []
    remainders = []
    for i, (m, s) in enumerate(discs):
        moduli.append(m)
        remainders.append(-(s + i + 1) % m)

    return chinese_remainer_theorum(moduli, remainders)


def part1(s):
    return solve(parse(s))


def part2(s):
    discs = parse(s)
    discs = discs + ((11, 0),)
    return solve(discs)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (5)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (16824)")
    print(part1(real_input()))

    print()
    print("Part 2 (3543984)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
