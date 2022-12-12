#!/usr/bin/env python3

from functools import reduce
from typing import List

import numpy as np

from pathlib import Path
WORK_DIR = Path(__file__).parent.absolute()

with (WORK_DIR / "2017-10.txt").open("r") as handle:
    line = handle.readline()


def contents(source: List, index: int, count: int) -> List:
    return [source[i % len(source)] for i in range(index, index+count)]


def update(destination: List, index: int, count: int, source: List) -> None:
    for i in range(count):
        destination[(index+i) % len(destination)] = source[i]
    return


def main() -> None:
    lengths = [int(entry) for entry in line.split(',')]
    memory = np.arange(256, dtype=np.int32) # list(range(256))
    current_position = 0
    skip_size = 0
    for length in lengths:
        extract = contents(memory, current_position, length)
        reverse = np.array(list(reversed(extract)), dtype=np.int32)   # list(reversed(extract))
        update(memory, current_position, length, reverse)
        current_position += length + skip_size
        skip_size += 1

    product = memory[0] * memory[1]
    print(f'memory[0] = {memory[0]}, memory[1] = {memory[1]}, product = {product}')

    lengths = [int(b) for b in bytes(line, 'utf-8')]
    lengths.extend([17,31,73,47,23])
    memory = np.arange(256, dtype=np.int32) # list(range(256))
    current_position = 0
    skip_size = 0
    for _ in range(64):
        for length in lengths:
            extract = contents(memory, current_position, length)
            reverse = np.array(list(reversed(extract)), dtype=np.int32)
            update(memory, current_position, length, reverse)
            current_position += length + skip_size
            skip_size += 1

    hashstring = [reduce(lambda x, y: x ^ y, memory[start:start+16]) for start in range(0, 256, 16)]
    string = reduce(lambda x, y: x + f'{y:02x}', hashstring, '')
    print(f'Hash = {hashstring}')
    print(f'Hex  = {string}')

    return


if __name__ == "__main__":
    main()
