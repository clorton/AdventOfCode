from pathlib import Path

import numpy as np

HERE = Path(__file__).parent

with Path(HERE / "day-03.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

banks = [[int(c) for c in line] for line in lines]

test = [
    [9,8,7,6,5,4,3,2,1,1,1,1,1,1,1], # 98
    [8,1,1,1,1,1,1,1,1,1,1,1,1,1,9], # 89
    [2,3,4,2,3,4,2,3,4,2,3,4,2,7,8], # 78
    [8,1,8,1,8,1,9,1,1,1,1,2,1,1,1], # 92
] # 357

total = 0
for bank in banks: # test:
    imax = 0
    for index in range(1, len(bank)-1):
        if bank[index] > bank[imax]:
            imax = index
    first = bank[imax]
    second = max(bank[imax+1:])
    # print(f"{bank} {(first,second)}")
    total += first * 10 + second

print(f"Part I: {total=}")

total = 0
for bank in banks: # test:
    bank = np.array(bank, np.uint8)
    istart = 0
    joltage = np.uint64(0)
    for idigit in range(12):
        isuffix = len(bank) - (11 - idigit)
        imax = np.argmax(bank[istart:isuffix])
        istart += imax
        best = bank[istart]
        joltage = joltage * 10 + best
        istart += 1

    # print(f"{bank} {(joltage)}")
    total += joltage

"""
987654321111111  987654321111
811111111111119  811111111119
234234234234278  434234234278
818181911112111  888911112111
The total output joltage is now much larger: 987654321111 + 811111111119 + 434234234278 + 888911112111 = 3121910778619.
"""

print(f"Part II: {total=}")

print("done")
