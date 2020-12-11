#!/usr/bin/env python3

from collections import namedtuple
from fractions import Fraction
import math
import numpy as np


Point = namedtuple('Point', ["x", "y"])
Line = namedtuple('Line', ["m", "b"])
Slope = namedtuple("Slope", ["fraction", "side"])

PLUS_ZERO = "+0"
MINUS_ZERO = "-0"
PLUS_INF = "+INF"
MINUS_INF = "-INF"
LEFT = "left"
RIGHT = "right"


def main():

    with open('day-10.txt', 'r') as file:
        inputs = [line.strip() for line in file.readlines()]

    # inputs = [
    #     ".#..#",
    #     ".....",
    #     "#####",
    #     "....#",
    #     "...##"
    # ]   # x = 3, y = 4 => 8

    # inputs = [
    #     "......#.#.",
    #     "#..#.#....",
    #     "..#######.",
    #     ".#.#.###..",
    #     ".#..#.....",
    #     "..#....#.#",
    #     "#..#....#.",
    #     ".##.#..###",
    #     "##...#..#.",
    #     ".#....####"
    # ]   # x=5, y=8 => 33

    # inputs = [
    #     "#.#...#.#.",
    #     ".###....#.",
    #     ".#....#...",
    #     "##.#.#.#.#",
    #     "....#.#.#.",
    #     ".##..###.#",
    #     "..#...##..",
    #     "..##....##",
    #     "......#...",
    #     ".####.###."
    # ]   # x = 1, y = 2 => 35

    # inputs = [
    #     ".#..#..###",
    #     "####.###.#",
    #     "....###.#.",
    #     "..###.##.#",
    #     "##.##.#.#.",
    #     "....###..#",
    #     "..#.#..#.#",
    #     "#..#.#.###",
    #     ".##...##.#",
    #     ".....#.#.."
    # ]   # x=6, y=3 => 41

    # inputs = [
    #     ".#..##.###...#######",
    #     "##.############..##.",
    #     ".#.######.########.#",
    #     ".###.#######.####.#.",
    #     "#####.##.#.##.###.##",
    #     "..#####..#.#########",
    #     "####################",
    #     "#.####....###.#.#.##",
    #     "##.#################",
    #     "#####.##.###..####..",
    #     "..######..##.#######",
    #     "####.##.####...##..#",
    #     ".#####..#.######.###",
    #     "##...#.##########...",
    #     "#.##########.#######",
    #     ".####.#.###.###.#.##",
    #     "....##.##.###..#####",
    #     ".#.#.###########.###",
    #     "#.#.#.#####.####.###",
    #     "###.##.####.##.#..##"
    # ]   # x = 11, y = 13 => 210

    grid = np.zeros((len(inputs), len(inputs[0])), dtype=np.uint32)
    for y in range(len(inputs)):
        for x in range(len(inputs[0])):
            grid[y, x] = 1 if inputs[y][x] != '.' else 0

    sight_lines = {}
    for y0 in range(grid.shape[0]):
        for x0 in range(grid.shape[1]):
            if grid[y0, x0] != 0:
                point = Point(x0, y0)
                asteroids = set()
                sight_lines[point] = asteroids
                for y1 in range(grid.shape[0]):
                    for x1 in range(grid.shape[1]):
                        if grid[y1, x1] != 0:
                            if y1 != y0 or x1 != x0:
                                if y1 == y0:    # +/-0
                                    slope = PLUS_ZERO if x1 > x0 else MINUS_ZERO
                                elif x1 == x0:  # +/-inf
                                    slope = PLUS_INF if y1 > y0 else MINUS_INF
                                else:
                                    slope = Slope(Fraction((y1 - y0), (x1 - x0)), LEFT if x0 < x1 else RIGHT)
                                asteroids.add(slope)
                                # if x1 == 5 and y1 == 8:
                                #     print(f"Adding {slope}...")
    maximum = -1
    best = None
    for point in sight_lines:
        if len(sight_lines[point]) > maximum:
            maximum = len(sight_lines[point])
            best = point

    print(f"Best point {best} can see {maximum} asteroids.")

    # Part 2

    x0 = 14
    y0 = 17
    asteroids = {}
    for y1 in range(grid.shape[0]):
        for x1 in range(grid.shape[1]):
            if y1 != y0 or x1 != x0:
                if grid[y1, x1] != 0:
                    asteroids[Point(x1, y1)] = (math.atan2(y1-y0, x1-x0)+(math.pi/2))%(2*math.pi)

    targets = {}
    for asteroid in asteroids:
        angle = asteroids[asteroid]
        if angle not in targets:
            targets[angle] = set()
        targets[angle].add(asteroid)

    counter = 1
    index = 0
    angles = sorted(targets.keys())
    while counter <= 200:
        actual = index % len(angles)
        bodies = targets[angles[actual]]
        bodies = sorted(bodies, key=lambda b: abs(x0 - b.x) + abs(y0 - b.y))
        if counter == 200:
            print(f"{counter}: zotting asteroid at {bodies[0]} ({bodies[0].x*100+bodies[0].y})...")
        targets[angles[actual]].remove(bodies[0])
        if len(targets[angles[actual]]) == 0:
            targets.pop(angles[actual])
            angles.remove(angles[actual])
        else:
            index += 1
        counter += 1

    return


if __name__ == "__main__":
    main()
