#! /usr/bin/env python3

from collections import defaultdict
from pathlib import Path

import numpy as np

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "example.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

seeds = { s:[s] for s in map(int, input[0].split(": ")[1].split()) }

maps = {}
for line in input[2:]:
    if len(line) == 0:
        continue
    if "map" in line:
        name = line.split()[0]
        mappings = []
        maps[name] = mappings
    else:
        dstart, sstart, length = map(int, line.split())
        mappings.append((sstart, dstart, length))

kind = "seed"
while kind != "location":
    key = list(filter(lambda k: k.startswith(kind), maps.keys()))[0]
    mapping = maps[key]
    for values in seeds.values():
        value = values[-1]
        result = value
        for sstart, dstart, length in mapping:
            if (value >= sstart) and (value < (sstart+length)):
                result = dstart+(value-sstart)
        values.append(result)
    kind = key.split("-to-")[1]

print(f"{min([values[-1] for values in seeds.values()])}")

#####

# consider each set of seeds
for i in range(len(input), 2):
    start = input[i]
    count = input[i+1]

    ranges = [(start, start, count)]
    mappings = []
    kind = "seed"
    while kind != "location":
        key = list(filter(lambda k: k.startswith(kind), maps.keys()))[0]
        while len(ranges):
            prior_left, target_left, map_count = ranges.pop()
            for input_left, output_left, length in maps[key]:
                input_right = input_left + length
                # if (input_right <= target_left) or (target_right <= input_left):
                #     # mapping doesn't overlap target range
                #     continue
                mapped_left = max(target_left, input_left)
                mapped_right = min(target_right, input_right)
                if mapped_right <= mapped_left:
                    continue
                left = (target_left,mapped_left,)
                center = (mapped_left,mapped_right,)
                right = (mapped_right,target_right,)

pass
