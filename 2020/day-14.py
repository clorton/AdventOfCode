#! /usr/bin/env python3

from collections import deque, namedtuple
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-14.txt").read_text()
lines = text.split("\n")

# lines = [
#     "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
#     "mem[8] = 11",
#     "mem[7] = 101",
#     "mem[8] = 0"
# ]

# part 1
memory = {}
for line in lines:
    if line.startswith("mask"):
        mask = list(line.split(" ")[2])
        mask.reverse()
    else:
        assert line.startswith("mem")
        address, _, value = line.split(" ")
        address = int(address[:-1].split("[")[1])
        value = int(value)
        bit = 1
        for entry in mask:
            if entry != "X":
                value &= ~bit
                value |= (bit * int(entry))
            bit *= 2
        memory[address] = value

print(f"Total of values in memory is {sum(memory.values())}")


# part 2

# lines = [
#     "mask = 000000000000000000000000000000X1001X",
#     "mem[42] = 100",
#     "mask = 00000000000000000000000000000000X0XX",
#     "mem[26] = 1"
# ]

memory = {}
for line in lines:
    if line.startswith("mask"):
        mask = list(line.split(" ")[2])
        mask.reverse()
    else:
        assert line.startswith("mem")
        address, _, value = line.split(" ")
        address = int(address[:-1].split("[")[1])
        value = int(value)
        bit = 1
        ops = []
        for entry in mask:
            if entry == "0":
                pass
            elif entry == "1":
                address |= bit
            else:   # "X"
                address &= ~bit
                ops.append(bit)
            bit *= 2

        def write(value, address, ops):
            if len(ops) == 0:
                memory[address] = value
            else:
                write(value, address, ops[1:])
                write(value, address + ops[0], ops[1:])

        write(value, address, ops)

print(f"Total of values in memory is {sum(memory.values())}")


print(".oO( done )")
