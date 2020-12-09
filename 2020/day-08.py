#! /usr/bin/env python3

from collections import deque, namedtuple
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-08.txt").read_text()
rules = text.split("\n")
instructions = [tuple(rule.split(" ")) for rule in rules]
instructions = [tuple([opcode, int(operand)]) for opcode, operand in instructions]


# part 1
def acc(accumulator, operand, index):
    accumulator += operand
    index += 1
    return accumulator, index


def jmp(accumulator, operand, index):
    index += operand
    return accumulator, index


def nop(accumulator, operand, index):
    index += 1
    return accumulator, index


dispatch = {
    "acc": acc,
    "jmp": jmp,
    "nop": nop
}


def loop(program):
    accumulator = 0
    ip = 0
    while ip < len(program):
        (opcode, operand) = program[ip]
        if opcode != "hlt":
            program[ip] = tuple(["hlt", operand])
            accumulator, ip = dispatch[opcode](accumulator, operand, ip)
        else:
            return accumulator, False
    return accumulator, True


accumulator, retval = loop(list(instructions))
print(f"Accumulator = {accumulator}")

# part 2
accumulator = 0
result = False
for ip, (opcode, operand) in enumerate(instructions):
    if opcode == "jmp":
        program = list(instructions)
        program[ip] = tuple(["nop", operand])
        accumulator, result = loop(program)
        if result:
            break
    elif opcode == "nop":
        program = list(instructions)
        program[ip] = tuple(["jmp", operand])
        accumulator, result = loop(program)
        if result:
            break

print(f"Accumulator = {accumulator}")

print(".oO( done )")
