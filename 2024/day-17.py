from pathlib import Path
# import re

import numpy as np

with (Path(__file__).parent / "day-17.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# lines = [
#     "Register A: 729",
#     "Register B: 0",
#     "Register C: 0",
#     "",
#     "Program: 0,1,5,4,3,0",
# ]
# 4,6,3,5,6,3,5,2,1,0

# lines = [
    # "Register A: 2024",
    # "Register B: 0",
    # "Register C: 0",
    # "",
    # "Program: 0,3,5,4,3,0",
# ]
# outputs self when a = 117440

for line in lines:
    if line.startswith("Register A: "):
        a = int(line.split(": ")[1])
    elif line.startswith("Register B: "):
        b = int(line.split(": ")[1])
    elif line.startswith("Register C: "):
        c = int(line.split(": ")[1])
    elif line.startswith("Program: "):
        program = [int(i) for i in line.split(": ")[1].split(",")]

ADV = 0
BXL = 1
BST = 2
JNZ = 3
BXC = 4
OUT = 5
BDV = 6
CDV = 7

opnames = {
    ADV: "ADV",
    BXL: "BXL",
    BST: "BST",
    JNZ: "JNZ",
    BXC: "BXC",
    OUT: "OUT",
    BDV: "BDV",
    CDV: "CDV",
}

DEBUG = False

"""
Combo operands 0 through 3 represent literal values 0 through 3.
Combo operand 4 represents the value of register A.
Combo operand 5 represents the value of register B.
Combo operand 6 represents the value of register C.
Combo operand 7 is reserved and will not appear in valid programs.
"""

def combo(m, o):
    if 0 <= o <= 3:
        return o
    elif o == 4:
        return m.a
    elif o == 5:
        return m.b
    elif o == 6:
        return m.c
    else:
        raise ValueError(f"Invalid operator {o}.")

"""
The adv instruction (opcode 0) performs division.
The numerator is the value in the A register.
The denominator is found by raising 2 to the power of the instruction's combo operand.
(So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
The result of the division operation is truncated to an integer and then written to the A register.
"""

def adv(m, o):
    o = combo(m, o)
    if DEBUG: print(f"m.a = {m.a} // 2**{o} ({m.a // 2**o})", end=" ")
    m.a = m.a // 2**o
    m.pc += 2

"""
The bxl instruction (opcode 1) calculates the bitwise XOR of register B and
the instruction's literal operand, then stores the result in register B.
"""

def bxl(m, o):
    if DEBUG: print(f"m.b = {m.b} ^ {o} ({m.b ^ o})", end=" ")
    m.b = m.b ^ o
    m.pc += 2

"""
The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
(thereby keeping only its lowest 3 bits), then writes that value to the B register.
"""

def bst(m, o):
    o = combo(m, o)
    if DEBUG: print(f"m.b = {o} % 8 ({o % 8})", end=" ")
    m.b = o % 8
    m.pc += 2

"""
The jnz instruction (opcode 3) does nothing if the A register is 0.
However, if the A register is not zero, it jumps by setting the instruction pointer
to the value of its literal operand; if this instruction jumps, the instruction pointer
is not increased by 2 after this instruction.
"""

def jnz(m, o):
    if m.a != 0:
        m.pc = o
        if DEBUG: print(f"Jumping to {o}.", end=" ")
    else:
        m.pc += 2

"""
The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
then stores the result in register B.
(For legacy reasons, this instruction reads an operand but ignores it.)
"""

def bxc(m, o):
    if DEBUG: print(f"m.b = {m.b} ^ {m.c} ({m.b ^ m.c})", end=" ")
    m.b = m.b ^ m.c
    m.pc += 2

"""
The out instruction (opcode 5) calculates the value of its combo operand modulo 8,
then outputs that value. (If a program outputs multiple values, they are separated by commas.)
"""

def out(m, o):
    o = combo(m, o)
    m.out.append(o % 8)
    if DEBUG: print(",".join([str(o) for o in m.out]), end=" ")
    m.pc += 2

"""
The bdv instruction (opcode 6) works exactly like the adv instruction except that
the result is stored in the B register.
(The numerator is still read from the A register.)
"""

def bdv(m, o):
    o = combo(m, o)
    if DEBUG: print(f"m.b = {m.a} // 2**{o} ({m.a // 2**o})", end=" ")
    m.b = m.a // 2**o
    m.pc += 2

"""
The cdv instruction (opcode 7) works exactly like the adv instruction except that
the result is stored in the C register.
(The numerator is still read from the A register.)
"""

def cdv(m, o):
    o = combo(m, o)
    if DEBUG: print(f"m.c = {m.a} // 2**{o} ({m.a // 2**o})", end=" ")
    m.c = m.a // 2**o
    m.pc += 2

opcodes = {
    ADV: adv,
    BXL: bxl,
    BST: bst,
    JNZ: jnz,
    BXC: bxc,
    OUT: out,
    BDV: bdv,
    CDV: cdv,
}

class Machine:
    def __init__(self, a, b, c, program):
        self.a = a
        self.b = b
        self.c = c
        self.pc = 0
        self.program = program
        self.out = []

    def run(self, pc = 0):
        self.pc = pc
        while self.pc < len(self.program):
            opcode, operand = self.program[self.pc], self.program[self.pc + 1]
            if DEBUG:
                print(f"PC: {self.pc}, Opcode: {opnames[opcode]}, Operand: {operand}", end=" ")
            opcodes[opcode](self, operand)
            if DEBUG:
                print(f"{self.a=}, {self.b=}, {self.c=}")
            # print(",".join([str(o) for o in self.out]))

        return
    
    def reset(self, a=0, b=0, c=0, out=None):
        self.a = a
        self.b = b
        self.c = c
        self.pc = 0
        self.out = out if out is not None else []

        return

    @property
    def output(self):
        return ",".join([str(o) for o in self.out])

m = Machine(a, b, c, program)
m.run()
print(m.output)

print("Done.")
