#! /usr/bin/env python3

from datetime import datetime

numbers = [9, 3, 1, 0, 8, 4]
# numbers = [2, 1, 3]

# part 1
start = datetime.now()
log = {n: [i] for i, n in enumerate(numbers)}

last = numbers[-1]
for turn in range(len(numbers), 2020):
    if len(log[last]) == 1:
        last = 0
    else:
        last = log[last][1] - log[last][0]
    if last in log:
        log[last] = [log[last][-1], turn]
    else:
        log[last] = [turn]
finish = datetime.now()

print(f"Last number spoken was {last} ({finish - start}).")

# part 2
start = datetime.now()
log = {n: [i] for i, n in enumerate(numbers)}

last = numbers[-1]
for turn in range(len(numbers), 30_000_000):
    if len(log[last]) == 1:
        last = 0
    else:
        last = log[last][1] - log[last][0]
    if last in log:
        log[last] = [log[last][-1], turn]
    else:
        log[last] = [turn]
finish = datetime.now()

print(f"Last number spoken was {last} ({finish - start}).")

print(".oO( done )")
