#!/usr/bin/env pypy3

ExampleInput1 = """\
2333133121414131402
"""

Free = 2 << 31


def parse(s):
    s = s.splitlines()[0]
    size = sum(int(_) for _ in s)
    disk = [Free] * size
    filemap = []

    cur = 0
    file = 0
    space = False
    for n in s:
        n = int(n)
        if space:
            cur += n
            space = False
            continue
        filemap.append((cur, n))
        for _ in range(n):
            disk[cur] = file
            cur += 1
        file +=1
        space = True

    return disk, filemap


def checksum(disk):
    return sum(i * file for i, file in enumerate(disk) if file != Free)


def print_disk(disk):
    out = []
    for _ in disk:
        if _ == Free:
            out.append('.')
        else:
            out.append(str(_))
    print("".join(out))


def part1(s):
    disk, filemap = parse(s)

    lcur = 0
    rcur = len(disk) - 1
    while True:
        while disk[lcur] != Free:
            lcur += 1
        while disk[rcur] == Free:
            rcur -= 1
        if lcur >= rcur:
            break
        disk[lcur] = disk[rcur]
        disk[rcur] = Free

    return checksum(disk)


def part2(s):
    disk, filemap = parse(s)

    def fill(loc, size, val):
        for i in range(loc, loc+size):
            disk[i] = val

    def find_space(size, before):
        start = None
        freelen = 0
        for i, f in enumerate(disk):
            if i == before:
                return None

            if f == Free:
                if start == None:
                    start = i
                    assert(freelen == 0)
                freelen += 1
                if freelen == size:
                    return start
            else:
                start = None
                freelen = 0
        return None

    for fid, (start, size) in reversed(list(enumerate(filemap))):
        free = find_space(size, start)
        if free != None:
            fill(start, size, Free)
            fill(free, size, fid)

    return checksum(disk)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (1928)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (6154342787400)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (2858)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (6183632723350)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
