#! /usr/bin/env python3

from collections import defaultdict
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip().split() for line in file.readlines()]

input = [[line[0], list(map(int,line[1].split(",")))] for line in input]

arrangements = []
for i in tqdm(range(len(input))):
    line, counts = input[i]
    line = np.array(list(line))
    line[line == "."] = " "
    positions = (line == "?").nonzero()[0]
    bits = len(positions)
    if bits > 0:
        permutations = 0
        for i in range(2**bits):
            fill = np.array(list(format(i, f"0{bits}b")))
            fill[fill == "0"] = " "
            fill[fill == "1"] = "#"
            np.put(line, positions, fill)
            runs = list(map(len,"".join(line).split()))
            if runs == counts:
                permutations += 1
    else:
        permutations = 1
    arrangements.append(permutations)

print(f"{sum(arrangements)} arrangements found for {len(arrangements)} lines")

pass
