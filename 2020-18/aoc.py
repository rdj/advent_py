#!/usr/bin/env pypy3


from collections import deque
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


def compute(toks: deque[str]) -> int:
    result = 0
    op = Op.add

    while toks:
        match toks.popleft():
            case n if str.isdigit(n):
                result = op(result, int(n))
                op = None

            case '+':
                op = Op.add

            case '*':
                op = Op.mul

            case '(':
                result = op(result, compute(toks))

            case ')':
                return result

    return result


def part1(s):
    return sum(compute(deque(line)) for line in parse(s))


# I rewrote my very brittle annoying string mutation solution based on
# something I found in the reddit answers thread.
#
# This very clever approach allows you to process left-to-right even with the
# new plus-first operator precedence.
#
# We only have to worry about three things, addition, multiplication, and
# grouping. The problem statement makes it explicit that part 2 is equivalent
# to adding groups around all addition statements.
#
# If we think about the relationship between those three things in terms of
# just our normal real world algebra, one thing that pops out is the
# distributive property of multiplication.
#
#     a * (b + c)  ===   a*b + b*c
#     (a + b + ....) * (c + d + ...)  ===   (a+b+...)*c + (a+b+...)*d + ...
#
# And that's basically our whole problem. If you add another * and group at the
# end, the multiplier part is just everything we have so far. If you add pluses
# on either side, they get automatically grouped in with the existing plus
# group. Any explicit parens get evaluated recursively to a value before
# proceeding.
#
# Here's the most complicated example from the problem:
#
#     ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
#      (  6   * 9)
#     ((     54  ) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
#                    ( 15   * 8 + 6)
#                    ( [m=15] 8 + 6)
#                    (      120 +90)
#                    (         210 )
#     (      54    *           210   + 6)
#     (         [m=54]         210   + 6)
#                           11340    + 324)
#     (                           11664 ) + 2 + 4 * 2
#                                       11666 + 4 * 2
#                                           11670 * 2
#                                              23340
#
# By default we just eat tokens and add them up. If we hit a *, we start over
# but now with a multiplier. If we hit a ( we evaluate the subgroup
# independently using the same rules recursively and then just deal with the
# value that comes out.

def compute2(toks: deque[str]) -> int:
    result = 0
    multiplier = 1

    while toks:
        match toks.popleft():
            case n if str.isdigit(n):
                result += int(n) * multiplier

            case '+':
                pass

            case '*':
                multiplier = result
                result = 0

            case '(':
                result += compute2(toks) * multiplier

            case ')':
                return result

    return result


def part2(s):
    return sum(compute2(deque(line)) for line in parse(s))


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
