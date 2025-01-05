from pathlib import Path

import numpy as np
from tqdm import tqdm

with (Path(__file__).parent / "2015-12.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

import json
data = json.loads(lines[0])

def process1(data):
    if isinstance(data, int):
        return data
    if isinstance(data, list):
        return sum([process1(d) for d in data])
    if isinstance(data, dict):
        return sum([process1(d) for d in data.values()])
    return 0

print(process1(data))

def process2(data):
    if isinstance(data, int):
        return data
    if isinstance(data, list):
        return sum([process2(d) for d in data])
    if isinstance(data, dict):
        return 0 if any((v == "red" for v in data.values())) else sum([process2(d) for d in data.values()])
    return 0

print(process2(data))

print("Done.")
