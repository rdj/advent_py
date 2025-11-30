#!/usr/bin/env python3

import re
from collections import Counter


ExampleInput1 = """\
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
"""


def parse(s):
    a = []
    p = re.compile(r"(.*)-(\d+)\[([a-z]+)\]")
    for line in s.splitlines():
        r, sec, chk = p.match(line).groups()
        sec = int(sec)
        a.append((r, sec, chk))
    return a


def cleanup(a):
    result = []
    for r, sec, chk in a:
        c = Counter([c for c in r if c != "-"])
        counts = [(-v, k) for k, v in c.items()]
        counts.sort()
        ver = "".join(_[1] for _ in counts[:5])
        if chk == ver:
            result.append((r, sec, chk))
    return result


def part1(s):
    a = cleanup(parse(s))
    return sum(sec for _, sec, _ in a)


TR1 = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                    "BCDEFGHIJKLMNOPQRSTUVWXYZAbcdefghijklmnopqrstuvwxyza")
def rotn(s, n):
    for _ in range(n):
        s = s.translate(TR1)
    return s


def part2(s):
    for r, sec, _ in cleanup(parse(s)):
        if rotn(r, sec) == "northpole-object-storage":
            return sec


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (1514)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (185371)")
    print(part1(real_input()))

    print()
    print("Part 2 (984)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
