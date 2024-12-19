from pathlib import Path
# import re

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "day-19.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "r, wr, b, g, bwu, rb, gb, br",
#     "",
#     "brwrr",
#     "bggr",
#     "gbbr",
#     "rrbgbr",
#     "ubwu",
#     "bwurrg",
#     "brgr",
#     "bbrgwb",
# ]

towels = set(lines[0].split(", "))
patterns = lines[2:]
prefixes = set([len(towel) for towel in towels])

from functools import lru_cache

@lru_cache(maxsize=(1<<20))
def solve(pattern):

    if pattern in towels:
        return True

    for i in sorted(prefixes, reverse=True):
        if (pattern[:i] in towels) and solve(pattern[i:]):
            return True

    return False

solveable = 0
for i in tqdm(range(len(patterns))):
    if solve(patterns[i]):
        solveable += 1

print(solveable)

@lru_cache(maxsize=(1<<20))
def solve2(pattern):

    if len(pattern) == 0:
        ways = 1
    elif len(pattern) == 1:
        ways = 1 if pattern in towels else 0
    else:
        ways = 0
        for i in sorted(prefixes, reverse=True):
            if i > len(pattern):
                continue
            if pattern[:i] in towels:
                # print(f"{i}:{pattern} - try `{pattern[:i]}` / `{pattern[i:]}`")
                ways += solve2(pattern[i:])

    # print(f"{pattern} -> {ways}")
    return ways

options = 0
for i in tqdm(range(len(patterns))):
    options += solve2(patterns[i])

print(options)

print("Done!")
