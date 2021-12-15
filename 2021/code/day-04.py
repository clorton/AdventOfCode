#! /usr/bin/env python3

from pathlib import Path
import numpy as np

with Path("../inputs/04.txt").open("r") as handle:
    lines = [line.strip() for line in handle.readlines() if line != "\n"]

prng = lines.pop(0)
prng = list(map(int, prng.split(",")))

lines = [list(map(int, line.split())) for line in lines]


class Board():
    def __init__(self, array):
        self.array = array
        self.row_sums = np.zeros(5, dtype=np.uint32)
        self.column_sums = np.zeros(5, dtype=np.uint32)
        return

    def check(self, value):
        row, column = (self.array == value).nonzero()
        if row.shape[0]:
            row, column = row[0], column[0]
            self.row_sums[row] += 1
            self.column_sums[column] += 1
            if (self.row_sums[row] == 5) or (self.column_sums[column] == 5):
                return True
        return False


boards = []
for i in range(0, len(lines), 5):
    board = np.array(lines[i:i+5])
    boards.append(Board(board))

bingo = False
for i, value in enumerate(prng):
    for j, board in enumerate(boards):
        if board.check(value):
            print(f"Bingo on board {j}")
            board_numbers = set(board.array.flatten())
            called_numbers = set(prng[0:i+1])
            remaining = board_numbers - called_numbers
            total = sum(remaining)
            answer = value * total
            print(f"Answer is {answer}")
            bingo = True
            break
    if bingo:
        break

active_boards = [Board(board.array) for board in boards]
for i, value in enumerate(prng):
    tmp = []
    while len(active_boards):
        board = active_boards.pop(0)
        if board.check(value):
            last_board = board
            last_index = i
            last_value = value
        else:
            tmp.append(board)
    active_boards = tmp

board_numbers = set(last_board.array.flatten())
called_numbers = set(prng[0:last_index+1])
remaining = board_numbers - called_numbers
total = sum(remaining)
answer = total * last_value
print(f"{answer=}")


pass
