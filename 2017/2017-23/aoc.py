#!/usr/bin/env pypy3

from itertools import count


def parse(s):
    return int(s.splitlines()[0].split()[-1])


def part1(s):
    b = parse(s)
    return (b - 2) * (b - 2)


def isprime(n):
    for x in count(2):
        if x*x > n:
            return True
        if n % x == 0:
            return False


def part2(s):
    b = parse(s)
    b = b * 100 + 100_000
    c = b + 17_000

    return sum(1 for n in range(b, c+1, 17) if not isprime(n))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Part 1 (3969)")
    print(part1(real_input()))

    print()
    print("Part 2 (917)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
