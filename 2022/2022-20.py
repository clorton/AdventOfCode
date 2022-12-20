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

state = np.array(inputs,dtype=np.int32)
positions = {value:index for index,value in enumerate(state)}

print(state[0:8])
# print(positions)

tstart = datetime.now()
for index, value in enumerate(inputs):

    current = positions[value]
    new = current + value
    if new >= len(state):
        new = new % len(state) + 1
    elif new < 0:
        new = new % len(state) - 1
    delta = abs(new - current)

    if index < 8:
        print(f"{state} {value=:2} {current=:1} new0={(current+value):2} {new=:1} ", end="")

    if new > current:

        first = current
        last = first + delta - 1

        state[first:last+1] = state[first+1:last+2]
        state[new] = value

        for i in range(current, new+1):
            positions[state[i]] = i

    elif new < current:

        first = new + 1
        last = first + delta - 1

        state[first:last+1] = state[first-1:last]
        state[new] = value

        for i in range(new, current+1):
            positions[state[i]] = i

    else:
        pass    # nothing changes (value is 0)

    if index < 8:
        print(f"{state}")
tend = datetime.now()

izero = positions[0]
einsk = state[(izero+1000)%len(state)]
zweik = state[(izero+2000)%len(state)]
dreik = state[(izero+3000)%len(state)]

# Answer != -13132 (-2622 + -8866 + -1624)
print(f"{tend-tstart}: {einsk=}, {zweik=}, {dreik=} ... {einsk+zweik+dreik}")
