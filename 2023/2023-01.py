#! /usr/bin/env python3

from pathlib import Path

import numpy as np

WORKING_DIRECTORY = Path(__file__).parent.absolute()

with (WORKING_DIRECTORY / "2023-01.txt").open("r") as file:
    input = [line.strip() for line in file.readlines()]

digits = [list(filter(str.isdigit, list(line))) for line in input]

numbers = [int(entry[0]+entry[-1]) for entry in digits]

print(f"{sum(numbers)=}")

words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

input = [line.replace("oneight", "oneeight") for line in input]
input = [line.replace("twone", "twoone") for line in input]
input = [line.replace("threeight", "threeeight") for line in input]
input = [line.replace("fiveight", "fiveeight") for line in input]
input = [line.replace("sevenine", "sevennine") for line in input]
input = [line.replace("eightwo", "eighttwo") for line in input]
input = [line.replace("eighthree", "eightthree") for line in input]
input = [line.replace("nineight", "nineeight") for line in input]

for i, word in enumerate(words):
    for j, line in enumerate(input):
        input[j] = line.replace(word, str(i))

digits = [list(filter(str.isdigit, list(line))) for line in input]
numbers = [int(entry[0]+entry[-1]) for entry in digits]
print(f"{sum(numbers)=}")

pass
