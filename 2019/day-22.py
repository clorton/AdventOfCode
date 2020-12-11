#!/usr/bin/env python3

import numpy as np


def deal_into_new(deck):

    return deck[::-1]


def deal_with_increment(deck, increment):

    length = len(deck)
    new_deck = np.zeros(length)
    for i in range(length):
        new_deck[(i*increment)%length] = deck[i]

    return new_deck


def cut_cards(deck, count):

    return np.roll(deck, -count)


def main():

    # deck = np.zeros(10)
    # for i in range(10):
    #     deck[i] = i

    # deck = deal_with_increment(deck, 7)
    # deck = deal_into_new(deck)
    # deck = deal_into_new(deck)
    # # Result: 0 3 6 9 2 5 8 1 4 7

    # deck = cut_cards(deck, 6)
    # deck = deal_with_increment(deck, 7)
    # deck = deal_into_new(deck)
    # # Result: 3 0 7 4 1 8 5 2 9 6

    # deck = deal_with_increment(deck, 7)
    # deck = deal_with_increment(deck, 9)
    # deck = cut_cards(deck, -2)
    # # Result: 6 3 0 7 4 1 8 5 2 9

    # deck = deal_into_new(deck)
    # deck = cut_cards(deck, -2)
    # deck = deal_with_increment(deck, 7)
    # deck = cut_cards(deck, 8)
    # deck = cut_cards(deck, -4)
    # deck = deal_with_increment(deck, 7)
    # deck = cut_cards(deck, 3)
    # deck = deal_with_increment(deck, 9)
    # deck = deal_with_increment(deck, 3)
    # deck = cut_cards(deck, -1)
    # # Result: 9 2 5 8 1 4 7 0 3 6

    # print(f"{deck}")

    with open("day-22.txt", "r") as file:
        instructions = [line.strip() for line in file.readlines()]

    LENGTH = 10007
    deck = np.zeros(LENGTH, dtype=np.int32)
    for i in range(LENGTH):
        deck[i] = i

    def process(_deck, _instructions):
        for instruction in _instructions:
            if instruction == "deal into new stack":
                _deck = deal_into_new(_deck)
            elif instruction.startswith("deal with increment"):
                parameter = int(instruction.split()[-1])
                _deck = deal_with_increment(_deck, parameter)
            elif instruction.startswith("cut"):
                parameter = int(instruction.split()[-1])
                _deck = cut_cards(_deck, parameter)
            else:
                raise RuntimeError(f"Unknown instruction '{instruction}'")
        return _deck

    deck = process(deck, instructions)

    TARGET = 2019
    position = None
    for i in range(LENGTH):
        if deck[i] == TARGET:
            position = i
            break

    print(f"Found {TARGET} at position {position}.")

    goal = np.zeros_like(deck)
    for i in range(LENGTH):
        goal[i] = deck[i] = i

    def equals(a, b):
        return not any(map(lambda x, y: x != y, a, b))

    count = 0
    while True:
        deck = process(deck, instructions)
        count += 1
        if equals(deck, goal):
            break

    print(f"Found cycle after {count} steps.")
    TIMES = 101741582076661
    print(f"{TIMES} % {count} = {TIMES % count}")

    return


if __name__ == "__main__":
    main()
