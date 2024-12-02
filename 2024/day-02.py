from collections import Counter
from pathlib import Path

import numpy as np

with (Path(__file__).parent / "day-02.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

lines = [list(map(int, line.split(" "))) for line in lines]

diffs = [np.diff(line) for line in lines]

def check(report):
    minimum = min(report)
    maximum = max(report)
    if (minimum > 0) or (maximum < 0):
        minimum = min(map(abs, report))
        maximum = max(map(abs, report))
        if (minimum > 0) and (maximum < 4):
              return True
    
    return False

safe = 0
for diff in diffs:
    if check(diff):
        safe += 1

print(f"{safe} reports are safe")

safe = 0
for line, diff in zip(lines, diffs):
    if check(diff):
        safe += 1
    else:
        for i in range(len(line)):
            dampened = list(line)
            del dampened[i]
            if check(np.diff(dampened)):
                safe += 1
                break

print(f"{safe} reports are safe")
