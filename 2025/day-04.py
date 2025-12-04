from pathlib import Path

import numpy as np

HERE = Path(__file__).parent

with Path(HERE / "day-04.txt").open("rt") as file:
    lines = [list(map(ord, line.strip())) for line in file.readlines()]

test = [
    "..@@.@@@@.",
    "@@@.@.@.@@",
    "@@@@@.@.@@",
    "@.@@@@..@.",
    "@@.@@@@.@@",
    ".@@@@@@@.@",
    ".@.@.@.@@@",
    "@.@@@.@@@@",
    ".@@@@@@@@.",
    "@.@.@@@.@.",
]
test = [list(map(ord, line)) for line in test]

# lines = test

bufferd = np.zeros((len(lines)+2, len(lines[0])+2), dtype=np.uint8)
bufferd[1:-1,1:-1] = np.array(lines, dtype=np.uint8)

FREE = ord(".")
ROLL = ord("@")

counts = np.zeros_like(bufferd, dtype=np.int32)
for row in range(1, len(lines)+1):
    for col in range(1, len(lines[0])+1):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr or dc:
                    if bufferd[row+dr,col+dc] == ROLL:
                        count += 1
        counts[row,col] = count

total = ((bufferd == ROLL) & (counts < 4)).sum()

"""
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.
"""

print(f"Part I: {total=}")

##### Part II #####

removed = 0
removable = np.nonzero((bufferd == ROLL) & (counts < 4))
while len(removable[0]): # > 0
    for row, col in zip(removable[0], removable[1]):
        bufferd[row,col] = FREE
        removed += 1
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr or dc:
                    counts[row+dr,col+dc] -= 1
    removable = np.nonzero((bufferd == ROLL) & (counts < 4))

print(f"Part II: {removed=}")

print("done")
