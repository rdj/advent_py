#!/usr/bin/env python3


def ones(s):
    return (1 if c == "(" else -1 for c in s.strip())


def part1(s):
    return sum(ones(s))


def part2(s):
    running = 0
    for i, one in enumerate(ones(s)):
        running += one
        if running == -1:
            return i + 1



def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Part 1 (280)")
    print(part1(real_input()))

    print()
    print("Part 2 (1797)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
