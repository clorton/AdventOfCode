#! /usr/bin/env python3

from pathlib import Path
import numpy as np

with Path("../inputs/22.txt").open("r") as handle:
    lines = list([line.strip() for line in handle.readlines()])

splines = [
    "on x=10..12,y=10..12,z=10..12",
    "on x=11..13,y=11..13,z=11..13",
    "off x=9..11,y=9..11,z=9..11",
    "on x=10..10,y=10..10,z=10..10"
]

inclines = [
    "on x=-20..26,y=-36..17,z=-47..7",
    "on x=-20..33,y=-21..23,z=-26..28",
    "on x=-22..28,y=-29..23,z=-38..16",
    "on x=-46..7,y=-6..46,z=-50..-1",
    "on x=-49..1,y=-3..46,z=-24..28",
    "on x=2..47,y=-22..22,z=-23..27",
    "on x=-27..23,y=-28..26,z=-21..29",
    "on x=-39..5,y=-6..47,z=-3..44",
    "on x=-30..21,y=-8..43,z=-13..34",
    "on x=-22..26,y=-27..20,z=-29..19",
    "off x=-48..-32,y=26..41,z=-47..-37",
    "on x=-12..35,y=6..50,z=-50..-2",
    "off x=-48..-32,y=-32..-16,z=-15..-5",
    "on x=-18..26,y=-33..15,z=-7..46",
    "off x=-40..-22,y=-38..-28,z=23..41",
    "on x=-16..35,y=-41..10,z=-47..6",
    "off x=-32..-23,y=11..30,z=-14..3",
    "on x=-49..-5,y=-3..45,z=-29..18",
    "off x=18..30,y=-20..-8,z=-3..13",
    "on x=-41..9,y=-7..43,z=-33..15",
    "on x=-54112..-39298,y=-85059..-49293,z=-27449..7877",
    "on x=967..23432,y=45373..81175,z=27513..53682",
]


class Instruction:

    def __init__(self, text):
        self.inst, coordinates = text.split(" ")
        xs, ys, zs = list(map(lambda s: s[2:].split(".."), coordinates.split(",")))
        self.x1, self.x2 = list(map(int, xs))
        self.y1, self.y2 = list(map(int, ys))
        self.z1, self.z2 = list(map(int, zs))

        return


class Prism:

    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1, self.x2 = x1, x2
        self.y1, self.y2 = y1, y2
        self.z1, self.z2 = z1, z2
        return

    @staticmethod
    def overlap(l1, l2, r1, r2):
        left = max(l1, l2)
        right = min(r1, r2)
        return (left, right) if left <= right else None

    def intersects(self, other):

        xs = self.overlap(self.x1, other.x1, self.x2, other.x2)
        ys = self.overlap(self.y1, other.y1, self.y2, other.y2)
        zs = self.overlap(self.z1, other.z1, self.z2, other.z2)
        if xs and ys and zs:
            return xs, ys, zs

        return None


lines = list([Instruction(line) for line in lines])


def part1(instructions):
    min_x = min_y = min_z = -50
    max_x = max_y = max_z = 50

    width = (max_x + 1) - min_x
    height = (max_y + 1) - min_y
    depth = (max_z + 1) - min_z

    voxels = np.zeros((depth, height, width), dtype=np.uint32)

    for instruction in instructions:
        x1 = instruction.x1 - min_x
        x2 = instruction.x2 - min_x
        y1 = instruction.y1 - min_y
        y2 = instruction.y2 - min_y
        z1 = instruction.z1 - min_z
        z2 = instruction.z2 - min_z
        if (x1 >= 0) and (x1 <= width) and (x2 >= 0) and (x2 <= width) and \
            (y1 >= 0) and (y1 <= height) and (y2 >= 0) and (y2 <= height) and \
            (z1 >= 0) and (z1 <= depth) and (z2 >= 0) and (z2 <= depth):
            if instruction.inst == "on":
                voxels[z1:z2+1, y1:y2+1, x1:x2+1] |= 1
            else:
                voxels[z1:z2+1, y1:y2+1, x1:x2+1] &= 0

    print(f"{np.count_nonzero(voxels)=}")

    return


part1(lines)


def part2(instructions):

    for instruction in instructions:
        if instruction.inst == "on":
            pass
        else:
            pass

    return


pass
