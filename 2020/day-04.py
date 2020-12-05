#! /usr/bin/env python3

from functools import reduce
from pathlib import Path

text = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

text = (Path(__file__).parent.absolute() / "day-04.txt").read_text()

# part 1
lines = text.split("\n\n")
lines = [line.replace("\n", " ").split(" ") for line in lines]
entries = [{field.split(":")[0]:field.split(":")[1] for field in line} for line in lines]

valid = 0
fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
for entry in entries:
    if set(entry.keys()) >= fields:
        valid += 1

print(f"Found {valid} valid passports")

# part 2

validate = {
    'byr': lambda v: 1920 <= int(v) <= 2002,
    'iyr': lambda v: 2010 <= int(v) <= 2020,
    'eyr': lambda v: 2020 <= int(v) <= 2030,
    'hgt': lambda v: (v.endswith("cm") and 150 <= int(v[:-2]) <= 193) or (v.endswith("in") and 59 <= int(v[:-2]) <= 76),
    'hcl': lambda v: v[0] == '#' and len(v) == 7 and set(v[1:]) <= set(list("0123456789abcdef")),
    'ecl': lambda v: v in set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]),
    'pid': lambda v: len(v) == 9 and set(v) <= set(list("0123456789")),
    'cid': lambda v: True
}

valid = 0
for entry in entries:
    if set(entry.keys()) >= fields:
        okay = True
        for field, value in entry.items():
            okay = okay and validate[field](value)
        valid += 1 if okay else 0

print(f"Found {valid} valid passports")

print("done")
