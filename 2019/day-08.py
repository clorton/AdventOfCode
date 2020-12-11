#!/usr/bin/env python3

import numpy as np


def main():

    with open('day-08.txt', "r") as file:
        data = file.read()

    # Part 1

    pixel_data = np.zeros(len(data), dtype=np.uint32)
    i = 0
    for digit in data:
        pixel_data[i] = ord(digit) - ord('0')
        i += 1

    layers = len(data) // (6*25)
    pixel_data = pixel_data.reshape((layers, 6, 25))

    info = {}
    minimum = 6*25
    index = -1
    for l in range(layers):
        counts = np.unique(pixel_data[l, :, :], return_counts=True)
        info[l] = counts[1]
        # print(f"{l}: {counts}")
        if int(counts[1][0]) < minimum:
            minimum = counts[1][0]
            index = l

    print(f"Minimum {minimum} on layer {index}, product {info[index][1] * info[index][2]}")

    # Part 2

    image = [[' ' for _ in range(25)] for __ in range(6)]
    for x in range(25):
        for y in range(6):
            for l in range(layers):
                if pixel_data[l, y, x] != 2:
                    image[y][x] = ' ' if pixel_data[l, y, x] == 0 else '*'
                    break

    for row in range(6):
        print(''.join(image[row]))

    return


if __name__ == "__main__":
    main()
