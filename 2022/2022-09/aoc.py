#!/usr/bin/env python3

ExampleInput1 = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''

ExampleInput2 = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''

def realinput():
    with open("input.txt", "r") as infile:
        return infile.read()

Directions = {
    'U': [0, -1],
    'D': [0, 1],
    'R': [1, 0],
    'L': [-1, 0],
}

def add(a, b):
    a[0] += b[0]
    a[1] += b[1]

def difference(a, b):
    return [a[0] - b[0], a[1] - b[1]]

def sign(n):
    if n == 0:
        return 0
    return n//abs(n)

def update(snake):
    for i in range(1, len(snake)):
        dxy = difference(snake[i-1], snake[i])
        if all([abs(n) <= 1 for n in dxy]):
            continue
        add(snake[i], [sign(d) for d in dxy])

def countailpos(input, snakelen):
    tailpos = set()
    snake = [[0,0] for _ in range(snakelen)]
    for m in input.splitlines():
        d, n = m[0], int(m[1:])
        for _ in range(n):
            add(snake[0], Directions[d])
            update(snake)
            tailpos.add(tuple(snake[-1]))
    return len(tailpos)

def part1(input):
    return countailpos(input, 2)

def part2(input):
    return countailpos(input, 10)

print('Example Part 1 (want 13)')
print(part1(ExampleInput1))

print()
print('Part 1')
print(part1(realinput()))

print()
print('Example 1 Part 2 (want 1)')
print(part2(ExampleInput1))

print()
print('Example 2 Part 2 (want 36)')
print(part2(ExampleInput2))

print()
print('Part 2')
print(part2(realinput()))
