from pathlib import Path

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "day-22.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

"""
value = secret# * 64
mix
prune
value = secret# // 32
mix
prune
value = secret# * 2048
mix
prune

mix: secret# <- value xor secret#
prune: secret# <- secret# % 16777216
"""

def getnext(secret):
    secret ^= secret * 64
    secret %= 16777216
    secret ^= secret // 32
    secret %= 16777216
    secret ^= secret * 2048
    secret %= 16777216
    return secret

# secret = 123
# for _ in range(10):
#     secret = getnext(secret)
#     print(secret)

# secret = 1
# for _ in range(2000):
#     secret = getnext(secret)
# print("   1:", secret)

# secret = 10
# for _ in range(2000):
#     secret = getnext(secret)
# print("  10: ", secret)

# secret = 100
# for _ in range(2000):
#     secret = getnext(secret)
# print(" 100:", secret)

# secret = 2024
# for _ in range(2000):
#     secret = getnext(secret)
# print("2024:", secret)

total = 0
for line in tqdm(lines):
    secret = int(line)
    for _ in range(2000):
        secret = getnext(secret)
    total += secret

print(f"Part1: {total=}")

initial = list(map(int, lines))

# initial = [
#     1,
#     2,
#     3,
#     2024
# ]

secrets = np.zeros((len(initial), 2001), np.int32)
secrets[:,0] = initial
for i in tqdm(range(2000)):
    snext = secrets[:,i+1]
    snext[:] = secrets[:,i]
    snext ^= snext * 64
    snext %= 16777216
    snext ^= snext // 32
    snext %= 16777216
    snext ^= snext * 2048
    snext %= 16777216

prices = secrets % 10
changes = np.diff(prices).astype(np.int8)

seqmaps = [{} for _ in range(len(initial))]
for i in tqdm(range(len(initial))):
    seqmap = {}
    change = changes[i,:]
    for j in range(len(change)-4):
        seq = int(change[j:j+4].view(dtype=np.uint32)[0])
        if seq not in seqmap:
            seqmap[seq] = (i, prices[i,j+4])
    seqmaps[i] = seqmap

from collections import defaultdict
merged = {}
for seqmap in tqdm(seqmaps):
    for seq, (i, price) in seqmap.items():
        merged[seq] = merged.get(seq, 0) + price

maximum = max(merged.values())
print(f"Part2: {maximum=}")
_ = [print(f"{hex(k)}: {v}") for k, v in merged.items() if v == maximum]

print("Done.")