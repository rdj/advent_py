#!/usr/bin/env python3

from collections import defaultdict
import re


MultiLineExample = """\
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""

ExamplesPart1 = (
    (MultiLineExample, 2),
)

MultiInvalid = """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""

MultiValid = """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""

ExamplesPart2 = (
    (MultiInvalid, 0),
    (MultiValid, 4),
)


def parse(s):
    return [dict(map(lambda s: s.split(":"), g.split())) for g in s.split("\n\n")]


def check(batch, with_validation):
    fields = (
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid',
        # cid not required
    )

    n = 0
    for p in batch:
        if all(f in p for f in fields):
            if not with_validation:
                n += 1
            elif all(validate(f, p[f]) for f in fields):
                n += 1

    return n


def part1(s):
    return check(parse(s), False)

def validate(f, s):
    match f:
        case 'byr':
            return 1920 <= int(s) <= 2002

        case 'iyr':
            return 2010 <= int(s) <= 2020

        case 'eyr':
            return 2020 <= int(s) <= 2030

        case 'hgt':
            m = re.search(r'^(\d+)(cm|in)', s)
            if not m:
                return False
            d, u = m.groups()
            d = int(d)
            if u == 'cm':
                return 150 <= d <= 193
            else:
                return 59 <= d <= 76

        case 'hcl':
            return re.search(r'^#[0-9a-f]{6}$', s)

        case 'ecl':
            return re.search(r'^(amb|blu|brn|gry|grn|hzl|oth)$', s)

        case 'pid':
            return re.search(r'^[0-9]{9}$', s)

        case 'cid':
            return True


def part2(s):
    return check(parse(s), True)


def real_input():
    with open("input.txt", "r") as infile:
        return infile.read()


def run_all():
    for i, (a, b) in enumerate(ExamplesPart1):
        c = part1(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 1.{i} ({b})")
        print(check, c)
        print()

    print("Part 1 (226)")
    print(part1(real_input()))
    print()

    for i, (a, b) in enumerate(ExamplesPart2):
        c = part2(a)
        check = "✅️" if b == c else "⚠️"
        print(f"Example Part 2.{i} ({b})")
        print(check, c)
        print()

    print("Part 2 (160)")
    print(part2(real_input()))


if __name__ == "__main__":
    run_all()
