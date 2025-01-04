from pathlib import Path

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "2015-10.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

line = lines[0]

# lines = [
# ]

# line = "1"

def look(string):
    counts = []
    count = 0
    for c in string:
        if count == 0:
            current = c
            count = 1
            continue
        if c == current:
            count += 1
        else:
            counts.append((count, current))
            current = c
            count = 1
    counts.append((count, current))
    return counts

def say(counts):
    return "".join(f"{count}{char}" for count, char in counts)

def do(s, n):
    for _ in range(n):
        print(f"{s} ({len(s)}): ", end="")
        s = say(look(s))
        print(f"{s} ({len(s)})")

for _ in range(51):
    # print(f"{line} ({len(line)}): ", end="")
    # print(f"({len(line):6}): {line}")
    print(f"{_:2}: {len(line):6}")
    line = say(look(line))
    # print(f"{line} ({len(line)})")

print("Done.")
