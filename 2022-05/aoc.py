#!/usr/bin/env python3

import re

ExampleInput1 = '''\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''

def realinput():
    with open("input.txt", "r") as infile:
        return infile.read()

def parse_stacks(input):
    stacks = {}
    for col in zip(*reversed(input.splitlines()), strict=True):
        if col[0].isspace():
            continue
        stacks[int(col[0])] = list(filter(lambda c: not c.isspace(), col[1:]))
    return stacks

def apply_moves_one_by_one(moves, stacks):
    for m in moves.splitlines():
        n, src, dst = [int(_) for _ in re.findall('\d+', m)]
        for _ in range(n):
            x = stacks[src].pop()
            stacks[dst].append(x)

def apply_moves_grouped(moves, stacks):
    for m in moves.splitlines():
        n, src, dst = [int(_) for _ in re.findall('\d+', m)]
        x = stacks[src][-n:]
        del stacks[src][-n:]
        stacks[dst] += x

def extract(stacks):
    return ''.join(
        [s[-1] for s in
         [stacks[k] for k in
          sorted(stacks.keys())]])

def run(input, movefn):
    stacks, moves = input.split("\n\n")
    stacks = parse_stacks(stacks)
    movefn(moves, stacks)
    return extract(stacks)

def part1(input):
    return run(input, apply_moves_one_by_one)

def part2(input):
    return run(input, apply_moves_grouped)

print('Example Part 1 (want CMZ)')
print(part1(ExampleInput1))

print()
print('Part 1')
print(part1(realinput()))

print()
print('Example Part 2 (want MCD)')
print(part2(ExampleInput1))

print()
print('Part 2')
print(part2(realinput()))
