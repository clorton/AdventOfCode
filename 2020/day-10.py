#! /usr/bin/env python3

from collections import deque, namedtuple
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-10.txt").read_text()
lines = text.split("\n")
adapters = sorted([int(string) for string in lines])


# part 1
sources = [0]
sources.extend(adapters)
diffs = [0]*len(adapters)
ones = 0
threes = 0
for i in range(len(adapters)):
    diff = adapters[i] - sources[i]
    diffs[i] = diff
    ones += 1 if diff == 1 else 0
    threes += 1 if diff == 3 else 0
print(f"{ones} ones and {threes} threes -> {ones*(threes+1)}")

# part 2

# adapters = sorted([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4])

adapters.append(adapters[-1] + 3)
temp = [0]
temp.extend(adapters)
adapters = temp
options = {adapters[-1]: 1}
for index in range(len(adapters)-2, -1, -1):
    count = 0
    for test in range(index+1, min(len(adapters), index+4)):
        if (adapters[test] - adapters[index]) <= 3:
            count += options[adapters[test]]
    options[adapters[index]] = count
print(f"Source has {options[0]} options.")

print(".oO( done )")
