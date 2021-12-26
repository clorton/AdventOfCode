#! /usr/bin/env python3

from pathlib import Path

with Path("../inputs/24.txt").open("r") as handle:
    lines = list([line.strip().split() for line in handle.readlines()])

registers = {
    "w": 0,
    "x": 0,
    "y": 0,
    "z": 0
}


def inp(r):
    global model_number
    registers[r] = model_number.pop(0)
    return


def add(a, b):
    registers[a] += registers[b] if b in registers else int(b)
    return


def mul(a, b):
    registers[a] *= registers[b] if b in registers else int(b)
    return


def div(a, b):
    dividend = registers[b] if b in registers else int(b)
    if dividend != 0:
        registers[a] //= dividend
    else:
        print("Skipping divide by zero.")
    return


def mod(a, b):
    if registers[a] < 0:
        print(f"Skipping modulo {registers[a]=}")
    else:
        modulo = registers[b] if b in registers else int(b)
        if modulo > 0:
            registers[a] %= modulo
        else:
            print(f"Skipping {modulo=}")
    return


def eql(a, b):
    comp = registers[b] if b in registers else int(b)
    registers[a] = 1 if registers[a] == comp else 0
    return


alu = {
    "inp": inp,
    "add": add,
    "mul": mul,
    "div": div,
    "mod": mod,
    "eql": eql
}

model_number = list(map(int, list("11111111111111")))

for line in lines:
    alu[line[0]](*line[1:])

print(f"{registers['z']=}")


def program(number):

    number = list(map(int, list(number)))
    w = 0
    x = 0
    # y = 0
    z = 0

    z_div =  [ 1,  1,  1,  1,  26,  26,  1,  1, 26, 26,  1, 26,  26, 26]
    x_plus = [13, 12, 12, 10, -11, -13, 15, 10, -2, -6, 14,  0, -15, -4]
    y_plus = [ 8, 13,  8, 10,  12,   1, 13,  5, 10,  3,  2,  2,  12,  7]

    for i in range(14):
        w = number[i];            print(f"{w=}, {z=}, ", end="")
        x = z % 26;               print(f"{z%26=}, {z_div[i]=}, ", end="")
        z //= z_div[i];           print(f"{z=}, {x_plus[i]=}, ", end="")
        x += x_plus[i];           print(f"{x=}, ", end="")
        x = 1 if x != w else 0;   print(f"{x=}, ", end="")
        z *= (25 * x) + 1;        print(f"{z=}, {y_plus[i]=}, ", end="")
        z += (w + y_plus[i]) * x; print(f"{z=}")

    return z


zed = program("99991111111111")
print(f"{zed=}")

pass
