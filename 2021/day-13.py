#! /usr/bin/env python3

from collections import defaultdict, namedtuple
from datetime import datetime
from pathlib import Path

import numpy as np

with Path("13.txt").open("r") as handle:
    lines = list([line.strip() for line in handle.readlines()])

"""
lines = [
    "6,10",
    "0,14",
    "9,10",
    "0,3",
    "10,4",
    "4,11",
    "6,0",
    "6,12",
    "4,1",
    "0,13",
    "10,12",
    "3,4",
    "3,0",
    "8,4",
    "1,10",
    "2,14",
    "8,10",
    "9,0",
    "fold along y=7",
    "fold along x=5"
]
"""

t_start = datetime.now()

Dot = namedtuple("Dot", ["x", "y"])

dots = list(filter(lambda p: "," in p, lines))
dots = list(map(lambda l: list(map(int, l.split(","))), dots))
dots = list(map(lambda d: Dot(*d), dots))
folds = list(filter(lambda p: len(p) and ("," not in p), lines))
folds = list(map(lambda l: l.split()[2].split("="), folds))

max_x = max([int(fold[1]) for fold in folds if fold[0] == "x"])
max_y = max([int(fold[1]) for fold in folds if fold[0] == "y"])

width = max_x * 2 + 1
height = max_y * 2 + 1

paper = np.zeros((height, width), dtype=np.int32)
for x, y in dots:
    paper[y, x] = 1


def do_fold(paper, fold):
    axis = fold[0]
    value = int(fold[1])
    if axis == "x":
        return paper[:, 0:value] + np.fliplr(paper)[:, 0:value]
    else:   # "y"
        return paper[0:value, :] + np.flipud(paper)[0:value, :]


paper = do_fold(paper, folds[0])

print(f"{np.count_nonzero(paper)=}")

for fold in folds[1:]:
    paper = do_fold(paper, fold)

paper[paper != 0] = ord("*")
paper[paper == 0] = ord(" ")

for row in range(paper.shape[0]):
    print(f"{''.join(map(chr, map(int, paper[row, :])))}")

# print(f"{paper}")

t_end = datetime.now()

print(f"{t_end-t_start}")

pass
