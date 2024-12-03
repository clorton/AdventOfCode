from pathlib import Path
import re

# import numpy as np

with (Path(__file__).parent / "day-03.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

sum = 0
for line in lines:
    finds = re.findall(r"mul\(([0-9]+),([0-9]+)\)", line)
    for a,b in finds:
        sum += int(a) * int(b)

print(f"{sum=}")

do = True
sum = 0
for line in lines:
    finds = re.findall(r"mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)", line)
    for find in finds:
        if find == "do()":
            do = True
        elif find == "don't()":
            do = False
        else:
            if do:
                a,b = re.findall("[0-9]+", find)
                sum += int(a) * int(b)

print(f"{sum=}")

print("Done.")
