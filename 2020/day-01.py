#! /usr/bin/env python3

from datetime import datetime
from pathlib import Path

input = Path(__file__).parent.absolute() / "day-01.txt"
data = [int(element) for element in input.read_text().split("\n")]
# optionally, sort the data and walk from each end updating "pointers" until the correct pair is found
for i, element in enumerate(data):
    # brute force search through remaining data
    for pair in data[i+1:]:
        if element + pair == 2020:
            print(f"{element} * {pair} = {element * pair}")

# sort the data, otherwise we need an O(n^3) search, I think
data = sorted(data)
data.reverse()
found = False
start = datetime.now()
for i, first in enumerate(data):                # start with large values
    for j, second in enumerate(data[-1:i:-1]):  # look for small values
        if first + second >= 2020:              # if first + second >= 2020, no third value will work, abandon this loop
            break
        # for third in data[j-2:i:-1]:
        for third in data[-1:j-2:-1]:           # look for another small value...
            if first + second + third < 2020:   # if baby bear, continue
                continue
            if first + second + third == 2020:  # if mama bear, we are done
                print(f"{first} * {second} * {third} = {first * second * third}")
                found = True
                break
            if first + second + third > 2020:   # if papa bear, no point continuing, thirds just get bigger, abandon this loop
                break
        if found:
            break
    if found:
        break
finish = datetime.now()
print(f"Elapsed time {finish - start}")
