#! /usr/bin/env python3

from collections import deque, namedtuple
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-09.txt").read_text()
lines = text.split("\n")
numbers = [int(string) for string in lines]


# part 1
def valid(number, values):
    for sample in values:
        if (number - sample) in values:
            return True
    return False


goal = 0
for index in range(25, len(numbers)):
    target = numbers[index]
    population = numbers[index-25:index]
    if not valid(target, population):
        goal = target
        print(f"Value {target} at index {index} is not valid.")
        break

# part 2
total = 0
start = 0
end = 0
while total != goal:
    total += numbers[end]
    end += 1
    while total > goal:
        total -= numbers[start]
        start += 1
smallest = min(numbers[start:end])
largest = max(numbers[start:end])
print(f"numbers {start} through {end} add up to {sum(numbers[start:end])}")
print(f"smallest is {smallest}, largest is {largest}, sum is {smallest + largest}")

print(".oO( done )")
