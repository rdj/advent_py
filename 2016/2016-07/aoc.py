#!/usr/bin/env python3

import regex # overlapped


ExampleInput1 = """\
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
"""

ExampleInput2 = """\
aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb
"""

ABBA = regex.compile(r"(.)(?!\1)(.)\2\1")
ABBA_IN = regex.compile(r"\[[^]]*(.)(?!\1)(.)\2\1")

def abbamatch(word):
    if ABBA_IN.search(word):
        return False
    clean = regex.sub(r"\[[^]]*\]", "/", word)
    return ABBA.search(clean) is not None


def part1(s):
    return sum(1 for word in s.splitlines() if abbamatch(word))


ABA = regex.compile(r"(.)(?!\1)(.)\1")

def abamatch(word):
    clean = regex.sub(r"\[[^]]*\]", "/", word)
    for a, b in ABA.findall(clean, overlapped=True):
        if regex.search(r"\[[^]]*" + b + a + b, word):
            return True
    return False


def part2(s):
    return sum(1 for word in s.splitlines() if abamatch(word))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (2)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (110)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (3)")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (242)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
