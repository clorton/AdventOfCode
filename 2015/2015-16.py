import re
from pathlib import Path

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "2015-16.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

mfcsam = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

sues = {}
for line in lines:
    sue, props = line.split(": ", 1)
    props = re.findall(r"(\w+): (\d+)", props)
    sues[sue] = {prop: int(value) for prop, value in props}

for sue in sues:
    if all(sues[sue][prop] == mfcsam[prop] for prop in sues[sue]):
        print(sue)
        # break

for sue in sues:
    match = True
    for prop in sues[sue]:
        if prop in ("cats", "trees"):
            if sues[sue][prop] <= mfcsam[prop]:
                match = False
                break
        elif prop in ("pomeranians", "goldfish"):
            if sues[sue][prop] >= mfcsam[prop]:
                match = False
                break
        elif sues[sue][prop] != mfcsam[prop]:
            match = False
            break
    if match:
        print(sue)
        # break

print("Done.")
