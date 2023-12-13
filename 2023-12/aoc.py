#!/usr/bin/env python3

ExampleInput1 = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def numways(pattern, groups):
    # Base case, groups exhausted
    if len(groups) == 0:
        # Any springs left? That would be a nope
        if '#' in pattern:
            return 0

        # Otherwise, good match
        return 1

    # Fixed leading dots are, uh, fixed, so we can skip over them
    while len(pattern) and pattern[0] == '.':
        pattern = pattern[1:]

    # Shortcut out if there's not enough pattern left to fit the groups
    if len(pattern) < sum(groups) + len(groups) - 1:
        return 0

    glen = groups[0]

    # If we're starting with a spring, it must fit the first group
    if pattern[0] == '#':
        # Cannot be any dots
        if len(pattern) < glen:
            return 0
        for c in pattern[0:glen]:
            if c == '.':
                return 0

        # And can't be trailed by a spring
        if len(pattern) > glen and pattern[glen] == '#':
            return 0

        remains = pattern[glen+1:]
        return numways(remains, groups[1:])

    assert pattern[0] == '?'
    skip = pattern[1:]
    place = '#' + skip
    return numways(place, groups) + numways(skip, groups)


def part1(s):
    total = 0
    for lineno, line in enumerate(s.splitlines()):
        pattern, groupstr = line.split(' ')
        groups = tuple(map(int, groupstr.split(',')))

        a = numways(pattern, groups)
        total += a

    return total


def part2(s):
    return "TODO"


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (21)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (7753)")
    print(part1(real_input()))

    print()
    print("Example Part 2")
    print(part2(ExampleInput1))

    print()
    print("Part 2")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()

    # assert 0 == numways('', (1,))

    # assert 1 == numways('#', (1,))
    # assert 1 == numways('.#', (1,))
    # assert 1 == numways('#.', (1,))

    # assert 0 == numways('#', (2,))
    # assert 0 == numways('#', (1,1))

    # assert 1 == numways('?', (1,))
    # assert 1 == numways('.?', (1,))
    # assert 1 == numways('?.', (1,))

    # assert 2 == numways('??', (1,))
    # assert 3 == numways('???', (1,))
    # assert 2 == numways('???', (2,))
    # assert 1 == numways('???', (1,1))

    # assert 3 == numways('????', (1,1))
    # assert 6 == numways('?????', (1,1))

    # # ??????????.???.??? (1, 1, 1, 1, 2, 1)

    # assert 6 == numways('???.???', (2, 1))
    # assert 12 == numways('??.???.???', (2, 1))
    # assert 6 == numways('????????##.???.???', (1, 1, 1, 1, 2, 1))

    #assert 3 == numways('???##????#', (6, 1))

    #print("DONE")
