#!/usr/bin/env python3

from bitstring import BitStream
from math import prod


ExampleInput1 = """\
8A004A801A8002F478
"""

ExampleInput2 = """\
620080001611562C8802118E34
"""

ExampleInput3 = """\
C0015000016115A2E0802F182340
"""

ExampleInput4 = """\
A0016C880162017C3686B18A3D4780
"""


def parse(s):
    return BitStream("0x" + s.strip())


def sum_versions(s):
    v = s.read(3).uint

    match s.read(3).uint:
        case 4: # literal
            n = 0b1_0000
            while n & 0b1_0000:
                n = s.read(5).uint

        case n: # operator
            lt = s.read(1).uint
            if lt == 0: # length is total bit length
                bitlen = s.read(15).uint
                before = s.pos
                while s.pos < before + bitlen:
                    v += sum_versions(s)

            else: # length is number of subpackets
                nsubs = s.read(11).uint
                for _ in range(nsubs):
                    v += sum_versions(s)

    return v


def packet_value(s):
    _ = s.read(3)

    opcode = s.read(3).uint
    if opcode == 4:
        n = 0b1_0000
        val = 0
        while n & 0b1_0000:
            n = s.read(5).uint
            val <<= 4
            val |= n & 0b1111
        return val

    subpackets = []
    lt = s.read(1).uint
    if lt == 0: # length is total bit length
        bitlen = s.read(15).uint
        before = s.pos
        while s.pos < before + bitlen:
            subpackets.append(packet_value(s))

    else: # length is number of subpackets
        nsubs = s.read(11).uint
        for _ in range(nsubs):
            subpackets.append(packet_value(s))

    match opcode:
        case 0:
            return sum(subpackets)

        case 1:
            return prod(subpackets)

        case 2:
            return min(subpackets)

        case 3:
            return max(subpackets)

        case 5:
            assert(len(subpackets) == 2)
            a, b = subpackets
            return int(a > b)

        case 6:
            assert(len(subpackets) == 2)
            a, b = subpackets
            return int(a < b)

        case 7:
            assert(len(subpackets) == 2)
            a, b = subpackets
            return int(a == b)

        case n:
            raise Exception(f"Unknown {opcode=}")


def part1(s):
    return sum_versions(parse(s))


def part2(s):
    return packet_value(parse(s))


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example 1 Part 1 (16)")
    print(part1(ExampleInput1))

    print()
    print("Example 2 Part 1 (12)")
    print(part1(ExampleInput2))

    print()
    print("Example 3 Part 1 (23)")
    print(part1(ExampleInput3))

    print()
    print("Example 4 Part 1 (31)")
    print(part1(ExampleInput4))

    print()
    print("Part 1 (873)")
    print(part1(real_input()))

    print()
    print("Part 2 (402817863665)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
