#! /usr/bin/env python3

from functools import reduce
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-05.txt").read_text()

lines = [
    "BFFFBBFRRR",   # row 70, column 7, seat ID 567
    "FFFBBBFRRR",   # row 14, column 7, seat ID 119
    "BBFFBBFRLL"    # row 102, column 4, seat ID 820
]

lines = text.split("\n")


# part 1
def seat_from_code(code: str) -> int:
    rows = list(range(128))
    for i in range(7):
        if code[i] == 'F':
            rows = rows[0:len(rows) // 2]
        else:
            rows = rows[len(rows)//2:]
    seats = list(range(8))
    for i in range(3):
        if code[7+i] == "L":
            seats = seats[0:len(seats) // 2]
        else:
            seats = seats[len(seats)//2:]
    row = rows[0]
    seat = seats[0]
    id = row * 8 + seat
    return id


maximum = 0
for seat in lines:
    maximum = max(maximum, seat_from_code(seat))

print(f"Maximum seat ID is {maximum}")

# part 2
seats = sorted(set([seat_from_code(seat) for seat in lines]))
for i, id in enumerate(seats):
    if id != i+seats[0]:
        print(f"Missing {id-1}.")
        break

print("done")
