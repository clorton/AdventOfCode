#!/usr/bin/python

import os
import sys

print(os.getcwd())
os.chdir(os.environ['HOME'])
os.chdir('Coding/AdventOfCode/2017')
print(os.getcwd())

with open('2017-20.txt', 'r') as handle:
    lines = handle.readlines()

specs = [line.strip().split(', ') for line in lines]

"""
Originally, I figured “oh, we can just take the particle with the lowest absolute acceleration and that’ll be it!”, and
for my input I was actually correct. However after talking to a few people on the #AdventOfCode channel in KotlinSlack,
it turns out that that doesn't always work out.
https://todd.ginsberg.com/post/advent-of-code/2017/day20/
"""

minimum_acceleration = sys.float_info.max
minimum_velocity = sys.float_info.max
minimum_position = sys.float_info.max
index = -1
for i in range(len(specs)):
    position = sum(map(lambda x: x*x, [value for value in map(int, specs[i][0][3:-1].split(','))]), 0)
    velocity = sum(map(lambda x: x*x, [value for value in map(int, specs[i][1][3:-1].split(','))]), 0)
    acceleration = sum(map(lambda x: x*x, [value for value in map(int, specs[i][2][3:-1].split(','))]), 0)
    if acceleration < minimum_acceleration:
        minimum_acceleration = acceleration
        minimum_velocity = velocity
        minimum_position = position
        index = i
    elif acceleration == minimum_acceleration:
        if velocity < minimum_velocity:
            minimum_acceleration = acceleration
            minimum_velocity = velocity
            minimum_position = position
            index = i
        elif velocity == minimum_velocity:
            if position < minimum_position:
                minimum_acceleration = acceleration
                minimum_velocity = velocity
                minimum_position = position
                index = i

print('Particle {0} had minimum acceleration ({1})'.format(index, minimum_acceleration))

# 279: p=<-1103,   92,1785>, v=<  49, -4, -97>, a=<1,0, 0> |p0| = 2100.31, |v| = 108.75, |a| = 1
# 308: p=< 2978, 2082,4280>, v=<-135,-88,-178>, a=<1,0, 0> |p0| = 5614.41, |v| = 240.11, |a| = 1
# 435: p=< 2030,-4343,-355>, v=< -69,145,  25>, a=<0,0,-1> |p0| = 4807.14, |v| = 162.51, |a| = 1

# 279 is always accelerating away from the origin
# 308 moves toward the origin on the x axis for 135 steps before moving away
# 435 moves toward the origin on the z axis for 25 steps before moving away
