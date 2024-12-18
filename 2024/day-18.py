from pathlib import Path
# import re

import numpy as np

with (Path(__file__).parent / "day-18.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

width = height = 71
count = 1024

# lines = [
#     "5,4",
#     "4,2",
#     "4,5",
#     "3,0",
#     "2,1",
#     "6,3",
#     "2,4",
#     "1,5",
#     "0,6",
#     "3,3",
#     "2,6",
#     "5,1",
#     "1,2",
#     "5,5",
#     "2,5",
#     "6,5",
#     "1,4",
#     "0,4",
#     "6,4",
#     "1,1",
#     "6,1",
#     "1,0",
#     "0,5",
#     "1,6",
#     "2,0",
# ]

# width = height = 7
# count = 12

memory = np.zeros((width, height), dtype=np.uint8)
for i, line in enumerate(lines):
    if i < count:
        x, y = map(int, line.split(","))
        memory[y, x] = 1

for row in memory:
    print("".join(map(str, row)))

from collections import namedtuple
Pt = namedtuple("Pt", ["x", "y", "d"])

test = [(Pt(0, 0, 0))]
best = np.full((width, height), width*height, dtype=np.uint32)
while test:
    x, y, d = test.pop(0)
    if memory[y, x] == 0 and d < best[y, x]:
        best[y, x] = d
        test.append(Pt(x - 1, y, d+1)) if x > 0 else None
        test.append(Pt(x + 1, y, d+1)) if x < width - 1 else None
        test.append(Pt(x, y - 1, d+1)) if y > 0 else None
        test.append(Pt(x, y + 1, d+1)) if y < height - 1 else None

print(f"Best: {best[height-1, width-1]}")

def solve(memory):
    test = [(Pt(0, 0, 0))]
    height, width = memory.shape
    best = np.full((width, height), width*height, dtype=np.uint32)
    while test:
        x, y, d = test.pop(0)
        if memory[y, x] == 0 and d < best[y, x]:
            best[y, x] = d
            test.append(Pt(x - 1, y, d+1)) if x > 0 else None
            test.append(Pt(x + 1, y, d+1)) if x < width - 1 else None
            test.append(Pt(x, y - 1, d+1)) if y > 0 else None
            test.append(Pt(x, y + 1, d+1)) if y < height - 1 else None
    return best[height-1, width-1] < width*height

from tqdm import tqdm

for i in tqdm(range(1024, len(lines)+1)):
    x, y = map(int, lines[i].split(","))
    memory[y, x] = 1
    if not solve(memory):
        print(f"Failed at {i} ({x}, {y})")
        break

print("Done")
