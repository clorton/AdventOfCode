#! /usr/bin/env python3

from collections import defaultdict
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"    # (Path(__file__).stem + ".txt")

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

workflows = []
parts = []
avant = True
for line in input:
    if line == "":
        avant = False
        continue
    if avant:
        workflows.append(line)
    else:
        parts.append(line)

parts = [eval("dict(" + part[1:-1] + ")") for part in parts]

flows = {}
for workflow in workflows:
    # print(workflow)
    name,steps = workflow[:-1].split("{")
    process = []
    for step in steps.split(","):
        # print(step)
        if ":" in step:
            pred, dest = step.split(":")
            prop = pred[0]
            op = pred[1]
            value = int(pred[2:])
        else:
            dest = step
            prop = None
            op = None
            value = None
        process.append((prop, op, value, dest))
    flows[name] = process

accepted = []
rejected = []
for part in parts:
    # print(part)
    flow = "in"
    while True:
        for step in flows[flow]:
            # print(step)
            prop, op, value, dest = step
            if prop is None:
                flow = dest
                break
            if op == ">":
                if part[prop] > value:
                    flow = dest
                    break
                else:
                    continue
            elif op == "<":
                if part[prop] < value:
                    flow = dest
                    break
                else:
                    continue
            # elif op == "=":
            #     if part[prop] == value:
            #         flow = dest
            #     else:
            #         continue
            else:
                raise ValueError(f"Unknown operator: {op}")
        if flow in "AR":
            break
    if dest == "A":
        accepted.append(part)
    elif dest == "R":
        rejected.append(part)
    else:
        raise ValueError(f"Unknown destination: {dest}")

print(f"{sum([sum(part.values()) for part in accepted])=}")

pass
