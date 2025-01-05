import re
from pathlib import Path

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "2015-13.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "Alice would gain 54 happiness units by sitting next to Bob.",
#     "Alice would lose 79 happiness units by sitting next to Carol.",
#     "Alice would lose 2 happiness units by sitting next to David.",
#     "Bob would gain 83 happiness units by sitting next to Alice.",
#     "Bob would lose 7 happiness units by sitting next to Carol.",
#     "Bob would lose 63 happiness units by sitting next to David.",
#     "Carol would lose 62 happiness units by sitting next to Alice.",
#     "Carol would gain 60 happiness units by sitting next to Bob.",
#     "Carol would gain 55 happiness units by sitting next to David.",
#     "David would gain 46 happiness units by sitting next to Alice.",
#     "David would lose 7 happiness units by sitting next to Bob.",
#     "David would gain 41 happiness units by sitting next to Carol.",
# ]

info = {}
for line in lines:
    match = re.match(r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).", line)
    if not match:
        raise ValueError(f"Invalid line: {line}")
    name1, sign, value, name2 = match.groups()
    value = int(value)
    if sign == "lose":
        value = -value
    info[(name1, name2)] = value

guests = sorted(set([name1 for name1, name2 in info.keys()]))

from itertools import permutations
most = 0
seating = None
for permutation in tqdm(permutations(guests)):
    total = 0
    for i, guest in enumerate(permutation):
        left = permutation[(i + 1) % len(permutation)]
        right = permutation[i - 1]
        total += info[(guest, left)]
        total += info[(guest, right)]
    if total > most:
        most = total
        seating = permutation

print(f"Part 1: {most}\n\t{seating}")

for guest in guests:
    info[("Christopher", guest)] = 0
    info[(guest, "Christopher")] = 0

guests.append("Christopher")

most = 0
seating = None
for permutation in tqdm(permutations(guests)):
    total = 0
    for i, guest in enumerate(permutation):
        left = permutation[(i + 1) % len(permutation)]
        right = permutation[i - 1]
        total += info[(guest, left)]
        total += info[(guest, right)]
    if total > most:
        most = total
        seating = permutation

print(f"Part 2: {most}\n\t{seating}")

print("Done.")
