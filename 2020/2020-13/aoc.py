#!/usr/bin/env pypy3

from math import prod


ExampleInput1 = """\
939
7,13,x,x,59,x,31,19
"""

MoreExamples = (
    ("17,x,13,19", 3417),
    ("67,7,59,61", 754018),
    ("67,x,7,59,61", 779210),
    ("67,7,x,59,61", 1261476),
    ("1789,37,47,1889", 1202161486)
)

def parse(s):
    lines = s.splitlines()
    ts = int(lines[0])
    buses = lines[1].split(",")
    buses = [int(n) if n != 'x' else 'x' for n in buses]
    return ts, buses


def part1(s):
    ts, buses = parse(s)

    def wait_time(n):
        m = (ts - 1) // n
        return (n * (m + 1) - ts, n)

    return prod(min(wait_time(n) for n in buses if n != 'x'))


# It's time for our old friend the Extended Euclidean Algorithm for computing
# GCD and Bézout coefficients. Last time I needed this I was using rust, which
# has it built-in, but apparently I have to write it myself in python.
#
# This is directly from https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
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


def multiplicative_inverse_mod(n, modulus):
    _, x, _ = extended_gcd(n, modulus)
    return x % modulus


# I thought Z3 would just be able to satisfy the straightforward set of
# constraints, but it just sits and spins forever.
#
# The set of constraints is of the form:
#
#     t % n == n - i
#
# Where t is the timestamp we're looking for, n is the bus number, and i is the
# bus's position in the list. If we have a gander at our input, the bus numbers
# are:
#
#     17,41,983,29,19,23,397,37,13
#
# Looks suspicious, how about the example inputs:
#
#    17,13,19
#    67,7,59,61
#    1789,37,47,1889
#
# All prime numbers. So there's clearly some crazy number theory thing going on
# here, and some googling reveals that what we're looking for is probably:
#
#     https://en.wikipedia.org/wiki/Chinese_remainder_theorem
#
# The explanation there for how to apply it is very hard to follow. Here is
# textbook with a concrete example in Sage:
#
#     https://www.math.gordon.edu/ntic/ntic/section-using-crt.html
#
# In their example x % 5 == 1, x % 6 == 2, x % 7 == 3. To find x:
#
#     n = [5, 6, 7]               # the moduli
#     a = [1, 2, 3]               # the remainders
#     N = prod(n)                 # the target modulus
#     c = [N//ni for ni in n]     # the complement moduli
#     d = [multiplicative_inverse_mod(ci, ni) for ci, ni in zip(c, n)]
#     x = sum(prod(acd) for acd in zip(a, c, d)) % N
#
def part2(s):
    _, buses = parse(s)

    moduli = []
    remainders = []
    for i, mod in enumerate(buses):
        if mod == 'x':
            continue
        moduli.append(mod)
        # Big gotcha is that the minute we want the bus to leave after the
        # target timestamp is the *negative* remainder
        remainders.append(-i)

    target_mod = prod(moduli)
    complement_mods = [target_mod//mod for mod in moduli]
    inverses = [multiplicative_inverse_mod(comp, mod) for comp, mod in zip(complement_mods, moduli)]
    t = sum(prod(rem_comp_inv) for rem_comp_inv in zip(remainders, complement_mods, inverses)) % target_mod
    return t


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (295)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (2382)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (1068781)")
    print(part2(ExampleInput1))

    for i, (s, a) in enumerate(MoreExamples):
        print()
        print(f"Example Part 2.{i} ({a})")
        print(part2("0\n" + s))

    print()
    print("Part 2 (906332393333683)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
