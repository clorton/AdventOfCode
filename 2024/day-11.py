from pathlib import Path

import numpy as np

with (Path(__file__).parent / "day-11.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [ "125 17" ]

stones = list(map(int, lines[0].split(" ")))

"""
If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
"""

def blink(stones) -> list:
    blinked = []
    for stone in stones:
        if stone == 0:
            blinked.append(1)
        elif (half := len(strang := str(stone))) % 2 == 0:
            half //= 2
            blinked.append(int(strang[:half]))
            blinked.append(int(strang[half:]))
        else:
            blinked.append(stone * 2024)

    return blinked

test = list(stones)
for _ in range(6):
    test = blink(test)

print(f"After 6: {len(test)}")

test = list(stones)
for _ in range(25):
    test = blink(test)

print(f"After 25: {len(test)}")

def process(stone) -> list:
    if stone == 0:
        return [1]
    elif (half := len(strang := str(stone))) % 2 == 0:
        half //= 2
        return [int(strang[:half]), int(strang[half:])]

    return [stone * 2024]

from functools import lru_cache

@lru_cache(maxsize=1024*1024)
def length(stones, blinks) -> int:
    if blinks == 0:
        return len(stones)

    total = 0
    for stone in stones:
        total += length(tuple(blink([stone])), blinks - 1)

    return total

print(f"{length(tuple(stones), 75)}")

print("Done.")
