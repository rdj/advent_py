#!/usr/bin/env python3

ExampleInput1 = '''\
A Y
B X
C Z
'''

def realinput():
    with open("input.txt", "r") as infile:
        return infile.read()

def parse(input):
    a = []
    for line in input.splitlines():
        elf, me = line.split()
        elf = ord(elf) - ord('A')
        me = ord(me) - ord('X')
        a.append((elf, me))
    return a

def score_round(elf, me):
    score = me + 1
    score += 3 * ((me - elf + 1) % 3)
    return score

def part1(input):
    score = 0
    for (elf, me) in parse(input):
        score += score_round(elf, me)
    return score

def part2(input):
    score = 0
    for (elf, result) in parse(input):
        me = (elf + result - 1) % 3
        score += score_round(elf, me)
    return score

print('Example Part 1 (want 15)')
print(part1(ExampleInput1))

print()
print('Part 1')
print(part1(realinput()))

print()
print('Example Part 2 (want 12)')
print(part2(ExampleInput1))

print()
print('Part 2')
print(part2(realinput()))
