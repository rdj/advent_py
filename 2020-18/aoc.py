#!/usr/bin/env pypy3


import operator as Op
import re


ExamplesPart1 = [
    ( "1 + 2 * 3 + 4 * 5 + 6", 71 ),
    ( "1 + (2 * 3) + (4 * (5 + 6))", 51 ),
    ( "2 * 3 + (4 * 5)", 26 ),
    ( "5 + (8 * 3 + 9 + 3 * 4 * 3)", 437 ),
    ( "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240 ),
    ( "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632 ),
]

ExamplesPart2 = [
    ( "1 + (2 * 3) + (4 * (5 + 6))", 51 ),
    ( "2 * 3 + (4 * 5)", 46 ),
    ( "5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445 ),
    ( "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060 ),
    ( "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340 ),
]


def parse(s):
    return [re.sub(" ", "", line) for line in s.splitlines()]


def compute(s: str, pos: int) -> (int, int):
    result = 0
    op = Op.add

    i = pos
    while i < len(s):
        match s[i]:
            case n if "0" <= n <= "9":
                result = op(result, int(n))
                op = None
                i += 1

            case '+':
                op = Op.add
                i += 1

            case '*':
                op = Op.mul
                i += 1

            case '(':
                sub, i  = compute(s, i + 1)
                result = op(result, sub)

            case ')':
                return result, i + 1

    return result, None


def skipgroup(s:str, pos: int, d: int) -> int:
    begin = "("
    end = ")"
    if d == -1:
        begin, end = end, begin

    assert(s[pos] == begin)
    pos += d
    while s[pos] != end:
        if s[pos] == begin:
            pos = skipgroup(s, pos, d)
        else:
            pos += d
    return pos + d


def parenthesize(s:str) -> str:
    # first parenthesize all subgroups
    i = 0
    while i < len(s):
        match s[i]:
            case "(":
                j = skipgroup(s, i, 1)
                sub = parenthesize(s[i+1:j-1])
                s = s[:i+1] + sub + s[j-1:]
                i += len(sub)

            case _:
                i += 1

    # then parenthesize the + ops at this level
    i = 0
    while i < len(s):
        match s[i]:
            case "(":
                i = skipgroup(s, i, 1)

            case "+":
                # left paren before the preceding single digit number or
                # grouped expression
                j = i - 1
                if s[j] == ")":
                    j = skipgroup(s, j, -1)
                    j += 1
                s = s[:j] + "(" + s[j:]
                i += 1

                # right paren after the following single digit number or
                # grouped expression
                j = i + 1
                if s[j] == "(":
                    j = skipgroup(s, j, 1)
                    j -=1
                s = s[:j+1] + ")" + s[j+1:]
                i += 1

            case _:
                i += 1
    return s


def part1(s):
    return sum(compute(line, 0)[0] for line in parse(s))


def part2(s):
    return sum(compute(parenthesize(line), 0)[0] for line in parse(s))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (s, x) in enumerate(ExamplesPart1):
        print(f"Example Part 1.{i} ({x})")
        print(part1(s))
        print()

    print("Part 1 (1890866893020)")
    print(part1(real_input()))
    print()

    for i, (s, x) in enumerate(ExamplesPart2):
        print(f"Example Part 2.{i} ({x})")
        print(part2(s))
        print()

    print("Part 2 (34646237037193)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
