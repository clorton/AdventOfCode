#! /usr/bin/env python3

from collections import defaultdict, deque, namedtuple
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

Point = namedtuple("Point", ["x", "y", "z"])

input = [line.split("~") for line in input]

input = [[Point(*map(int, start.split(","))), Point(*map(int, end.split(",")))] for [start, end] in input]

maxx = max(map(lambda l: l[0].x, input))
maxx = max(maxx, max(map(lambda l: l[1].x, input)))
maxy = max(map(lambda l: l[0].y, input))
maxy = max(maxy, max(map(lambda l: l[1].y, input)))
maxz = max(map(lambda l: l[0].z, input))
maxz = max(maxz, max(map(lambda l: l[1].z, input)))

print(f"maxx: {maxx}, maxy: {maxy}, maxz: {maxz}")
print(f"{maxx * maxy * maxz}")

cube = np.zeros((maxx + 1, maxy + 1, maxz + 1), dtype=np.int32)

for index, [start, end] in enumerate(input):
    assert start.x <= end.x
    assert start.y <= end.y
    assert start.z <= end.z
    cube[start.x:end.x + 1, start.y:end.y + 1, start.z:end.z + 1] = index+1

print("Dropping blocks...")
dropped = True
while dropped:
    dropped = False
    for iblock in range(1, len(input)+1):
        indices = np.nonzero(cube == iblock)
        minz = np.min(indices[2])
        if minz > 1:
            if np.all(indices[2] == minz):
                # horizontal block, check all blocks
                if np.all(cube[indices[0], indices[1], minz - 1] == 0):
                    cube[indices[0], indices[1], minz] = 0
                    cube[indices[0], indices[1], minz-1] = iblock
                    dropped = True
                    # print(f"dropped {iblock} to {minz-1}")
            else:
                # vertical block, check only one block
                if cube[indices[0][0], indices[1][0], minz - 1] == 0:
                    maxz = np.max(indices[2])
                    cube[indices[0][0], indices[1][0], maxz] = 0
                    cube[indices[0][0], indices[1][0], minz-1] = iblock
                    dropped = True
                    # print(f"dropped {iblock} to {minz-1}")
print("Done dropping blocks.")

print("Calculating supports and restsons...")
supports = {}
restson = {}
for iblock in (pbar := tqdm(range(1, len(input)+1))):
    indices = np.nonzero(cube == iblock)
    minz = np.min(indices[2])
    maxz = np.max(indices[2])
    if np.all(indices[2] == minz):
        # horizontal block, check all blocks
        # supports
        if minz < cube.shape[2] - 1:
            others = set(cube[indices[0], indices[1], minz+1])
            others.discard(0)   # doesn't count
            supports[iblock] = others
        # restson
        if minz > 1:
            others = set(cube[indices[0], indices[1], minz-1])
            others.discard(0)
            restson[iblock] = others
    else:
        # vertical block, check only one block
        # supports
        maxz = np.max(indices[2])
        if maxz < cube.shape[2] - 1:
            others = set([cube[indices[0][0], indices[1][0], maxz+1]])
            others.discard(0)
            supports[iblock] = others
        # restson
        if minz > 1:
            others = set([cube[indices[0][0], indices[1][0], minz-1]])
            others.discard(0)
            restson[iblock] = others
print("Done calculating supports and restsons.")

print("Calculating disintegrations...")
disintegrate = 0
for iblock in (pbar := tqdm(range(1, len(input)+1))):
    if iblock not in supports:
        disintegrate += 1
        # pbar.set_description(f"disintegrate {iblock} (doesn't support anything)")
    elif all([len(restson[supported]) > 1 for supported in supports[iblock]]):
        disintegrate += 1
        # pbar.set_description(f"disintegrate {iblock} (all supports have more than one restson)")

print(f"disintegrate: {disintegrate}")

print("Calculating totalfall...")
totalfall = 0
for iblock in (pbar := tqdm(range(1, len(input)+1))):
    supporters = set()
    consider = deque([iblock])
    newfall = 0
    while consider:
        block = consider.pop()  # pop from the right
        supporters.add(block)
        for check in supports[block]:
            if (check not in supporters) and (restson[check] <= supporters):
                newfall += 1
                supporters.add(check)
                consider.appendleft(check)  # add to the left
    totalfall += newfall
    # print(f"Disintegrating {iblock} will cause {newfall} blocks to fall.")

print(f"totalfall: {totalfall}")

pass
