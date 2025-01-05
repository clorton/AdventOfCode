import re
from pathlib import Path

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "2015-14.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
#     "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.",
# ]

info = {}
for line in lines:
    match = re.match(r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.", line)
    name, speed, tfly, trest = match.groups()
    info[name] = (int(speed), int(tfly), int(trest))

def distance(speed, tfly, trest, time):
    cycle = tfly + trest
    full_cycles = time // cycle
    remaining = time % cycle
    return full_cycles * tfly * speed + min(remaining, tfly) * speed

# time = 1000
time = 2503

print("Part 1:")
for name, (speed, tfly, trest) in info.items():
    print(f"{name:7}: {distance(speed, tfly, trest, time)}")
print()

names = sorted(list(info.keys()))

traces = np.zeros((len(names), time), dtype=np.int32)
for i, name in enumerate(names):
    (speed, tfly, trest) = info[name]
    for t in range(time):
        traces[i, t] = distance(speed, tfly, trest, t+1)

scores = np.zeros((len(info), time), dtype=np.int32)
for t in range(time):
    scores[:, t] = traces[:, t] == traces[:, t].max()

print("Part 2:")
for name, score in zip(names, scores.sum(axis=1)):
    print(f"{name:7}: {score}")
print()

print("Done.")
