#!/usr/bin/env python3

from collections import defaultdict

ExampleInput1 = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".strip()


def wincount(s):
    card, rest = s.split(': ')
    winstr, mystr = rest.split('|')
    winners = set([int(n) for n in winstr.split()])
    mine = set([int(n) for n in mystr.split()])
    return len(winners & mine)


def part1(s):
    score = 0

    for line in s.splitlines():
        wins = wincount(line)
        if wins > 0:
            score += 2**(wins - 1)

    return score


def part2(s):
    counts = defaultdict(lambda: 1)

    for i, line in enumerate(s.splitlines()):
        wins = wincount(line)
        mycount = counts[i]
        for n in range(wins):
            counts[i+n+1] += mycount

    return sum(counts.values())


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read().strip()


def run_all():
    print("Example Part 1 (13)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (17782)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (30)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (8477787)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
