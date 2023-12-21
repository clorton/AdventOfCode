#! /usr/bin/env python3

from collections import defaultdict, deque
from math import prod, lcm  
from pathlib import Path

import numpy as np

from tqdm import tqdm

WORKING_DIRECTORY = Path(__file__).parent.absolute()
INPUT_FILE = Path(__file__).parent / "input.txt"

with INPUT_FILE.open("r") as file:
    input = [line.strip() for line in file.readlines()]

# Flip-flop modules (prefix %) are either on or off; they are initially off.
# If a flip-flop module receives a high pulse, it is ignored and nothing happens.
# However, if a flip-flop module receives a low pulse, it flips between on and off.
# If it was off, it turns on and sends a high pulse.
# If it was on, it turns off and sends a low pulse.
    
LOW = False
HIGH = True
counts = {LOW: 0, HIGH: 0}
pulses = deque()
# history = []
def send_pulse(source, value, destination):
    counts[value] += 1
    pulses.append((source, value, destination))
    # history.append((source, value, destination))
    return
    
class FlipFlop():
    def __init__(self, label, sinks):
        self.label = label
        self.sinks = sinks
        self.state = LOW

    def add_input(self, input):
        return

    def pulse(self, source, value):
        if value == LOW:
            self.state = not self.state
            for destination in self.sinks:
                send_pulse(self.label, self.state, destination)
        return
    
# Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules;
# they initially default to remembering a low pulse for each input.
# When a pulse is received, the conjunction module first updates its memory for that input.
# Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
    
class Conjunction():
    def __init__(self, label, sinks):
        self.label = label
        self.sinks = sinks
        self.memory = {}

    def add_input(self, input):
        self.memory[input] = LOW
        return

    def pulse(self, source, value):
        self.memory[source] = value
        if all(self.memory.values()):
            for destination in self.sinks:
                send_pulse(self.label, LOW, destination)
        else:
            for destination in self.sinks:
                send_pulse(self.label, HIGH, destination)
        return  

# There is a single broadcast module (named broadcaster).
# When it receives a pulse, it sends the same pulse to all of its destination modules.

class Broadcaster():
    def __init__(self, label, sinks):
        self.label = label
        self.sinks = sinks
        self.nxt = None

    def add_input(self, input):
        return

    def pulse(self, source, value):
        for destination in self.sinks:
            send_pulse(self.label, value, destination)
        return
    
class Button():
    def __init__(self, label, sinks=["broadcaster"]):
        self.label = label
        self.sinks = sinks
        self.state = LOW

    def add_input(self, input):
        return

    def pulse(self, source, value):
        for destination in self.sinks:
            send_pulse(self.label, self.state, destination)
        return
    
class Output():
    def __init__(self, label="output", sinks=[]):
        self.label = label
        self.sinks = sinks
        self.low = 0

    def add_input(self, input):
        return

    def pulse(self, source, value):
        if value == LOW:
            self.low += 1
        # print(f"{self.label}: {value}")
        return

def initialize(input):

    modules = {}
    for line in input:
        if line.startswith("broadcaster"):
            label, sinks = line.split(" -> ")
            modules[label] = Broadcaster(label, sinks.split(", "))
            continue
        if line.startswith("%"):
            label, sinks = line[1:].split(" -> ")
            modules[label] = FlipFlop(label, sinks.split(", "))
            continue
        if line.startswith("&"):
            label, sinks = line[1:].split(" -> ")
            modules[label] = Conjunction(label, sinks.split(", "))
            continue

    modules["output"] = Output()
    modules["rx"] = Output("rx")

    for label, module in modules.items():
        for sink in module.sinks:
            modules[sink].add_input(label)

    return modules

modules = initialize(input)
for push in range(1000):
    button = Button("button")
    button.pulse("button", LOW)
    while pulses:
        source, value, destination = pulses.popleft()
        modules[destination].pulse(source, value)

print(f"{counts=}, {prod(counts.values())=}")
# for index, (source, value, destination) in enumerate(history):
#     print(f"{index}: {source} -> {destination}: {value}")

modules = initialize(input)
push = 1
cycles = { "pr": 0, "rd": 0, "bt": 0, "fv": 0 }
while True:
    button = Button("button")
    button.pulse("button", LOW)
    while pulses:
        source, value, destination = pulses.popleft()
        if source in ["pr", "rd", "bt", "fv"] and (value == HIGH) and (cycles[source] == 0):
            cycles[source] = push
        modules[destination].pulse(source, value)
    if modules["rx"].low > 0:
        print(f"{modules['rx'].low=}")
        print(f"{push=}")
        break
    if all(cycles.values()):
        break
    push += 1

print(f"{cycles=}")
print(f"{lcm(*cycles.values())=}")

pass
