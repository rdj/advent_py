#!/usr/bin/env python3

ExampleInput1 = '''\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
'''

def realinput():
    with open("input.txt", "r") as infile:
        return infile.read()

def subtotals(input):
    return [sum([int(line) for line in line_groups.strip().split("\n")]) for line_groups in input.split("\n\n")]

def part1(input):
    return max(subtotals(input))

def part2(input):
    a = subtotals(input)
    a.sort(reverse=True)
    return sum(a[0:3])

print('Example Part 1')
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
