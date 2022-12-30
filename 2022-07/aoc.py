#!/usr/bin/env python3

import re

ExampleInput1 = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''

def realinput():
    with open("input.txt", "r") as infile:
        return infile.read()

class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.contents = []
        self.size = None

    def is_dir(self):
        return True

    def get(self, name):
        for x in self.contents:
            if x.name == name:
                return x
        assert False, "did't find subdir"

    def get_size(self):
        if self.size == None:
            self.size = 0
            for x in self.contents:
                self.size += x.get_size()
        return self.size

class File:
    def __init__(self, name, parent, size):
        self.name = name
        self.parent = parent
        self.size = size

    def get_size(self):
        return self.size

    def is_dir(self):
        return False

def parse(s):
    root = Directory('/', None)
    cd = root
    fs = [root]

    for line in s.splitlines():
        if line == '$ cd /':
            cd = root
            continue

        if line == '$ ls':
            continue

        m = re.match('[$] cd (\S+)', line)
        if m != None:
            name = m[1]
            if name == '..':
                if cd.parent != None:
                    cd = cd.parent
                continue

            cd = cd.get(name)
            continue

        m = re.match('(\d+) (\S+)', line)
        if m != None:
            size, name = int(m[1]), m[2]
            newfile = File(name, cd, size)
            fs.append(newfile)
            cd.contents.append(newfile)
            continue

        m = re.match('dir (\S+)', line)
        if m != None:
            name = m[1]
            newdir = Directory(name, cd)
            fs.append(newdir)
            cd.contents.append(newdir)
            continue

        assert False, "Unmatched line: %s" % line

    return fs

def part1(input):
    fs = parse(input)
    total = 0
    for f in fs:
        if f.is_dir() and f.get_size() <= 100000:
            total += f.get_size()
    return total

def part2(input):
    DISK_CAPACITY = 70000000
    SPACE_REQUIRED = 30000000

    fs = parse(input)
    used = fs[0].get_size()
    to_free = SPACE_REQUIRED - (DISK_CAPACITY - used)

    best = DISK_CAPACITY
    for f in fs:
        if f.is_dir() and f.get_size() >= to_free:
            best = min(best, f.get_size())

    return best

print('Example Part 1 (want 95437)')
print(part1(ExampleInput1))

print()
print('Part 1')
print(part1(realinput()))

print()
print('Example Part 2 (want 24933642)')
print(part2(ExampleInput1))

print()
print('Part 2')
print(part2(realinput()))
