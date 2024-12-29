#!/usr/bin/env python3

from functools import cmp_to_key
from collections import defaultdict


ExampleInput1 = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def parse(s):
    r, u = s.split("\n\n")
    r = [_.split("|") for _ in r.splitlines()];
    u = [_.split(",") for _ in u.splitlines()];
    return r, u


def build_must_preceed(rules):
    must_preceed = defaultdict(list)
    for [a, b] in rules:
        must_preceed[a].append(b)
    return must_preceed


def is_good(update, must_preceed):
    seen = []
    for n in update:
        if any(_ in seen for _ in must_preceed[n]):
            return False
        seen.append(n)
    return True


def mid(u):
    if len(u) % 2 == 0:
        raise Exception(f"No middle value for list: #{u}")
    return int(u[len(u)//2])


def part1(s):
    rules, updates = parse(s)
    must_preceed = build_must_preceed(rules)
    return sum(mid(u) for u in updates if is_good(u, must_preceed))


def preceed_cmp(must_preceed):
    def curried_cmp(a, b):
        if a in must_preceed[b]:
            return 1
        if b in must_preceed[a]:
            return -1
        return 0
    return curried_cmp


def fix(u, must_preceed):
    return sorted(u, key=cmp_to_key(preceed_cmp(must_preceed)))


def part2(s):
    rules, updates = parse(s)
    must_preceed = build_must_preceed(rules)
    return sum(mid(fix(u, must_preceed)) for u in updates if not is_good(u, must_preceed))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (143)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (4996)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (123)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (6311)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
