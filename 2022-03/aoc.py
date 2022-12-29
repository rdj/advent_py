#!/usr/bin/env python3

#import itertools

ExampleInput1 = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw'''

def realinput():
    with open("input.txt", "r") as infile:
        return infile.read()

def value(b):
    if b.isupper():
        return ord(b) - ord('A') + 27
    return ord(b) - ord('a') + 1

def part1(input):
    sum = 0
    for line in input.splitlines():
        split = len(line)//2
        both = set(line[:split]) & set(line[split:])
        assert len(both) == 1, "failed to find common item"
        sum += value(both.pop())
    return sum


def part2(input):
    lines = iter(input.splitlines())
    sum = 0
    for three in zip(*([lines] * 3)):
        common = None
        for line in three:
            if common == None:
                common = set(line)
                continue
            common &= set(line)
        assert len(common) == 1, "failed to find common item"
        sum += value(common.pop())
    return sum

print('Example Part 1 (want 157)')
print(part1(ExampleInput1))

print()
print('Part 1')
print(part1(realinput()))

print()
print('Example Part 2 (want 70)')
print(part2(ExampleInput1))

print()
print('Part 2')
print(part2(realinput()))
