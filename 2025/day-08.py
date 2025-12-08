from collections import namedtuple
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent

Point = namedtuple("Point", ["x", "y", "z"])

with Path(HERE / "day-08.txt").open("rt") as file:
    boxes = [Point(*list(map(int, line.split(",")))) for line in file.readlines()]

test = [Point(*list(map(int, line.split(",")))) for line in [
    "162,817,812",
    "57,618,57",
    "906,360,560",
    "592,479,940",
    "352,342,300",
    "466,668,158",
    "542,29,236",
    "431,825,988",
    "739,650,466",
    "52,470,668",
    "216,146,977",
    "819,987,18",
    "117,168,530",
    "805,96,715",
    "346,949,466",
    "970,615,88",
    "941,993,340",
    "862,61,35",
    "984,92,344",
    "425,690,689",
]]

dists = np.zeros((len(boxes), len(boxes)), dtype=np.float32)

for src, (sx, sy, sz) in enumerate(boxes):
    for dst, (dx, dy, dz) in enumerate(boxes):
        if dst <= src:
            continue
        dists[src, dst] = np.sqrt((sx - dx)**2 + (sy - dy)**2 + (sz - dz)**2)

indices = list(zip(*np.nonzero(dists)))

dists = [(dists[row,col], row, col) for row, col in indices]

dists = sorted(dists)

circuits = {box: set([box]) for box in range(len(boxes))}

for i, (d, boxa, boxb) in enumerate(dists[0:1000]):
    circuita = circuits[boxa]
    circuitb = circuits[boxb]
    newcircuit = circuita | circuitb
    for box in newcircuit:
        circuits[box] = newcircuit

lengths = {",".join(map(str,sorted(circuit))): len(circuit) for circuit in circuits.values()}

# print(f"{list(lengths.values())}")

descending = sorted(lengths.values(), reverse=True)
product = np.array(descending[0:3]).prod()
print(f"Part I:  {product=}")

##### Part II #####

circuits = {box: set([box]) for box in range(len(boxes))}

for i, (d, boxa, boxb) in enumerate(dists):
    circuita = circuits[boxa]
    circuitb = circuits[boxb]
    newcircuit = circuita | circuitb
    if len(newcircuit) < len(boxes):
        for box in newcircuit:
            circuits[box] = newcircuit
    else:
        print(f"Connected all boxes with {boxa} and {boxb}.")
        break

print(f"Part II: {(boxes[boxa].x * boxes[boxb].x)=}")

print("done")
