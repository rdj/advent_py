#!/usr/bin/env python3

import operator
from collections import deque


ExampleInput1 = """\
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
"""

ExampleInput2 = """\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""


def parse(s):
    statepart, rulespart = s.split("\n\n")

    state = {}
    for line in statepart.splitlines():
        key, val = line.split(": ")
        state[key] = int(val)

    rules = []
    for line in rulespart.splitlines():
        a, op, b, _, c = line.split()
        match op:
            case 'AND':
                op = operator.and_
            case 'OR':
                op = operator.or_
            case 'XOR':
                op = operator.xor
        rules.append((op, a, b, c))

    return state, rules


def evaluate(state, rules):
    rules = deque(rules)
    while rules:
        r = rules.popleft()
        op, a, b, c = r
        if a in state and b in state:
            state[c] = op(state[a], state[b])
        else:
            rules.append(r)

    result = 0
    i = 0
    while True:
        key = f"z{i:02d}"
        if key not in state:
            break
        result |= state[key] << i
        i += 1
    return result


def part1(s):
    return evaluate(*parse(s))


def part2(s):
    state, rules = parse(s)

    blank = state.copy()
    for k in blank.keys():
        blank[k] = 0

    broken_bits = []
    for i in range(44):
        s = blank.copy()
        x = 1 << i
        s[f"x{i:02d}"] = 1
        result = evaluate(s, rules)
        if result != x:
            broken_bits.append(i)

    print("Broken bits:", broken_bits)
    # Bits found wrong by experiment: 5 15 20 36

    # With the code above, I determined four bits that have problems. Since I
    # found that each z only depends on same/earlier x/y, I'm hoping this means
    # that each of the four bits has a localized problem with its adder that
    # can be fixed by swapping two outputs.
    #
    # I did not come up with a reasonable programmatic way to review the adder
    # design. (LATER NOTE: It seems like most people used graphviz or similar
    # to visually examine the circuit layout for problems.) I did an image
    # search for a full adder and then came up with an example for what that
    # would look like in the format of this puzzle:
    #
    # Example full adder for bit 2:
    #
    #   x02 XOR y02        -> xor02
    # xor02 XOR carry01    -> z02
    #   x02 AND y02        -> and02
    # xor02 AND carry01    -> precarry02
    # and02  OR precarry02 -> carry02
    #
    # Bits 0 and 45 will differ because of no carry in and out respectively.
    # The intermediate values I've called xor02, and02, carry01, precarry02,
    # and carry02 all have random 3-char names in the puzzle input.
    #
    # So now I manually isolate the five adder rules for each of the broken
    # bits and look for a swap that fixes them.

    swaps = []

    # BIT 5.
    #
    # The z05 rule is AND rule instead of XOR rule, so we have to figure out
    # whether it is and05 or precarry05. And swap accordingly. Here are the
    # rules:
    #
    #     x05 XOR y05 -> hdc (xor05)
    #     y05 AND x05 -> z05 <--
    #     gcs XOR hdc -> dkr <--
    #     hdc AND gcs -> fdd (precarry05)
    #     dkr OR  fdd -> bvc (carry05)
    #
    # Fixed by swapping z05 and dkr.
    swaps += ['z05', 'dkr']

    # BIT 15.
    #
    # Again the z15 rule is AND instead of XOR. Same logic as bit 5.
    #
    #     y15 XOR x15 -> bhw (xor15)
    #     sth AND bhw -> z15 <--
    #     y15 AND x15 -> hhb (and15)
    #     bhw XOR sth -> htp <--
    #     hhb OR  htp -> mqr (carry15)
    #
    # Fixed by swapping z15 and htp.
    swaps += ['z15', 'htp']

    # BIT 20.
    #
    # The z20 rule is an OR rule, so it must be swapped with the carry20 rule.
    #
    #     x20 XOR y20 -> mvv (xor20)
    #     qfj OR  mqg -> z20 <--
    #     x20 AND y20 -> mqg (and20)
    #     mvv AND fvm -> qfj (precarry20)
    #     mvv XOR fvm -> hhh <--
    #
    # Fixed by swapping z20, hhh.
    swaps += ['z20', 'hhh']

    # BIT 36.
    #
    # This one was trickier since the z rule itself looked fine. So next look
    # at the x/y rules, xor36 and and36. You can see they're wired wrong. For
    # example, carry36 needs to consume xor36 instead of and36.
    #
    #     y36 XOR x36 -> rhv <--
    #     ggk XOR hpg -> z36
    #      ^------------------------- This is and36 but should be xor36.
    #     x36 AND y36 -> ggk <--
    #     ggk AND hpg -> bqf (precarry36)
    #      ^------------------------- This is and36 but should be xor36.
    #     bqf OR  rhv -> gqf (carry36)
    #              ^----------------- This is the xor36 but should be and36.
    #
    # Fixed by swapping rhv, ggk.
    swaps += ['rhv', 'ggk']

    return ",".join(sorted(swaps))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example 1 Part 1 (4)")
    print(part1(ExampleInput1))

    print()
    print("Example 2 Part 1 (2024)")
    print(part1(ExampleInput2))

    print()
    print("Part 1 (53755311654662)")
    print(part1(real_input()))

    print()
    print("Part 2 (dkr,ggk,hhh,htp,rhv,z05,z15,z20)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()


