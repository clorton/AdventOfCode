from itertools import permutations
from pathlib import Path
# import re

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "day-21.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "029A",
#     "980A",
#     "179A",
#     "456A",
#     "379A",
# ]

"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""

"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""

npad = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),

    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),

    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),

    "0": (1, 3),
    "A": (2, 3),
}

dpad = {
    "^": (1, 0),
    "A": (2, 0),

    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}

delta = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
    "A": (0, 0),
}

def valid(cx, cy, sequence, space):
    for char in sequence:
        dx, dy = delta[char]
        cx, cy = cx + dx, cy + dy
        if (cx, cy) == space:
            return False

    return True

def numeric(code):
    cx, cy = npad["A"]
    sequence = []
    for char in code:
        ex, ey = npad[char]

        key = "<" if ex < cx else ">"
        moves =  key * abs(ex - cx)
        key = "^" if ey < cy else "v"
        moves += key * abs(ey - cy)

        options = list(set(filter(lambda p: valid(cx, cy, p, (0, 3)), map(lambda p: "".join(p)+"A", permutations(moves)))))
        sequence.append(options)

        cx, cy = ex, ey

    return sequence

def directional(code):
    cx, cy = dpad["A"]
    sequence = []
    for char in code:
        ex, ey = dpad[char]

        key = "<" if ex < cx else ">"
        moves =  key * abs(ex - cx)
        key = "^" if ey < cy else "v"
        moves += key * abs(ey - cy)

        options = list(set(filter(lambda p: valid(cx, cy, p, (0, 0)), map(lambda p: "".join(p)+"A", permutations(moves)))))
        sequence.append(options)

        cx, cy = ex, ey

    return sequence

def expand(lst):
    result = []
    for element in lst:
        if isinstance(element, list):
            result.append(expand(element))
        else:
            result.append(directional(element))
    return result

def select(l):
    minimum = min(map(len, l))
    return next(filter(lambda p: len(p) == minimum, l))

def concat(m):
    return "".join(list(map(select, m)))

complexity = 0
for code in lines:
    num = concat([concat([[concat(directional(sequence)) for sequence in options] for options in directional(sequence)]) for sequence in options] for options in numeric(code))
    print(f"{code}: ({len(num)=}) {num=}")
    complexity += len(num) * int(code[:-1], 10)

print(f"Complexity: {complexity}")

# Part 2

from functools import lru_cache

@lru_cache
def foo(s, depth):
    if depth == 0:
        return len(s)
    return solve(directional(s), depth)

def solve(code, depth):
    # code = list of lists of strings, e.g. [['<A'], ['^A'], ['^^>A', '^>^A', '>^^A'], ['vvvA']]

    lengths = []
    for a in code:  # a = list of strings, e.g. ['<A'] or ['^^>A', '^>^A', '>^^A']
        minima = [foo(b, depth-1) for b in a]   # depth first search
        minimum = min(minima)
        lengths.append(minimum)
    return sum(lengths)

complexity = 0
for code in lines:
    num = numeric(code)
    length = solve(num, 26)
    print(f"{code}: {length}")
    complexity += length * int(code[:-1], 10)

print(f"Complexity: {complexity}")

print("Done.")
