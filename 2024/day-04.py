from pathlib import Path
import re

import numpy as np

with (Path(__file__).parent / "day-04.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# horizontal
count = 0
for line in lines:
    fa = re.findall("XMAS", line)
    count += len(fa)
    af = re.findall("SAMX", line)
    count += len(af)

# vertical
a = np.array(list(map(list, lines)))
t = a.T
for line in ["".join(row) for row in t]:
    fa = re.findall("XMAS", line)
    count += len(fa)
    af = re.findall("SAMX", line)
    count += len(af)

# southeast
for row in range(a.shape[0]-3):
    for col in range(a.shape[1]-3):
        if a[row,col] == "X" and a[row+1,col+1] == "M" and a[row+2,col+2] == "A" and a[row+3,col+3] == "S":
            count += 1
        if a[row,col] == "S" and a[row+1,col+1] == "A" and a[row+2,col+2] == "M" and a[row+3,col+3] == "X":
            count += 1

# southwest
for row in range(a.shape[0]-3):
    for col in range(3, a.shape[1]):
        if a[row,col] == "X" and a[row+1,col-1] == "M" and a[row+2,col-2] == "A" and a[row+3,col-3] == "S":
            count += 1
        if a[row,col] == "S" and a[row+1,col-1] == "A" and a[row+2,col-2] == "M" and a[row+3,col-3] == "X":
            count += 1

print(f"{count=}")

uldr = np.zeros_like(a)
aay = (a == "A").astype(np.uint8)
ems = (a == "M").astype(np.uint8)
ess = (a == "S").astype(np.uint8)

mas = ems[:-2,:-2] + aay[1:-1,1:-1] + ess[2:,2:]    # MAS down right
sam = ems[2:,2:] + aay[1:-1,1:-1] + ess[:-2,:-2]    # SAM down right

backslash = (mas == 3) | (sam == 3)  # MAS or SAM "\"

mas = ems[2:,:-2] + aay[1:-1,1:-1] + ess[:-2,2:]    # MAS up right
sam = ems[:-2,2:] + aay[1:-1,1:-1] + ess[2:,:-2]    # SAM up right

slash = (mas == 3) | (sam == 3)  # MAS or SAM "/"

xmas = (backslash & slash)    # MAS|SAM "\" and MAS|SAM "/" == X-MAS

print(f"{xmas.sum()=}")

print("Done.")
