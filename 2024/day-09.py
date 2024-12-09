from pathlib import Path

import numpy as np

with (Path(__file__).parent / "day-09.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#      "2333133121414131402", # 2-block file, 3-blocks free, 3-block file, 3-blocks free, 1-block file...
# ]

lengths = list(map(int, list(lines[0])))

files = [length for i, length in enumerate(lengths) if i % 2 == 0]
spaces = [length for i, length in enumerate(lengths) if i % 2 == 1]

while len(spaces) < len(files):
    spaces.append(0)

disk = np.full(sum(lengths), -1, np.int32)
i = 0
for id, (file, space) in enumerate(zip(files, spaces)):
    disk[i:i+file] = id
    i += file
    i += space

writer = 0
reader = len(disk) - 1
while True:
    while writer < len(disk) and disk[writer] != -1:
        writer += 1
    while reader >= 0 and disk[reader] == -1:
        reader -= 1
    if writer < reader:
        disk[writer] = disk[reader]
        disk[reader] = -1
    else:
        break

check = 0
for i in range(len(disk)):
    if disk[i] > 0:
        check += i * int(disk[i])

print(f"checksum = {check}")

disk[:] = -1
i = 0
from collections import defaultdict

used = []
free = []
for id, (file, space) in enumerate(zip(files, spaces)):
    disk[i:i+file] = id
    used.append((id, i, file))
    i += file
    if space > 0:
        free.append((i, space))
        i += space

for id, index, length in reversed(used):
    for i, (location, space) in enumerate(free):
        if location > index:
            # We don't move files further into the disk
            break
        if space >= length:
            disk[index:index+length] = -1
            disk[location:location+length] = id
            if space > length:
                free[i] = (location + length, space -length)
            else:
                free.pop(i)
            break

check = 0
for i in range(len(disk)):
    if disk[i] > 0:
        check += i * int(disk[i])

print(f"checksum = {check}")

print("Done.")
