#!/usr/bin/env python3

Examples = (
    ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7, 19),
    ('bvwbjplbgvbhsrlpgdmjqwftvncz', 5, 23),
    ('nppdvjthqldpwncqszvftbrmjlhg', 6, 23),
    ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10, 29),
    ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11, 26),
)

def realinput():
    with open("input.txt", "r") as infile:
        return infile.read()

def index_after_first_heterogeneous_seq(s, n):
    for i in range(n, len(s)):
        if len(set(s[i-n:i])) == n:
            return i
    assert False, "found no heterogeneous seq of length %d in %s" % (n, s)


def part1(input):
    return index_after_first_heterogeneous_seq(input, 4)

def part2(input):
    return index_after_first_heterogeneous_seq(input, 14)

for n, (s, want, _) in enumerate(Examples):
    print('Part 1 - Example %d (want %s)' % (n + 1, want))
    print(part1(s))

print()
print('Part 1')
print(part1(realinput()))

print()
for n, (s, _, want) in enumerate(Examples):
    print('Part 2 - Example %d (want %s)' % (n + 1, want))
    print(part2(s))

print()
print('Part 2')
print(part2(realinput()))
