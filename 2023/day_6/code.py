#! /usr/bin/env python3

from collections import defaultdict
from pathlib import Path

import numpy as np

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

times = list(map(int, input[0].split(":")[1].strip().split()))
bests = list(map(int, input[1].split(":")[1].strip().split()))

races = list(zip(times, bests))

product = 1
for race in races:
    time, best = race
    wins = 0
    for seconds in range(1,time):
        v = seconds
        t = time - seconds
        distance = v*t
        if distance > best:
            wins += 1
    product *= wins

print(f"{product=}")

time = int("".join(map(str, times)))
best = int("".join(map(str, bests)))

# wins = 0
# for seconds in range(1,time):
#     v = seconds
#     t = time - seconds
#     distance = v*t
#     if distance > best:
#         wins += 1

# print(f"{wins=}")

# v+t = time
# t = time - v
# distance = v*t = v(time - v) = v*time - v^2
# v*v - v*time + best = 0

a = np.int64(1)
b = np.int64(-time)
c = np.int64(best)

minimum = np.ceil((-b - np.sqrt(b*b-4*a*c))/(2*a))
maximum = np.floor((-b + np.sqrt(b*b-4*a*c))/(2*a))

print(f"{np.int64(maximum-minimum+1)=}")

pass
