#!/usr/bin/env python3

ExampleInput1 ="""\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

from collections import defaultdict

def hash(s):
    value = 0
    for c in s:
        value += ord(c)
        value *= 17
        value %= 256
    return value


def part1(s):
    return sum(hash(_) for _ in s.strip().split(','))


def part2(s):
    boxes = defaultdict(list)
    for step in s.strip().split(','):
        if '-' in step:
            label = step[:-1]
            box = hash(label)
            for lens in boxes[box]:
                if lens[0] == label:
                    boxes[box].remove(lens)
                    break
        else:
            label, length = step.split('=')
            box = hash(label)
            length = int(length)

            found = False
            for i, lens in enumerate(boxes[box]):
                if lens[0] == label:
                    boxes[box][i] = (label, length,)
                    found = True
                    break
            if not found:
                boxes[box].append((label, length,))

    power = 0
    for boxno, lenses in boxes.items():
        for i, lens in enumerate(lenses):
            power += (1 + boxno) * (i + 1) * lens[1]

    return power


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("HASH (52)")
    print(part1('HASH'))

    print()
    print("Example Part 1 (1320)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (510273)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (145)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (212449)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
