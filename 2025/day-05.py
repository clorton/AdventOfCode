from pathlib import Path

import numpy as np

HERE = Path(__file__).parent

with Path(HERE / "day-05.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

iblank = lines.index("")

ranges = [list(map(int, line.split("-"))) for line in lines[:iblank]]
ingredients = [int(line) for line in lines[iblank+1:]]

fresh = 0
for ingredient in ingredients:
    for start, stop in ranges:
        if start <= ingredient <= stop:
            fresh += 1
            break

print(f"Part I: {fresh=}")

##### Part II #####

from collections import namedtuple

Range = namedtuple("Range", ["start", "stop"])

def overlaps(a, b):
    if a.stop < b.start-1 or a.start > b.stop+1:
        return False
    return True


def merge(a, b):
    return Range(min(a.start, b.start), max(a.stop, b.stop))

results = []
for start, stop in ranges:
    incoming = Range(start, stop)
    keep = []
    # Compare incoming range to ranges in result
    for check in results:
        if overlaps(incoming, check):
            incoming = merge(incoming, check)
        else:
            keep.append(check)
    keep.append(incoming)
    results = keep

total = 0
for range in results:
    total += range.stop - range.start + 1

print(f"Part II: {total=}")

print("done")
