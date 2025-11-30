#!/usr/bin/env python3

import re
from collections import defaultdict, Counter


MultiLineExample = """\
H => HO
H => OH
O => HH

HOHOHO
"""

ExamplesPart1 = (
    (MultiLineExample, 7),
)


def parse(s):
    rules = defaultdict(list)
    s, iv = s.split("\n\n")
    for line in s.splitlines():
        a, b = line.split(" => ")
        rules[a] += [b]
    return iv.strip(), rules



def part1(s):
    iv, rules = parse(s)
    mols = set()

    for pat, subs in rules.items():
        for m in re.finditer(pat, iv):
            a, b = m.span()
            before, after = iv[:a], iv[b:]
            for sub in subs:
                mols.add(before + sub + after)

    return len(mols)


def analyze(target, rules):
    nonterminals = set(rules.keys())
    syms = set()
    for prods in rules.values():
        for v in prods:
            for s in re.findall(r"e|[A-Z][a-z]|[A-Z]", v):
                syms.add(s)

    terminals = syms - nonterminals

    print("Nonterminals")
    print(nonterminals)
    print()

    print("Terminals")
    print(terminals)
    print()

    # Nonterminals
    # {'Al', 'B', 'Ca', 'F', 'H', 'Mg', 'N', 'O', 'P', 'Si', 'Th', 'Ti', 'e'}
    # Terminals
    # {'Rn', 'Ar', 'Y', 'C'}
    #

    tokens = list(re.findall("e|[A-Z][a-z]|[A-Z](?![a-z])", target))
    c = Counter(tokens)

    # Note: The "target" string contains a mix of terminal and nonterminal
    # symbols. In fact, this grammar never matches anything because it can't
    # terminate.
    #
    # The terminals are Rn, Ar, Y, and C.
    #
    # Let Q, R, S, T be nonterminal symbols.
    #
    # All the productions are of the form
    #
    #     Q => R S
    #     Q => R Rn S Ar
    #     Q => R Rn S F T Ar
    #     Q => C Rn R Ar
    #     Q => C Rn R F S Ar
    #     Q => C Rn R F S F T Ar
    #
    # So just from the point of view of making this visually easier, Ar and Rn
    # are acting like balanced parentheses and F is like a comma, and C is the
    # only other nonterminal, and it has some weird properties that would care
    # about if we were actually trying to make the parse tree, but for the
    # purposes of counting steps, we can just ignore it.
    #
    #     Q => R S             2 symbols
    #     Q => R ( S )         2 symbols + ( )
    #     Q => R ( S , T )     2 symbols + ( ) + 1 symbol + ,
    #     Q => 0 ( R )         2 symbols + ( )
    #     Q => 0 ( R , S )     2 symbols + ( ) + , + 1 symbol
    #     Q => 0 ( R , S , T ) 2 symbols + ( ) + 2 * (, + 1 symbol)
    #
    # There's no need to actually create the parse tree, we just need to figure
    # out the number of steps.
    #
    # It generally takes (N-1) steps to produce N tokens, and then we adjust
    # for the special nonterminals. The paren-like symbols (Rn, Ar) come along
    # for free. The comma-like symbol (Y) is free and also brings along an
    # extra free nonterminal.

    return len(tokens) - 1 - c['Rn'] - c['Ar'] - 2*c['Y']


# It seems so ill-advised, but I am going to just BFS this since this is 2015
# and so far every time I've tried to be cleverer than that it has been a waste
# of my time. I'm gonna guess from the way things are hinted the only real
# optimization you need is to prune duplicate paths.
#
# Ok, lol, brute force did not work this time. It ran for a while and didn't
# come up with an answer so now it's time to look at the input.
#
# If I'm remembering my college courses correctly, this looks like a
# context-free grammar, and probably we care which productions are terminal vs
# non-terminal, and there's definitely a normalized form that they might be in
# that would make things easier. Later: It's not in Chomsky normal form.
def part2(s):
    target, rules = parse(s)
    return analyze(target, rules)


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

    print("Part 1 (535)")
    print(part1(real_input()))
    print()

    print("Part 2 (212)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
