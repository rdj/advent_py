#!/usr/bin/env pypy3


ExampleInput1 = "389125467"


def parse(s):
    nums = list(map(int, s.strip()))
    k = len(nums)
    a = [0] * (k+1)
    for i in range(k):
        a[nums[i]] = nums[(i+1) % k]
    return a, nums[0]


def dump(d, start, cur, sep=" "):
    s = []
    n = start
    first = True
    while first or n != start:
        first = False
        if n == cur:
            s.append(f"({n})")
        else:
            s.append(str(n))
        n = d[n]
    return sep.join(s)


def run(d, cur, steps, mod):
    start = cur

    for m in range(steps):
        #print(f"-- move {m+1} --")
        #print("cups:", dump(d, start, cur))

        pickup = [d[cur], 0 , 0]
        pickup[1] = d[pickup[0]]
        pickup[2] = d[pickup[1]]
        d[cur] = d[pickup[-1]]

        #print("pick up:", pickup)

        dst = cur
        while True:
            dst = ((dst - 2) % mod) + 1
            if dst not in pickup:
                break
        #print("destination:", dst)

        d[dst], d[pickup[-1]] = pickup[0], d[dst]

        cur = d[cur]

    return d


def part1(s):
    a, cur = parse(s)
    run(a, cur, 100, 9)
    return dump(a, 1, -1, "")[1:]


def embiggen(head, cur):
    a = [0] * 1_000_001
    a[:len(head)] = head

    last = a.index(cur)
    a[last] = 10
    a[1_000_000] = cur

    for i in range(10, 1_000_000):
        a[i] = i + 1

    return a


def part2(s):
    head, cur = parse(s)
    a = embiggen(head, cur)
    run(a, cur, 10_000_000, 1_000_000)
    return a[1] * a[a[1]]


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (67384529)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (25368479)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (149245887792)")
    print(part2(ExampleInput1))

    print()
    print("Part 2 (44541319250)")
    print(part2(real_input()))


if __name__ == "__main__":
    # import cProfile
    # cProfile.run("part2(real_input())", sort="cumulative")
    run_all()
