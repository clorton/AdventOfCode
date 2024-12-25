from pathlib import Path

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "day-25.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "#####",
#     ".####",
#     ".####",
#     ".####",
#     ".#.#.",
#     ".#...",
#     ".....",
#     "",
#     "#####",
#     "##.##",
#     ".#.##",
#     "...##",
#     "...#.",
#     "...#.",
#     ".....",
#     "",
#     ".....",
#     "#....",
#     "#....",
#     "#...#",
#     "#.#.#",
#     "#.###",
#     "#####",
#     "",
#     ".....",
#     ".....",
#     "#.#..",
#     "###..",
#     "###.#",
#     "###.#",
#     "#####",
#     "",
#     ".....",
#     ".....",
#     ".....",
#     "#....",
#     "#.#..",
#     "#.#.#",
#     "#####",
# ]

locks = []
keys = []

item = []
for i, line in enumerate(lines):
    if not line:
        continue
    item.append(line)
    if i % 8 == 6:
        a = np.array([list(map(ord, l)) for l in item])
        if item[0] == "#####":
            h = (a[1:] == ord("#")).sum(axis=0)
            locks.append(h)
        else:
            h = (a[:-1] == ord("#")).sum(axis=0)
            keys.append(h)
        item = []

print(f"Locks: {len(locks)}")
print(f"Keys: {len(keys)}")

from itertools import product

fits = 0 
for key, lock in product(keys, locks):
    if np.max(key+lock) < 6:
        fits += 1
print(f"Fits: {fits}")

print("Done.")
