#!/usr/bin/env pypy3

import re
import json


ExamplesPart1 = (
    ("[1,2,3]", 6),
    ('{"a":2,"b":4}', 6),
    ('[[[3]]]', 3),
    ('{"a":{"b":4},"c":-1}', 3),
    ('{"a":[-1,1]}', 0),
    ('[-1,{"a":1}]', 0),
    ('[]', 0),
    ('{}', 0),
)

ExamplesPart2 = (
    ('[1,2,3]', 6),
    ('[1,{"c":"red","b":2},3]', 4),
    ('{"d":"red","e":[1,2,3,4],"f":5}', 0),
    ('[1,"red",5]', 6),
)


def part1(s):
    return sum(map(int, re.findall(r"-?\d+", s)))


def dsum(d):
    total = 0
    for k, o in d.items():
        if k == "red" or o == "red":
            return 0
        total += rsum(k) + rsum(o)
    return total


def rsum(o):
    if isinstance(o, int):
        return o
    if isinstance(o, str):
        return 0
    if isinstance(o, list):
        return sum(map(rsum, o))
    if isinstance(o, dict):
        return dsum(o)
    raise Exception(f"Unknown object type {o}")


def part2(s):
    return rsum(json.loads(s))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1):
        c = part1(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 (119433)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (68466)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
