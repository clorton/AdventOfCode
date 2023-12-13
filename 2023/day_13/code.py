#! /usr/bin/env python3

from collections import defaultdict
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

patterns = []
pattern = []
for line in input:
    if line == "":
        patterns.append(pattern)
        pattern = []
        continue
    pattern.append(line)
patterns.append(pattern)

def find_reflection(pattern):
    consider = []
    for column in range(pattern.shape[1]-1):
        if np.all(pattern[:, column] == pattern[:, column+1]):
            consider.append(column)
    match = False
    for column in consider:
        match = True
        left, right = column-1, column+2
        while left >= 0 and right < pattern.shape[1]:
            if not np.all(pattern[:, left] == pattern[:, right]):
                match = False
                break
            left -= 1
            right += 1
        if match:
            return column + 1
    return 0

score = 0
for ipattern, pattern in enumerate(patterns):
    pattern = np.array(list(map(list, pattern)))
    if column := find_reflection(pattern):
        score += column
    elif column := find_reflection(pattern.T):
        score += 100 * column
    else:
        print("No reflection found for pattern", ipattern)
    
print("Score:", score)

def find_reflection2(pattern):
    consider = []
    for column in range(pattern.shape[1]-1):
        diffs = (pattern[:, column] != pattern[:, column+1]).sum()
        if diffs in [0, 1]:
            consider.append((column, diffs))
    for column, diffs in consider:
        left, right = column-1, column+2
        while (diffs <= 1) and (left >= 0) and (right < pattern.shape[1]):
            diffs += (pattern[:, left] != pattern[:, right]).sum()
            left -= 1
            right += 1
        if diffs == 1:
            return column + 1
    return 0

score = 0
for ipattern, pattern in enumerate(patterns):
    pattern = np.array(list(map(list, pattern)))
    if column := find_reflection2(pattern):
        score += column
    elif column := find_reflection2(pattern.T):
        score += 100 * column
    else:
        print("No reflection found for pattern", ipattern)

print("Score:", score)

pass
