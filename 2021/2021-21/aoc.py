#!/usr/bin/env pypy3

from collections import Counter
from itertools import cycle, islice, product


ExampleInput1 = """\
Player 1 starting position: 4
Player 2 starting position: 8
"""

def parse(s):
    return tuple(int(line.split(": ")[-1]) - 1 for line in s.splitlines())

def part1(s):
    rollcount = 0
    pos = list(parse(s))
    score = [0, 0]
    die = cycle(range(1,101))
    p = 0

    while True:
        turn = sum(islice(die, 3))
        rollcount += 3

        pos[p] = (pos[p] + turn) % 10
        score[p] += pos[p] + 1
        if score[p] >= 1000:
            break
        p = int(not p)

    return min(score) * rollcount


def part2(s):
    die = (1, 2, 3)
    turnfreq = tuple(Counter(sum(roll) for roll in product(*(die,)*3)).items())

    # state = (pos, score)
    states = Counter([(parse(s), (0, 0))])

    wins = [0, 0]
    p = 0
    while states:
        newstates = Counter()
        for (pos0, score0), n0 in states.items():
            for turn, freq in turnfreq:
                n = n0 * freq
                pos = list(pos0)
                score = list(score0)
                pos[p] = (pos[p] + turn) % 10
                score[p] += pos[p] + 1
                if score[p] >= 21:
                    wins[p] += n
                else:
                    newstates[(tuple(pos), tuple(score))] += n
        states = newstates
        p = int(not p)

    return max(wins)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (739785)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (711480)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (444356092776315)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (265845890886828)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
