#!/usr/bin/env python3

import re


store = {
    # cost, dmg, arm
    'weapons': [
        ( 8, 4, 0),
        (10, 5, 0),
        (25, 6, 0),
        (40, 7, 0),
        (74, 8, 0),
    ],
    'armor': [
        (  0, 0, 0),
        ( 13, 0, 1),
        ( 31, 0, 2),
        ( 53, 0, 3),
        ( 75, 0, 4),
        (102, 0, 5),
    ],
    'rings': [
        (  0, 0, 0),
        ( 25, 1, 0),
        ( 50, 2, 0),
        (100, 3, 0),
        ( 20, 0, 1),
        ( 40, 0, 2),
        ( 80, 0, 3),
    ],
}


def addt(t0, t1):
    a, b, c = t0
    x, y, z = t1
    return (a+x, b+y, c+z)


def loadouts():
    for wpn in store['weapons']:
        for arm in store['armor']:
            wa = addt(wpn, arm)
            yield wa # no rings at all
            for i, r1 in enumerate(store['rings']):
                war = addt(wa, r1)
                for r2 in store['rings'][i+1:]:
                    yield addt(war, r2)


def parse(s):
    return tuple(map(int, re.findall(r"\d+", s)))


def wins(gear, boss):
    bhp, bdmg, barm = boss
    _, dmg, arm = gear
    hp = 100
    return bhp / max(1, dmg - barm) <= hp / (max(1, bdmg - arm))


def part1(s):
    boss = parse(s)
    for gear in sorted(loadouts()):
        if wins(gear, boss):
            return gear[0]


def part2(s):
    boss = parse(s)
    for gear in reversed(sorted(loadouts())):
        if not wins(gear, boss):
            return gear[0]


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Part 1 (91)")
    print(part1(real_input()))
    print()

    print("Part 2 (158)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
