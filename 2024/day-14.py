from pathlib import Path
import re

import numpy as np

with (Path(__file__).parent / "day-14.txt").open("rt") as file:
    lines = [line.strip() for line in file.readlines()]

width = 101
height = 103

# lines = [
#     "p=0,4 v=3,-3",
#     "p=6,3 v=-1,-3",
#     "p=10,3 v=-1,2",
#     "p=2,0 v=2,-1",
#     "p=0,0 v=1,3",
#     "p=3,0 v=-2,-2",
#     "p=7,6 v=-1,-3",
#     "p=3,0 v=-1,-2",
#     "p=9,3 v=2,3",
#     "p=7,3 v=-1,2",
#     "p=2,4 v=2,-3",
#     "p=9,5 v=-3,-3",
# ]

# width = 11
# height = 7

from collections import namedtuple
Robot = namedtuple("Robot", ["x0", "y0", "vx", "vy"])

robots = []

for line in lines:
    m = re.match(r"p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)", line)
    robots.append(Robot(int(m[1]), int(m[2]), int(m[3]), int(m[4])))

floor = np.zeros((height, width), dtype=np.int32)
for robot in robots:
    x = (robot.x0 + 100 * robot.vx) % width
    y = (robot.y0 + 100 * robot.vy) % height
    floor[y, x] += 1

nw = floor[:height//2, :width//2].sum()
ne = floor[:height//2, width//2+1:].sum()
sw = floor[height//2+1:, :width//2].sum()
se = floor[height//2+1:, width//2+1:].sum()

print(f"Safety factor = {nw} * {ne} * {sw} * {se} = {nw*ne*sw*se}")

print("Done.")
