#!/usr/bin/env python3

from collections import Counter
from enum import Enum

ExampleInput1 = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".strip()


CARD_RANKS = '23456789TJQKA'
CARD_RANKS_JOKER = 'J23456789TQKA'

HandRank = Enum('HandRank', ['HIGH_CARD', 'ONE_PAIR', 'TWO_PAIR', 'THREE_OF_A_KIND', 'FULL_HOUSE', 'FOUR_OF_A_KIND', 'FIVE_OF_A_KIND'])


def score_hand(hand, jokers=False):
    counts = Counter(hand)

    joker_count = 0
    if jokers:
        joker_count = counts['J']
        del counts['J']

    counts = list(reversed(sorted(counts.values())))
    if len(counts) == 0:
        # There's a hand with all jokers!
        counts = [joker_count]
    else:
        counts[0] += joker_count

    if counts[0] == 5:
        return HandRank.FIVE_OF_A_KIND
    if counts[0] == 4:
        return HandRank.FOUR_OF_A_KIND
    if counts == [3, 2]:
        return HandRank.FULL_HOUSE
    if counts[0] == 3:
        return HandRank.THREE_OF_A_KIND
    if counts == [2, 2, 1]:
        return HandRank.TWO_PAIR
    if counts[0] == 2:
        return HandRank.ONE_PAIR
    return HandRank.HIGH_CARD


def hand_sort_key(hand, jokers=False):
    card_ranks = CARD_RANKS
    if jokers:
        card_ranks = CARD_RANKS_JOKER

    score = score_hand(hand, jokers)
    key = [score.value]
    for c in hand:
        key.append(card_ranks.index(c))
    return tuple(key)


def parse(s):
    entries = []
    for line in s.splitlines():
        hand, bid = line.split()
        entries.append((hand, int(bid)))
    return entries


def get_total(s, jokers=False):
    entries = parse(s)
    entries.sort(key=lambda e:hand_sort_key(e[0], jokers))

    answer = 0
    for n, (hand, bid) in enumerate(entries):
        rank = n + 1
        answer += rank * bid
    return answer


def part1(s):
    return get_total(s)


def part2(s):
    return get_total(s, jokers=True)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read().strip()


def run_all():
    print("Example Part 1 (6440)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (248179786)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (5905)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (247885995)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
