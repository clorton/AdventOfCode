# from collections import namedtuple
from datetime import datetime
from pathlib import Path

import numpy as np

WORKDIR = Path(__file__).parent.absolute()
INPUTFILE = WORKDIR / "2022-20.txt"

with INPUTFILE.open("r") as file:
    inputs = [int(line.strip()) for line in file.readlines()]

test = [1,2,-3,3,-2,0,4]
# inputs = test

print(inputs[0:8])

VALUE = 0
NEXT = 1
PREV = 2
length = len(inputs)
linked = np.zeros((length, 3), dtype=np.int32)

for index, value in enumerate(inputs):
    linked[index, VALUE] = value
    linked[index, NEXT] = (index+1)%length
    linked[index, PREV] = (index-1)%length

def unlink(index, linkedlist):

    linkedlist[linkedlist[index, NEXT], PREV] = linkedlist[index, PREV]
    linkedlist[linkedlist[index, PREV], NEXT] = linkedlist[index, NEXT]

    return

def insert_after(target, index, linkedlist):

    save_next = linkedlist[target, NEXT]
    linkedlist[index, NEXT] = save_next
    linkedlist[index, PREV] = target
    linkedlist[target, NEXT] = index
    linkedlist[save_next, PREV] = index

    return

def insert_before(target, index, linkedlist):

    save_prev = linkedlist[target, PREV]
    linkedlist[index, NEXT] = target
    linkedlist[index, PREV] = save_prev
    linkedlist[target, PREV] = index
    linkedlist[save_prev, NEXT] = index

    return

def mix(inputs, linkedlist, iteration="?"):

    tstart = datetime.now()
    for index, value in enumerate(inputs):

        if value == 0:
            continue

        skip = value

        unlink(index, linkedlist)
        current = index

        if skip > 0:

            current = linkedlist[current, NEXT]
            skip -= 1

            skip = (skip % (length-1))

            for _ in range(skip):
                current = linkedlist[current, NEXT]

            insert_after(current, index, linkedlist)

        else:   # skip < 0:

            current = linkedlist[current, PREV]
            skip += 1

            skip = (abs(skip) % (length-1))

            for _ in range(abs(skip)):
                current = linkedlist[current, PREV]

            insert_before(current, index, linkedlist)

    tend = datetime.now()

    if length <= 16:
        print(f"{iteration}: ", end="")
        current = 0
        for _ in range(length):
            print(f"{linkedlist[current, VALUE]} ", end="")
            current = linkedlist[current, NEXT]
        print()

    return tend-tstart

elapsed = mix(inputs, linked)

def get_coordinates(linkedlist, elapsed):

    izero = np.nonzero(linkedlist[:,VALUE] == 0)[0][0]

    current = izero
    for _ in range(1000):
        current = linkedlist[current, NEXT]
    einsk = linkedlist[current, VALUE]
    for _ in range(1000):
        current = linkedlist[current, NEXT]
    zweik = linkedlist[current, VALUE]
    for _ in range(1000):
        current = linkedlist[current, NEXT]
    dreik = linkedlist[current, VALUE]

    print(f"{elapsed}: {einsk=}, {zweik=}, {dreik=} ... {einsk+zweik+dreik}")

    return

get_coordinates(linked, elapsed)

KEY = 811589153
decrypted = np.zeros((length, 3), dtype=np.int64)

for index, value in enumerate(inputs):
    decrypted[index, VALUE] = value*KEY
    decrypted[index, NEXT] = (index+1)%length
    decrypted[index, PREV] = (index-1)%length

if length <= 16:
    print(" ".join(map(str, decrypted[:,VALUE])))

elapsed = datetime.now()
elapsed -= elapsed
for _ in range(10):
    elapsed += mix(inputs, decrypted, _)

# 5449009573242 is too high...
get_coordinates(decrypted, elapsed)
