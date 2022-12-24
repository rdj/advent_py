#!/usr/bin/env python3

ExampleInput1 = '''\
A Y
B X
C Z
'''

ResultScore = {
    0: 3, # Draw
    1: 6, # Win
    2: 0, # Loss
}

def realinput():
    with open("input.txt", "r") as infile:
        return infile.read()

def part1(input):
    score = 0
    for line in input.splitlines():
        elf, me = line.split()
        elf = ord(elf) - ord('A')
        me = ord(me) - ord('X')

        score += me + 1
        score += ResultScore[(me - elf) % 3]

    return score

def part2(input):
    return "TODO"

print('Example Part 1 (want 15)')
print(part1(ExampleInput1))

print()
print('Part 1')
print(part1(realinput()))

print()
print('Example Part 2')
print(part2(ExampleInput1))

print()
print('Part 2')
print(part2(realinput()))
