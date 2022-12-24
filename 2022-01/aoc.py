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
    a = []
    single = 0
    for line in input.splitlines():
        if line == '':
            a.append(single)
            single = 0
            continue

        single += int(line)
    a.append(single)
    a.sort(reverse=True)
    return a

def part1(input):
    return subtotals(input)[0]

def part2(input):
    return sum(subtotals(input)[0:3])

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
