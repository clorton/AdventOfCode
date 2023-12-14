#! /usr/bin/env python3

from collections import defaultdict
from hashlib import sha256
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

platform = np.array(list(map(list, input)))

hashes = {}
h = sha256()
# copy = h.copy()
# copy.update(platform.data)
# hashes[copy.hexdigest()] = 0

def tnorth(platform):
    for row in range(1, platform.shape[0]):
        for col in range(0, platform.shape[1]):
            if platform[row, col] == "O":
                rowp = row - 1
                while rowp >= 0:
                    if platform[rowp, col] == ".":
                        platform[rowp, col] = "O"
                        platform[rowp+1, col] = "."
                    else:
                        break
                    rowp -= 1
    return

tnorth(platform=platform)

def calc_load(platform):
    load = 0
    for row in tqdm(range(0, platform.shape[0])):
        load += (platform.shape[0] - row) * (platform[row, :] == "O").sum()
    return load

load = calc_load(platform=platform)
print(f"{load=}")

def tsouth(platform):
    for row in range(platform.shape[0]-2, -1, -1):
        for col in range(0, platform.shape[1]):
            if platform[row, col] == "O":
                rowp = row + 1
                while rowp < platform.shape[0]:
                    if platform[rowp, col] == ".":
                        platform[rowp, col] = "O"
                        platform[rowp-1, col] = "."
                    else:
                        break
                    rowp += 1
    return

def teast(platform):
    for col in range(platform.shape[1]-2, -1, -1):
        for row in range(0, platform.shape[0]):
            if platform[row, col] == "O":
                colp = col + 1
                while colp < platform.shape[1]:
                    if platform[row, colp] == ".":
                        platform[row, colp] = "O"
                        platform[row, colp-1] = "."
                    else:
                        break
                    colp += 1
    return

def twest(platform):
    for col in range(1, platform.shape[1]):
        for row in range(0, platform.shape[0]):
            if platform[row, col] == "O":
                colp = col - 1
                while colp >= 0:
                    if platform[row, colp] == ".":
                        platform[row, colp] = "O"
                        platform[row, colp+1] = "."
                    else:
                        break
                    colp -= 1
    return

for cycle in tqdm(range(2, 1_000_000_001)):
    tnorth(platform=platform)
    twest(platform=platform)
    tsouth(platform=platform)
    teast(platform=platform)
    copy = h.copy()
    copy.update(platform.data)
    key = copy.hexdigest()
    if key in hashes:
        print(f"{cycle=} {hashes[key]=}")
        break
    hashes[key] = cycle

start = hashes[key]
recycle = cycle - start
full = (1_000_000_000 - start) // recycle
goal = 1_000_000_000 - (recycle * full)

platform = np.array(list(map(list, input)))

for cycle in tqdm(range(1, goal+1)):
    tnorth(platform=platform)
    twest(platform=platform)
    tsouth(platform=platform)
    teast(platform=platform)
    # load = calc_load(platform=platform)
    # print(f"{cycle=} {load=}")
    # for row in platform:
    #     print("".join(row))
    # print()

print(f"Calculating load for {cycle=}")
load = calc_load(platform=platform)
print(f"{load=}")

pass
