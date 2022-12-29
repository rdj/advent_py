#!/usr/bin/env python3

ExampleInput1 = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''

def realinput():
    with open("input.txt", "r") as infile:
        return infile.read()

def torange(s):
    m, n = [int(_) for _ in s.split('-')]
    return range(m, n + 1)

def countif(input, cond):
    count = 0
    for line in input.splitlines():
        a, b = [set(torange(_)) for _ in line.split(',')]
        if cond(a, b):
            count += 1
    return count

def part1(input):
    return countif(input, lambda a, b: a <= b or b <= a)

def part2(input):
    return countif(input, lambda a, b: len(a & b) > 0)

print('Example Part 1 (want 2)')
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
