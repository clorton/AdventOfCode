#! /usr/bin/env python3

from collections import deque, namedtuple
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-13.txt").read_text()
lines = text.split("\n")
departure = int(lines[0])
buses = lines[1].split(",")
buses = [int(bus) for bus in buses if bus != "x"]

# departure = 939
# buses = [7, 13, 59, 31, 19]

# part 1
departures = {}
soonest = -1
wait = max(buses)
for bus in buses:
    # trips = departure // bus
    offset = departure % bus
    when = (bus - offset if offset != 0 else 0)
    departures[bus] = when
    if when < wait:
        soonest = bus
        wait = when

print(f"Soonest is bus {soonest} at {wait} => {soonest * wait}")

# part 2
buses = lines[1].split(",")
buses = [(offset, int(bus)) for offset, bus in enumerate(buses) if bus != "x"]

time = 0
delta = 1
for offset, bus in buses:
    remainder = (bus - (offset % bus)) if offset else 0
    while time % bus != remainder:
        time += delta
    delta *= bus

print(f"Starting at time {time}, each bus will arrive at the correct offset.")

print(".oO( done )")
