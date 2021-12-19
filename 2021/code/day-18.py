#! /usr/bin/env python3

from pathlib import Path

with Path("../inputs/18.txt").open("r") as handle:
    lines = list([eval(line.strip()) for line in handle.readlines()])

lines = [
    [1, 2],
    [[1, 2], 3],
    [9, [8, 7]],
    [[1, 9], [8, 5]],
    [[[[1, 2], [3, 4]], [[5, 6], [7, 8]]], 9],
    [[[9, [3, 8]], [[0, 9], 6]], [[[3, 7], [4, 9]], 3]],
    [[[[1, 3], [5, 3]], [[1, 3], [8, 7]]], [[[4, 9], [6, 9]], [[8, 2], [7, 3]]]],
]


def store(value, index, array):

    while len(array) <= index:
        array.append(False)
    array[index] = value

    return


def flatten(number, array=None, position=0):

    if array is None:
        array = []

    if isinstance(number, list):
        left, right = number
        flatten(left, array, 2*position+1)
        flatten(right, array, 2*position+2)
        store(True, position, array)
    else:
        store(number, position, array)

    return array


def previous(position, array):

    while True:
        if position == 0:
            return None

        if position % 2 == 0:   # right child
            position -= 1
            while isinstance(array[position], bool):
                if array[position] and ((2*position + 2) < len(array)):
                    position = 2*position + 2  # right child
                else:
                    return None     # no more children
        else:   # left child
            position -= 1
            position //= 2

        if not isinstance(array[position], bool):   # if not bool, then int
            break

    return position


def subsequent(position, array):

    if position == 0:
        return 

    while True:

        if position > len(array):
            return None

        if position % 2 == 1:   # left child
            position += 1       # goto right child
            while isinstance(array[position], bool):
                if array[position] and (2*position + 1 < len(array)):
                    position = 2*position + 1
                else:
                    return None     # no more children
        else:   # right child
            while position % 2 == 0:
                position -= 2
                position //= 2  # goto parent
                if position == 0:
                    return None

        if not isinstance(array[position], bool):   # if not boot, then int
            break

    return position


def reduce(array):

    while True:
        # Walk through level four looking for a deeply nested number to explode
        if len(array) > 31:
            while True:
                explosion = False
                end = min(63, len(array))   # level four in positions 31..62
                for i in range(31, end, 2):
                    if not isinstance(array[i], bool):  # if not bool, then int
                        left, right = array[i:i+2]
                        array[i] = array[i+1] = False
                        # Walk backward looking for regular number to increment by left
                        j = previous(i, array)
                        if j is not None:
                            array[j] += left
                        # Walk forward looking for regular number to increment by right
                        j = subsequent(i+1, array)
                        if j is not None:
                            array[j] += right
                        array[(i-1)//2] = 0
                        explosion = True
                        break   # exit for
                if not explosion:
                    break   # exit while

        # Look for value >= 10 to split
        split = False
        j = 0
        while True:
            j = subsequent(j, array)
            if j is not None:
                value = array[j]
                if value >= 10:
                    store(True, j, array)
                    store(value // 2, 2*j+1, array)
                    store((value+1) // 2, 2*j+2, array)
                    split = True
                    break
            else:
                break
        if not split:
            break

    while isinstance(array[-1], bool):
        array.pop()

    return array


flat = flatten([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])
reduced = reduce(flat)
flat = flatten([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
reduced = reduce(flat)

# explode
reduced = reduce(flatten([[[[[9, 8], 1], 2], 3], 4]))   # [[[[0,9],2],3],4]
reduced = reduce(flatten([7, [6, [5, [4, [3, 2]]]]]))   # [7,[6,[5,[7,0]]]]
reduced = reduce(flatten([[6, [5, [4, [3, 2]]]], 1]))   # [[6,[5,[7,0]]],3]
reduced = reduce(flatten([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]))   # [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
reduced = reduce(flatten([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]))    # [[3,[2,[8,0]]],[9,[5,[7,0]]]]

# split
reduced = reduce(flatten([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]))   # [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
reduced = reduce(flatten([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]))   # [[[[0,7],4],[[7,8],[0,13]]],[1,1]]


def add_snailfish(left, right):

    return [left, right]


temp = reduce(flatten(add_snailfish(lines[0], lines[1])))


pass
