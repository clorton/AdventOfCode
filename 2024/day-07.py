from itertools import product
from pathlib import Path
import re

import numpy as np

with (Path(__file__).parent / "day-07.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "190: 10 19",
#     "3267: 81 40 27",
#     "83: 17 5",
#     "156: 15 6",
#     "7290: 6 8 6 15",
#     "161011: 16 10 13",
#     "192: 17 8 14",
#     "21037: 9 7 18 13",
#     "292: 11 6 16 20",
# ]

lines = [tuple(list(line.split(": "))) for line in lines]
tests = [(int(line[0]), list(map(int, line[1].split(" ")))) for line in lines]

total = 0
for goal, numbers in tests:
    for combination in product("+*", repeat=len(numbers)-1):
        combination = list(combination)
        accumulator = numbers[0]
        for operation, argument in zip(combination, numbers[1:]):
            if operation == "+":
                accumulator += argument
            elif operation == "*":
                accumulator *= argument
            else:
                raise RuntimeError(f"Unknown operation {operation}")
        if accumulator == goal:
            # print(f"Solved: {goal} = {numbers} with {combination}")
            total += accumulator
            break

print(f"Total = {total}")

total = 0
for goal, numbers in tests:
    for combination in product("+*|", repeat=len(numbers)-1):
        # combination = list(combination)
        accumulator = numbers[0]
        for operation, argument in zip(combination, numbers[1:]):
            if operation == "+":
                accumulator += argument
            elif operation == "*":
                accumulator *= argument
            elif operation == "|":
                accumulator = int(str(accumulator)+str(argument))
            else:
                raise RuntimeError(f"Unknown operation {operation}")
            # # Useful?
            # if accumulator > goal:
            #     break
        if accumulator == goal:
            # print(f"Solved: {goal} = {numbers} with {combination}")
            total += accumulator
            break

print(f"Total = {total}")

print("Done.")
