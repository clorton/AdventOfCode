#! /usr/bin/env python3

from functools import reduce

data = [1, 6, 7, 2, 4, 8, 3, 5, 9]
# data = [3, 8, 9, 1, 2, 5, 4, 6, 7]


# part 1
"""
def clockwise(label: int, cups: list):
    index = cups.index(label)
    index += 1
    index %= len(cups)
    return index


def move(cups: list, current: int):

    size = len(cups)
    removed = [cups.pop(clockwise(current, cups)) for _ in range(3)]
    predecessor = current - 1 if current > 1 else max(cups)
    while predecessor in removed:
        predecessor = predecessor - 1 if predecessor > 1 else max(cups)
    for _ in range(3):
        cups.insert(cups.index(predecessor) + 1, removed.pop())
    current = cups[clockwise(current, cups)]
    return cups, current


cups = [label for label in data]
current = cups[0]
for _ in range(100):
    cups, current = move(cups, current)
print(f"labels = {cups}")
"""

# part 1.5
cups = {}
for index, label in enumerate(data):
    cups[label] = data[(index+1) % len(data)]


def do_move(current, cups):
    p_removed = cups[current]
    cups[current] = cups[cups[cups[p_removed]]]
    removed = [p_removed, cups[p_removed], cups[cups[p_removed]]]
    destination = current - 1 if current > 1 else len(cups)
    while destination in removed:
        destination = destination - 1 if destination > 1 else len(cups)
    cups[cups[cups[p_removed]]] = cups[destination]
    cups[destination] = p_removed
    new = cups[current]

    return new, cups

current = data[0]
for _ in range(100):
    current, cups = do_move(current, cups)
current = 1
labels = []
for _ in range(len(cups)-1):
    current = cups[current]
    labels.append(current)
print(f"labels = {labels}")


# part 2
cups = {}
for index, label in enumerate(data):
    cups[label] = data[(index+1) % len(data)]
for extra in range(len(data), 1_000_001):
    cups[extra] = extra + 1
cups[1_000_000] = data[0]

current = data[0]
for _ in range(10_000_000):
    print(f"{_}") if _ % 100_000 == 0 else None
    current, cups = do_move(current, cups)
cw1 = cups[1]
cw2 = cups[cw1]
print(f"..., 1, {cw1}, {cw2}, ... -> {cw1 * cw2}")

print(".oO( done )")
