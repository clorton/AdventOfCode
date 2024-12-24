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

ops = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "XOR": lambda x, y: x ^ y,
}

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
        gates.add(Gate(a, ops[op], b, c))

print(f"{len(wires)=}, {len(gates)=}")

def run(wires, gates):
    state = dict(wires)
    test = list(gates)
    while test:
        retest = []
        for gate in test:
            a, op, b, c = gate
            if a in state and b in state:
                state[c] = op(state[a], state[b])
            else:
                retest.append(gate)
        test = retest

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

from collections import deque

def run2(wires, gates):
    state = dict(wires)
    check = deque(gates)
    while check:
        gate = check.popleft()
        a, op, b, c = gate
        if a in state and b in state:
            state[c] = op(state[a], state[b])
        else:
            check.append(gate)
            if not any(a in state and b in state for a, op, b, c in check):
                raise RuntimeError("Stuck")

    return state

xkeys = [f"x{i:02d}" for i in range(45)]
ykeys = [f"y{i:02d}" for i in range(45)]
zkeys = [f"z{i:02d}" for i in range(46)]

from functools import reduce

def trial(x, y, gates):
    wires = {k:x>>i & 1 for i, k in enumerate(xkeys)}
    wires.update({k:y>>i & 1 for i, k in enumerate(ykeys)})
    state = run2(wires, gates)
    result = reduce(lambda a, b: a | b[1] << b[0], enumerate([state[k] for k in zkeys]), 0)
    return result

x = 0b101101010111101101000111000000010110000000011
y = 0b100011100111110100010111100110001110000011011
# print(f"{trial(x, y, gates)=}")
assert trial(x, y, gates) == 43942008931358

def test(bit, gates):

    value = 1<<bit
    output = trial(value, 0, gates)
    if output != value:
        # print(f"Failed for 1+0 {bit=:2}, {output=:46} != {value=:46}")
        return False
    output = trial(0, value, gates)
    if output != value:
        # print(f"Failed for 0+1 {bit=:2}, {output=:46} != {value=:46}")
        return False
    output = trial(value, value, gates)
    if output != (value + value):
        # print(f"Failed for 1+1 {bit=:2}, {output=:46} != {value=:46}")
        return False

    return True

from itertools import combinations

# for bit in range(45):
#     if not test(bit, gates):
#         print(f"Failed {bit=:2}")
#         fixed = set(gates)
#         for gateA, gateB in tqdm(list(combinations(gates, 2))):
#             fixed.remove(gateA)
#             fixed.remove(gateB)
#             fixed.add(switchA := Gate(gateA.a, gateA.op, gateA.b, gateB.c))
#             fixed.add(switchB := Gate(gateB.a, gateB.op, gateB.b, gateA.c))
#             try:
#                 if test(bit, fixed):
#                     print(f"Fixed {bit=:2} with {gateA=} and {gateB=}")
#                     break
#             except RuntimeError:
#                 pass
#             fixed.remove(switchB)
#             fixed.remove(switchA)
#             fixed.add(gateB)
#             fixed.add(gateA)

def swap(gates, a, b):
    gates.remove(a)
    gates.remove(b)
    gates.add(switchA := Gate(a.a, a.op, a.b, b.c))
    gates.add(switchB := Gate(b.a, b.op, b.b, a.c))
    return switchA, switchB

fixed = set(gates)
# swap(fixed, Gate(a='fgb', op=ops['XOR'], b='bmd', c='z11'), Gate(a='x10', op=ops['AND'], b='y10', c='z10'))
# # swap(fixed, Gate(a='jfb', op=ops['XOR'], b='vgw', c='z18'), Gate(a='qjg', op=ops['AND'], b='jjf', c='z17'))
# swap(fixed, Gate(a='jjf', op=ops['XOR'], b='qjg', c='fhg'), Gate(a='qjg', op=ops['AND'], b='jjf', c='z17'))
# swap(fixed, Gate(a='dvb', op=ops['XOR'], b='jsn', c='z35'), Gate(a='ftc', op=ops['OR'], b='fsq', c='bwc'))
# # swap(fixed, Gate(a='gqm', op=ops['OR'], b='kfp', c='mnd'), Gate(a='y39', op=ops['AND'], b='x39', c='rvd'))
# swap(fixed, Gate(a='kmh', op=ops['XOR'], b='mnd', c='tnc'), Gate(a='rvd', op=ops['OR'], b='wrj', c='z39'))

def test2(bit, gates):

    for x in [0, 1, 2, 3]:
        for y in [0, 1, 2, 3]:
            value1 = x<<bit
            value2 = y<<bit
            output = trial(value1, value2, gates)
            if output != (value1 + value2):
                return False

    return True

# benchmark = set()
# for bit in tqdm(range(44)):
#     try:
#         if not test2(bit, gates):
#             benchmark.add(bit)
#     except RuntimeError:
#         benchmark.add(bit)
# print(f"{benchmark=}")

# for gateA, gateB in tqdm(list(combinations(gates, 2))):
#     switchA, switchB = swap(fixed, gateA, gateB)
#     failed = set()
#     for bit in benchmark:
#         try:
#             if not test(bit, fixed):
#                 failed.add(bit)
#         except RuntimeError:
#             failed.add(bit)
#     if failed != benchmark:
#         print(f"Switch {gateA=} and {gateB=} fixed {benchmark - failed}")
#     swap(fixed, switchA, switchB)

"""
Switch gateA=Gate(a='x10', op=AND, b='y10', c='z10') and gateB=Gate(a='fgb', op=XOR, b='bmd', c='z11') fixed {9, 10}
Switch gateA=Gate(a='x10', op=AND, b='y10', c='z10') and gateB=Gate(a='sst', op=OR , b='vcf', c='fgb') fixed {9, 10}
Switch gateA=Gate(a='x10', op=AND, b='y10', c='z10') and gateB=Gate(a='kck', op=XOR, b='skm', c='vcf') fixed {9, 10}

Switch gateA=Gate(a='qjg', op=AND, b='jjf', c='z17') and gateB=Gate(a='jjf', op=XOR, b='qjg', c='fhg') fixed {16, 17}

Switch gateA=Gate(a='y35', op=AND, b='x35', c='dvb') and gateB=Gate(a='y35', op=XOR, b='x35', c='fsq') fixed {35}
Switch gateA=Gate(a='dvb', op=XOR, b='jsn', c='z35') and gateB=Gate(a='y35', op=XOR, b='x35', c='fsq') fixed {35}
Switch gateA=Gate(a='dvb', op=XOR, b='jsn', c='z35') and gateB=Gate(a='ftc', op=OR , b='fsq', c='bwc') fixed {35}
Switch gateA=Gate(a='dvb', op=XOR, b='jsn', c='z35') and gateB=Gate(a='ncq', op=XOR, b='bwc', c='z36') fixed {35}

Switch gateA=Gate(a='kmh', op=XOR, b='mnd', c='tnc') and gateB=Gate(a='y39', op=AND, b='x39', c='rvd') fixed {38, 39}
Switch gateA=Gate(a='kmh', op=XOR, b='mnd', c='tnc') and gateB=Gate(a='rvd', op=OR , b='wrj', c='z39') fixed {38, 39}
Switch gateA=Gate(a='y39', op=AND, b='x39', c='rvd') and gateB=Gate(a='rtf', op=XOR, b='tnc', c='z40') fixed {38, 39}
Switch gateA=Gate(a='rtf', op=XOR, b='tnc', c='z40') and gateB=Gate(a='rvd', op=OR , b='wrj', c='z39') fixed {38, 39}
"""

fixed = set(gates)
# for swap1 in [("z10", "z11"), ("z10", "fgb"), ("z10", "vcf")]:
a1 = next(filter(lambda g: g.c == "z10", fixed))
b1 = next(filter(lambda g: g.c == "vcf", fixed))
c1, d1 = swap(fixed, a1, b1)
# for swap2 in [("z17", "fhg")]:
a2 = next(filter(lambda g: g.c == "z17", fixed))
b2 = next(filter(lambda g: g.c == "fhg", fixed))
c2, d2 = swap(fixed, a2, b2)
# for swap3 in [("dvb", "fsq"), ("z35", "fsq"), ("z35", "bwc"), ("z35", "z36")]:
a3 = next(filter(lambda g: g.c == "dvb", fixed))
b3 = next(filter(lambda g: g.c == "fsq", fixed))
c3, d3 = swap(fixed, a3, b3)
# for swap4 in [("tnc", "rvd"), ("tnc", "z39"), ("rvd", "z40"), ("z40", "z39")]:
a4 = next(filter(lambda g: g.c == "tnc", fixed))
b4 = next(filter(lambda g: g.c == "z39", fixed))
c4, d4 = swap(fixed, a4, b4)
for bit in tqdm(range(44)):
    try:
        if not test2(bit, fixed):
            print(f"Failed {bit=:2}")
    except RuntimeError:
        print(f"Failed {bit=:2}")
print(",".join(sorted([a1.c, b1.c, a2.c, b2.c, a3.c, b3.c, a4.c, b4.c])))

from itertools import product

fixed = set(gates)
for swap1, swap2, swap3, swap4 in tqdm(list(product([("z10", "z11"), ("z10", "fgb"), ("z10", "vcf")], [("z17", "fhg")], [("dvb", "fsq"), ("z35", "fsq"), ("z35", "bwc"), ("z35", "z36")], [("tnc", "rvd"), ("tnc", "z39"), ("rvd", "z40"), ("z40", "z39")]))):
    a1 = next(filter(lambda g: g.c == swap1[0], fixed))
    b1 = next(filter(lambda g: g.c == swap1[1], fixed))
    c1, d1 = swap(fixed, a1, b1)
    a2 = next(filter(lambda g: g.c == swap2[0], fixed))
    b2 = next(filter(lambda g: g.c == swap2[1], fixed))
    c2, d2 = swap(fixed, a2, b2)
    a3 = next(filter(lambda g: g.c == swap3[0], fixed))
    b3 = next(filter(lambda g: g.c == swap3[1], fixed))
    c3, d3 = swap(fixed, a3, b3)
    a4 = next(filter(lambda g: g.c == swap4[0], fixed))
    b4 = next(filter(lambda g: g.c == swap4[1], fixed))
    c4, d4 = swap(fixed, a4, b4)
    good = True
    for bit in range(44):
        try:
            if not test2(bit, fixed):
                good = False
                break
        except RuntimeError:
            good = False
            break
    if good:
        print(f"{swap1=}")
        print(f"{swap2=}")
        print(f"{swap3=}")
        print(f"{swap4=}")
        print(",".join(sorted([swap1[0], swap1[1], swap2[0], swap2[1], swap3[0], swap3[1], swap4[0], swap4[1]])))
        break
    swap(fixed, c4, d4)
    swap(fixed, c3, d3)
    swap(fixed, c2, d2)
    swap(fixed, c1, d1)

print("Done.")
