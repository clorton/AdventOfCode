from pathlib import Path
import re

import numpy as np

with (Path(__file__).parent / "day-13.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

# It costs 3 tokens to push the A button and 1 token to push the B button.

# lines = [
#     "Button A: X+94, Y+34",
#     "Button B: X+22, Y+67",
#     "Prize: X=8400, Y=5400",
#     "",
#     "Button A: X+26, Y+66",
#     "Button B: X+67, Y+21",
#     "Prize: X=12748, Y=12176",
#     "",
#     "Button A: X+17, Y+86",
#     "Button B: X+84, Y+37",
#     "Prize: X=7870, Y=6450",
#     "",
#     "Button A: X+69, Y+23",
#     "Button B: X+27, Y+71",
#     "Prize: X=18641, Y=10279",
# ]

from collections import namedtuple
Button = namedtuple("Button", ["dx", "dy"])
Prize = namedtuple("Prize", ["x", "y"])
Machine = namedtuple("Machine", ["A", "B", "prize"])

machines = []
for i, line in enumerate(lines):
    if i % 4 == 0:  # first line
        m = re.match(r"Button A: X\+([0-9]+), Y\+([0-9]+)", line)
        dx, dy = m[1], m[2]
        A = Button(int(dx), int(dy))
    elif i % 4 == 1: # second line
        m = re.match(r"Button B: X\+([0-9]+), Y\+([0-9]+)", line)
        dx, dy = m[1], m[2]
        B = Button(int(dx), int(dy))
    elif i % 4 == 2: # third line
        m = re.match(r"Prize: X=([0-9]+), Y=([0-9]+)", line)
        x, y =  m[1], m[2]
        P = Prize(int(x), int(y))
        machines.append(Machine(A, B, P))


def solve(machine):
    system = np.array([
        [machine.prize.x, machine.A.dx, machine.B.dx],
        [machine.prize.y, machine.A.dy, machine.B.dy]])
    system[0,:] *= machine.B.dy
    system[1,:] *= machine.B.dx
    equation = system[0,:] - system[1,:]
    a = equation[0] / equation[1]
    if (a >= 0) and (a <= 100) and (a == int(a)):
        a = int(a)
        b = (machine.prize.x - a * machine.A.dx) / machine.B.dx
        if (b >= 0) and (b <= 100) and (b == int(b)):
            b = int(b)
            return a, b

    return 0, 0

total = 0
for machine in machines:
    A, B = solve(machine)
    if (A != 0) or (B != 0):
        print(f"Solved machine {machine}: {A=}, {B=}, cost = {3*A+B}")
        total += 3*A + B

print(f"Total = {total} tokens.")

def solve2(machine):
    system = np.array([
        [machine.prize.x+10000000000000, machine.A.dx, machine.B.dx],
        [machine.prize.y+10000000000000, machine.A.dy, machine.B.dy]],dtype=np.float64)
    system[0,:] *= machine.B.dy
    system[1,:] *= machine.B.dx
    equation = system[0,:] - system[1,:]
    a = equation[0] / equation[1]
    if (a >= 0) and (a == int(a)):
        a = int(a)
        b = ((machine.prize.x+10000000000000) - a * machine.A.dx) / machine.B.dx
        if (b >= 0) and (b == int(b)):
            b = int(b)
            return a, b

    return 0, 0

total = 0
for machine in machines:
    A, B = solve2(machine)
    if (A != 0) or (B != 0):
        print(f"Solved machine {machine}: {A=}, {B=}, cost = {3*A+B}")
        total += 3*A + B

print(f"Total = {total} tokens.")

print("Done.")
