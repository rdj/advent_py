#!/usr/bin/env python3

import re
import operator

from collections import deque
from functools import reduce, partial

ExampleInput1 = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


def allints(s):
    return list(int(_) for _ in re.findall(r"\d+", s))


def square(x):
    return x * x


def parse(s):
    monkeys = []

    for block in s.split("\n\n"):
        lines = iter(block.splitlines())

        # Monkey 3:
        number = allints(next(lines))[0]
        #   Starting items: 74
        items = allints(next(lines))

        #   Operation: new = old + 3
        #   Operation: new = old * 4
        #   Operation: new = old * old
        opwords = next(lines).split()
        op = None
        if opwords[-1] == "old":
            op = square
        else:
            arg = int(opwords[-1])
            match opwords[-2]:
                case "+":
                    op = partial(operator.add, arg)
                case "*":
                    op = partial(operator.mul, arg)
        assert op is not None, f"Unrecognized operation: {opwords}"

        #   Test: divisible by 17
        divisor = allints(next(lines))[0]

        #     If true: throw to monkey 0
        next_true = allints(next(lines))[0]

        #     If false: throw to monkey 1
        next_false = allints(next(lines))[0]

        monkeys.append(
            Monkey(number, items, op, divisor, next_true, next_false))

    return monkeys


class Monkey:

    def __init__(self, number, items, operation, divisor, next_true,
                 next_false):
        self.number = number
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.next_true = next_true
        self.next_false = next_false
        self.inspected = 0
        assert self.next_true != self.number, "Target is self"
        assert self.next_false != self.number, "Target is self"

    def toss_all(self, monkeys, shrinkfn):
        items, self.items = self.items, []
        for n in items:
            self.inspected += 1
            n = self.operation(n)
            n = shrinkfn(n)
            is_div = n % self.divisor == 0
            target = self.next_true if is_div else self.next_false
            monkeys[target].items.append(n)


def dump(monkeys):
    for m in monkeys:
        print(f"Monkey {m.number}: {m.items}")
    print()


def do_round(monkeys, shrinkfn):
    for m in monkeys:
        m.toss_all(monkeys, shrinkfn)


def extract(monkeys):
    *_, a, b = sorted((m.inspected for m in monkeys))
    return a * b


def part1(s):
    ROUNDS = 20
    def div3(x): return x // 3
    monkeys = parse(s)
    for _ in range(ROUNDS):
        do_round(monkeys, div3)
    return extract(monkeys)


def part2(s):
    ROUNDS = 10_000
    monkeys = parse(s)
    divisors = [m.divisor for m in monkeys]
    # In theory we want the LCM, but in our actual input, the divisors are all
    # prime, so just multiply them all together to find a modulus that will
    # work.
    multiple = reduce(operator.mul, divisors)
    def modlcm(x): return x % multiple

    for _ in range(ROUNDS):
        do_round(monkeys, modlcm)
    return extract(monkeys)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (10605)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (99840)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (2713310158)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (20683044837)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
