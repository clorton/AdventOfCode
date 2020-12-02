#! /usr/bin/env python3

from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-02.txt").read_text()


# part 1
lines = text.split("\n")
entries = [tuple(line.split(" ")) for line in lines]


def valid(entry):
    minimum, maximum = entry[0].split("-")
    minimum = int(minimum)
    maximum = int(maximum)
    character = entry[1][0]
    password = entry[2]
    count = password.count(character)
    return minimum <= count <= maximum


valid_entries = sum(map(valid, entries))
print(f"# of valid passwords is {valid_entries}")


# part 2
def extra_valid(entry):
    minimum, maximum = entry[0].split("-")
    minimum = int(minimum)
    maximum = int(maximum)
    character = entry[1][0]
    password = entry[2]
    first = (password[minimum-1] == character)
    second = (password[maximum-1] == character)
    return (first and not second) or (second and not first)
    # return (first or second) and (first ^ second)


valid_entries = sum(map(extra_valid, entries))
print(f"# of valid passwords is {valid_entries}")
