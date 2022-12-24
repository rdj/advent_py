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

def part1(input):
    best = 0
    single = 0
    for line in input.splitlines():
        if line == '':
            single = 0
            continue

        single += int(line)
        best = max(best, single)
    return best

print('Example')
print(part1(ExampleInput1))

print()
print('Part 1')
print(part1(realinput()))
