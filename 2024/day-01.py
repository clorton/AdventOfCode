from collections import Counter
from pathlib import Path

with (Path(__file__).parent / "day-01.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

list1 = [int(line.split(" ")[0]) for line in lines]
list2 = [int(line.split(" ")[-1]) for line in lines]

dist = 0
for a, b in zip(sorted(list1), sorted(list2)):
    dist += abs(a - b)

print(f"Part 1, total dist = {dist}")

counts = Counter(list2)
similarity = 0
for element in list1:
    similarity += element * counts[element]

print(f"Part2, similarity = {similarity}")

print("Done.")