from pathlib import Path

HERE = Path(__file__).parent

with Path(HERE / "day-01.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

actions = [(line[0], int(line[1:])) for line in lines]

dial = 50
count = 0
for (dir, dist) in actions:
    if dir == "R":
        dial -= dist
    elif dir == "L":
        dial += dist
    else:
        raise RuntimeError(f"Unknown direction '{dir}'")

    dial %= 100

    if dial == 0:
        count += 1

print(f"Part I: {count=}")

# "CLICK"
print(chr(int("0x43", 16)) + chr(int("0x4C", 16)) + chr(int("0x49", 16)) + chr(int("0x43", 16)) + chr(int("0x4B", 16)))

##### Part II #####

"""
- The dial starts by pointing at 50.
- The dial is rotated L68 to point at 82; during this rotation, it points at 0 once.
- The dial is rotated L30 to point at 52.
- The dial is rotated R48 to point at 0.
- The dial is rotated L5 to point at 95.
- The dial is rotated R60 to point at 55; during this rotation, it points at 0 once.
- The dial is rotated L55 to point at 0.
- The dial is rotated L1 to point at 99.
- The dial is rotated L99 to point at 0.
- The dial is rotated R14 to point at 14.
- The dial is rotated L82 to point at 32; during this rotation, it points at 0 once.

In this example, the dial points at 0 three times at the end of a rotation, plus three more times during a rotation. So, in this example, the new password would be 6.
"""

test = [("L", 68), ("L", 30), ("R", 48), ("L", 5), ("R", 60), ("L", 55), ("L", 1), ("L", 99), ("R", 14), ("L", 82)]

# actions = test

dial = 50
count = 0
for (dir, dist) in actions:

    if dist >= 100:
        turns = dist // 100 # number of full turns
        count += turns
        dist %= 100 # remaining clicks

    if dir == "R":
        dial += dist
        if dial > 100: # we traversed 0
            count += 1
    elif dir == "L":
        if dial != 0:
            dial -= dist
            if (dial < 0): # we traversed 0
                count += 1
        else:
            dial -= dist
    else:
        raise RuntimeError(f"Unknown direction '{dir}'")

    dial %= 100

    if dial == 0:
        count += 1

print(f"part II: {count=}")

print("done")
