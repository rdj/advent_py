#!/usr/bin/env python3


from math import prod


ExampleInput1 = """\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""


def parse(s):
    s_rules, s_my, s_nearby = s.split("\n\n")

    rules = []
    for line in s_rules.splitlines():
        name, s_ranges = line.split(": ")
        s_ranges = s_ranges.split(" or ")
        s_ranges = [list(map(int, r.split("-"))) for r in s_ranges]
        ranges = tuple(range(r[0], r[1]+1) for r in s_ranges)
        rules.append(tuple([name, *ranges]))

    my = tuple(map(int, s_my.splitlines()[-1].split(",")))

    nearby = tuple(tuple(map(int, line.split(","))) for line in s_nearby.splitlines()[1:])

    return rules, my, nearby


def part1(s):
    rules, _, nearby = parse(s)
    ranges = [r for rule in rules for r in rule[1:]]
    return sum(f for t in nearby for f in t if not any(f in r for r in ranges))


def part2(s):
    rules, my, nearby = parse(s)
    assert(len(rules) == len(my))

    # Filter out tickets with values that match no rule
    allranges = [r for rule in rules for r in rule[1:]]
    tickets = [t for t in (my, *nearby) if all(any(n in r for r in allranges) for n in t)]

    # For each field index, keep track of which rules have been violated
    fi_valid_for_ri = []
    for _ in range(len(tickets[0])):
        fi_valid_for_ri.append([True] * len(rules))

    for t in tickets:
        for fi, f in enumerate(t):
            for ri, r in enumerate(rules):
                if not any(f in _ for _ in r[1:]):
                    fi_valid_for_ri[fi][ri] = False

    # Find which field indices map to which rule indices by repeatedly finding
    # a field that violates all but one rule, mapping it, then eliminating that
    # rule for all other field positions
    fi_to_ri = [-1] * len(rules)
    while any(ri == -1 for ri in fi_to_ri):
        for fi in range(len(fi_to_ri)):
            if fi_to_ri[fi] != -1:
                continue
            if sum(fi_valid_for_ri[fi]) == 1:
                ri = fi_valid_for_ri[fi].index(True)
                fi_to_ri[fi] = ri
                for fj in range(len(fi_valid_for_ri)):
                    fi_valid_for_ri[fj][ri] = False

    # Find the indices of the rules that are wanted, then figure out which
    # field indices those correspond to.
    wanted_ris = [ri for ri, r in enumerate(rules) if r[0].startswith("departure")]
    wanted_fis = [fi_to_ri.index(ri) for ri in wanted_ris]

    # Extract the fields and return their product
    return prod(my[fi] for fi in wanted_fis)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (71)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (26009)")
    print(part1(real_input()))

    print()
    print("Part 2 (589685618167)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
