#!/usr/bin/env python3

from collections import defaultdict, deque
from enum import IntEnum, auto


ExampleInput1 = """\
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
"""


ExampleInput2 = """\
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
"""


class Op(IntEnum):
    SND = auto()
    SET = auto()
    ADD = auto()
    MUL = auto()
    MOD = auto()
    RCV = auto()
    JGZ = auto()


class Status(IntEnum):
    Initial = auto()
    Sending = auto()
    Waiting = auto()
    Terminated = auto()


def tryparse(s):
    try:
        return int(s)
    except:
        pass

    try:
        return Op[s.upper()]
    except:
        return s


def parse(s):
    return tuple(tuple(map(tryparse, line.split())) for line in s.splitlines())


def get(env, x):
    if isinstance(x, int):
        return x
    return env[x]


def p1runner(prog):
    ip = 0
    env = defaultdict(int)
    sound = None

    while 0 <= ip < len(prog):
        op, *args = prog[ip]
        match op:
            case Op.SND:
                sound = get(env, args[0])

            case Op.SET:
                env[args[0]] = get(env, args[1])

            case Op.ADD:
                env[args[0]] += get(env, args[1])

            case Op.MUL:
                env[args[0]] *= get(env, args[1])

            case Op.MOD:
                env[args[0]] %= get(env, args[1])

            case Op.RCV:
                if get(env, args[0]) != 0:
                    yield sound

            case Op.JGZ:
                if get(env, args[0]) > 0:
                    ip += get(env, args[1]) - 1

        ip += 1


def p2runner(prog, pid, q):
    ip = 0
    env = defaultdict(int)
    env["p"] = pid

    while 0 <= ip < len(prog):
        op, *args = prog[ip]
        match op:
            case Op.SND:
                yield (Status.Sending, get(env, args[0]))

            case Op.SET:
                env[args[0]] = get(env, args[1])

            case Op.ADD:
                env[args[0]] += get(env, args[1])

            case Op.MUL:
                env[args[0]] *= get(env, args[1])

            case Op.MOD:
                env[args[0]] %= get(env, args[1])

            case Op.RCV:
                if len(q) == 0:
                    yield (Status.Waiting,)
                env[args[0]] = q.popleft()

            case Op.JGZ:
                if get(env, args[0]) > 0:
                    ip += get(env, args[1]) - 1

        ip += 1

    return (Status.Terminated,)


def part1(s):
    prog = parse(s)
    runner = p1runner(prog)
    return next(runner)


def part2(s):
    prog = parse(s)

    queues = tuple(deque() for i in range(2))
    runners = tuple(p2runner(prog, i, queues[i]) for i in range(2))
    status = [Status.Initial] * 2
    sent = [0] * 2

    while True:
        if all(s == Status.Terminated for s in status):
            # Natural termination
            break

        if all(len(q) == 0 for q in queues) and all(s == Status.Waiting for s in status):
            # Deadlock
            break

        for i in range(2):
            if status[i] == Status.Waiting and len(queues[i]) == 0:
                continue

            s, *data = next(runners[i])
            if s == Status.Sending:
                queues[(i+1) % len(queues)].append(data[0])
                sent[i] += 1
            status[i] = s

    return sent[1]


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    print("Example Part 1 (4)")
    print(part1(ExampleInput1))

    print()
    print("Part 1 (2951)")
    print(part1(real_input()))

    print()
    print("Example Part 2 (3)")
    print(part2(ExampleInput2))

    print()
    print("Part 2 (7366)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
