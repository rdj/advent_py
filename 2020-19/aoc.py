#!/usr/bin/env pypy3


from collections import deque
from functools import cache, cached_property
import regex as re  # supports recursive subpatterns (?<foo>...(?&foo)*...)


ExampleInput1 = """\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""


ExampleInput2 = """\
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""


class Matcher:
    def __init__(self, rules, part2=False):
        self.part2 = part2
        self.rule_strings = rules

    @cached_property
    def re(self):
        return re.compile(self.rule("0"))


    # 8: 42 | 42 8
    def rule8(self):
        return f'(?:{self.rule("42")})+'


    # 11: 42 31 | 42 11 31
    def rule11(self):
        return f'(?<r11>{self.rule("42")}(?&r11)*{self.rule("31")})'


    @cache
    def rule(self, n):
        if self.part2:
            if n == "8":
                return self.rule8()
            if n == "11":
                return self.rule11()

        srule = self.rule_strings[n]
        toks = deque(srule.split())
        grouped = False
        a = []

        while toks:
            match toks.popleft():
                case t if t[0] == '"':
                    a.append(t[1:-1])

                case t if t.isdigit():
                    a.append(self.rule(t))

                case "|":
                    a.append("|")
                    grouped = True

                case _:
                    raise Exception(f"Unrecognized rule: {n}: {srule}")

        rule = "".join(a)

        if grouped:
            return f"(?:{rule})"
        else:
            return rule


    def ismatch(self, s):
        return self.re.fullmatch(s)


def parse(s):
    s_rules, s_inputs = s.split("\n\n")
    rules = {}
    for line in s_rules.splitlines():
        k, v = line.split(": ")
        rules[k] = v
    return rules, s_inputs.splitlines()


def part1(s):
    rules, inputs = parse(s)
    matcher = Matcher(rules)
    return sum(1 for s in inputs if matcher.ismatch(s))


def part2(s):
    rules, inputs = parse(s)
    matcher = Matcher(rules, part2=True)
    return sum(1 for s in inputs if matcher.ismatch(s))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (2)")
    print(part1(ExampleInput1))

    print()
    print("Example Part 1.2 (3)")
    print(part1(ExampleInput2))

    print()
    print("Part 1 (129)")
    print(part1(real_input()))

    print()
    print("Example Part 2")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (243)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
