#! /usr/bin/env python3

from collections import Counter
from functools import reduce
from pathlib import Path

""" Ideal Patterns: 

0: abcefg  6/6 or 9
1: cf      2
2: acdeg   5/3 or 5
3: acdfg   5/2 or 5
4: bcdf    4
5: abdfg   5/2 or 3
6: abdefg  6/0 or 9
7: acf     3
8: abcdefg 7
9: abcdfg  6/0 or 6

"""

with Path("../inputs/08.txt").open("r") as handle:
    lines = [line.strip() for line in handle.readlines()]

lines = list([line.split(" | ") for line in lines])
lines = list([[list(map(lambda x: "".join(sorted(x)), line[0].split())), list(map(lambda x: "".join(sorted(x)), line[1].split()))] for line in lines])

# Part 1 - look for 1, 4, 7, or 8 (unique lengths)
outputs = reduce(lambda x, y: x + y, map(lambda l: l[1], lines), [])

lengths = list(map(len, outputs))
counts = Counter(lengths)

print(f"{counts[2]=}, {counts[3]=}, {counts[4]=}, {counts[7]=}, total={counts[2] + counts[3] + counts[4] + counts[7]}")


def get_mapping(unique):
    """
    1. length 2 is "1"
    2. length 3 is "7"
    3. length 4 is "4"
    4. length 7 is "8"
    5. length 5 with two segments in common with 4 is "2"
    6. length 5 with four segments in common with 2 is "3"
    7. length 5 with three segments in common with 2 is "5" (or four segments in common with 3)
    8. length 6 with four segments in common with 4 is "9"
    9. length 6 with five segments in common with 5 is "6"
    10. remaining length 6 is "0"
    """

    one = list(filter(lambda x: len(x) == 2, unique))[0]
    seven = list(filter(lambda x: len(x) == 3, unique))[0]
    four = list(filter(lambda x: len(x) == 4, unique))[0]
    eight = list(filter(lambda x: len(x) == 7, unique))[0]

    fives = list(filter(lambda x: len(x) == 5, unique))

    def is_two(test):
        return len(set(test) & set(four)) == 2  # two segments in common with 4 is "2"

    two = list(filter(is_two, fives))[0]
    fives.remove(two)

    def is_three(test):
        return len(set(test) & set(two)) == 4   # four segments in common with 2 is "3"

    three = list(filter(is_three, fives))[0]
    fives.remove(three)

    five = fives[0]

    sixes = list(filter(lambda x: len(x) == 6, unique))

    def is_nine(test):
        return len(set(test) & set(four)) == 4  # four segments in common with four is "9"

    nine = list(filter(is_nine, sixes))[0]
    sixes.remove(nine)

    def is_six(test):
        return len(set(test) & set(five)) == 5  # five segments in common with five is "6"

    six = list(filter(is_six, sixes))[0]
    sixes.remove(six)

    zero = sixes[0]

    return {zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9}


def decode_line(line):
    cat = get_mapping(line[0])
    digits = list([cat[output] for output in line[1]])
    number = reduce(lambda x, y: 10*x + y, digits, 0)

    return number


numbers = list(map(decode_line, lines))
total = sum(numbers)
print(f"{total=}")

pass
