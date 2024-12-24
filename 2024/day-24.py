from pathlib import Path

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "day-24.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

alines = [
    "x00: 1",
    "x01: 1",
    "x02: 1",
    "y00: 0",
    "y01: 1",
    "y02: 0",
    "",
    "x00 AND y00 -> z00",
    "x01 XOR y01 -> z01",
    "x02 OR y02 -> z02",
]

blines = [
    "x00: 1",
    "x01: 0",
    "x02: 1",
    "x03: 1",
    "x04: 0",
    "y00: 1",
    "y01: 1",
    "y02: 1",
    "y03: 1",
    "y04: 1",
    "",
    "ntg XOR fgs -> mjb",
    "y02 OR x01 -> tnw",
    "kwq OR kpj -> z05",
    "x00 OR x03 -> fst",
    "tgd XOR rvg -> z01",
    "vdt OR tnw -> bfw",
    "bfw AND frj -> z10",
    "ffh OR nrd -> bqk",
    "y00 AND y03 -> djm",
    "y03 OR y00 -> psh",
    "bqk OR frj -> z08",
    "tnw OR fst -> frj",
    "gnj AND tgd -> z11",
    "bfw XOR mjb -> z00",
    "x03 OR x00 -> vdt",
    "gnj AND wpb -> z02",
    "x04 AND y00 -> kjc",
    "djm OR pbm -> qhw",
    "nrd AND vdt -> hwm",
    "kjc AND fst -> rvg",
    "y04 OR y02 -> fgs",
    "y01 AND x02 -> pbm",
    "ntg OR kjc -> kwq",
    "psh XOR fgs -> tgd",
    "qhw XOR tgd -> z09",
    "pbm OR djm -> kpj",
    "x03 XOR y03 -> ffh",
    "x00 XOR y04 -> ntg",
    "bfw OR bqk -> z06",
    "nrd XOR fgs -> wpb",
    "frj XOR qhw -> z04",
    "bqk OR frj -> z07",
    "y03 OR x01 -> nrd",
    "hwm AND bqk -> z03",
    "tgd XOR rvg -> z12",
    "tnw OR pbm -> gnj",
]

from collections import namedtuple
Gate = namedtuple("Gate", ["a", "op", "b", "c"])

wires = {}
gates = set()
start = True
for line in lines:
    if not line:
        start = False
        continue

    if start:
        wire, value = line.split(": ")
        wires[wire] = int(value)
    else:
        a, op, b, _, c = line.split()
        gates.add(Gate(a, op, b, c))

print(f"{len(wires)=}, {len(gates)=}")

def run(wires, gates):
    state = dict(wires)
    check = list(gates)
    while check:
        gate = check.pop(0)
        a, op, b, c = gate
        if a in state and b in state:
            if op == "AND":
                state[c] = state[a] & state[b]
            elif op == "OR":
                state[c] = state[a] | state[b]
            elif op == "XOR":
                state[c] = state[a] ^ state[b]
            else:
                raise RuntimeError(f"Unknown operator: {op}")
        else:
            check.append(gate)

    return state

state = run(wires, gates)

def decode(state):
    zs = [k for k in state if k.startswith("z")]
    zs = sorted(zs, reverse=True)
    outputs = "".join([str(state[k]) for k in zs])
    return outputs

outputs = decode(state)
print(f"{len(outputs)=}")
print(f"{outputs=} = {int(outputs, 2)}")

## Part 2

check00 = {k:0 for k in wires}
state00 = run(check00, gates)
print(f"{decode(state00)=}")

check01 = {k: 0 if k.startswith("x") else 1 for k in wires}
state01 = run(check01, gates)
print(f"{decode(state01)=}")

check10 = {k: 1 if k.startswith("x") else 0 for k in wires}
state10 = run(check10, gates)
print(f"{decode(state10)=}")

check11 = {k: 1 for k in wires}
state11 = run(check11, gates)
print(f"{decode(state11)=}")

checker = dict(wires)
for k in checker:
    if k.startswith("x"):
        checker[k] = int(k[1:]) % 2
    else:
        checker[k] = 1 - (int(k[1:]) % 2)
stateck = run(checker, gates)
print(f"{decode(stateck)=}")

def findall(gates, wire):
    result = set()
    check = [wire]
    while check:
        wire = check.pop(0)
        for gate in gates:
            if gate.c == wire:
                result.add(gate)
                check.append(gate.a)
                check.append(gate.b)

    return result

f = findall(gates, "z00")

def test(x, y, gates):
    wires = {}
    for p in range(len(x)):
        wires[f"x{p:02}"] = int(x[p])
    for p in range(len(y)):
        wires[f"y{p:02}"] = int(y[p])
    s = run(wires, gates)
    o = decode(s)
    print(f"{x=}")
    print(f"{y=}")
    print(f"{o=}")
    print()

test("0"*45+"0", "0"*45+"0", gates)
test("0"*45+"0", "0"*45+"1", gates)
test("0"*45+"1", "0"*45+"0", gates)
test("0"*45+"1", "0"*45+"1", gates)

suspect = set()
for position in range(0, 45):
    for test in [(0, 1, 1), (1, 0, 1), (1, 1, 0)]:
        inputs = {k:0 for k in wires}
        x, y, z = test
        inputs[f"x{position:02}"] = x
        inputs[f"y{position:02}"] = y
        state = run(inputs, gates)
        xs = ["0"]*45; xs[44-position] = str(x); xs = "".join(xs)
        ys = ["0"]*45; ys[44-position] = str(y); ys = "".join(ys)
        o = decode(state)
        if state[f"z{position:02}"] != z:
            print(f"Failed at {position=}")
            print(f"{xs=}")
            print(f"{ys=}")
            print(f"{o=}")
            suspect.add(f"z{position:02}")
        if x and y and state[f"z{position+1:02}"] != 1:
            print(f"Failed at {position+1=}")
            print(f"{xs=}")
            print(f"{ys=}")
            print(f"{o=}")
            suspect.add(f"z{position+1:02}")
print(f"{suspect=}")

# for wire in sorted(suspect):
#     f = findall(gates, wire)
#     print(f"{wire=} {len(f)=}")
#     for g in f:
#         print(f"\t{g}")

print("Done.")
