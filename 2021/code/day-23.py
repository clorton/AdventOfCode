#! /usr/bin/env python3

from collections import namedtuple
from heapq import heappush, heappop
import numpy as np

"""
#############
#...........#
###D#C#D#B###
  #B#A#A#C#
  #########
"""

FREE = "."
WALL = "#"

board = [
    list("#############"),
    list("#...........#"),
    list("###D#C#D#B###"),
    list("  #B#A#A#C#  "),
    list("  #########  ")
]

board = [
    list("#############"),
    list("#...........#"),
    list("###B#C#B#D###"),
    list("###A#D#C#A###"),
    list("#############")
]

board = np.array(board, dtype=np.unicode_)


def print_board(array):
    for row in range(array.shape[0]):
        print("".join(array[row, :]))
    return


print_board(board)

Location = namedtuple("Location", ["x", "y"])

hallway = [
    Location(1, 1),
    Location(2, 1),
    Location(4, 1),
    Location(6, 1),
    Location(8, 1),
    Location(10, 1),
    Location(11, 1)
]

slots = [
    Location(3, 2),
    Location(5, 2),
    Location(7, 2),
    Location(9, 2),
    Location(3, 3),
    Location(5, 3),
    Location(7, 3),
    Location(9, 3)
]

homes = {
    "A": [Location(3, 3), Location(3, 2)],
    "B": [Location(5, 3), Location(5, 2)],
    "C": [Location(7, 3), Location(7, 2)],
    "D": [Location(9, 3), Location(9, 2)]
}

Amphipod = namedtuple("Amphipod", ["kind", "location"])


def get_pods(state):

    pods = []
    height, width = state.shape
    for y in range(1, height-1):
        for x in range(1, width-1):
            if state[y, x] in list("ABCD"):
                pods.append(Amphipod(state[y, x], Location(x, y)))

    return pods


Move = namedtuple("Move", ["cost", "amphipod", "finish"])


def get_moves(amphipods, state):

    # valid_locations = list(hallway)
    # valid_locations.extend(slots)
    valid_locations = list(map(lambda l: Location(l[1], l[0]), zip(*np.nonzero(state == FREE))))
    possible = []
    for amphipod in amphipods:
        for finish in valid_locations:
            if can_move(amphipod.location, finish, state) and may_move(amphipod.kind, amphipod.location, finish, state):
                possible.append(Move(move_cost(amphipod, finish), amphipod, finish))

    return sorted(possible, key=lambda p: p.cost)


def can_move(start, finish, state):
    if state[finish.y, finish.x] != FREE:
        return False

    if finish.x == start.x:
        return False

    dx = finish.x - start.x
    dx = dx // abs(dx)
    cx, cy = start
    if start in hallway:
        # move horizontal first
        while cx != finish.x:
            cx += dx
            if state[cy, cx] != FREE:
                return False
        # move vertical second
        while cy != finish.y:
            cy += 1
            if state[cy, cx] != FREE:
                return False
    else:  # assume in slot
        # move vertical first
        while cy != finish.y:
            cy -= 1
            if state[cy, cx] != FREE:
                return False
        # move horizontal second
        while cx != finish.x:
            cx += dx
            if state[cy, cx] != FREE:
                return False

    return True


def may_move(pod, start, finish, state):

    if start == homes[pod][0]:
        return False

    if start == homes[pod][1] and state[homes[pod][0].y, homes[pod][0].x] == pod:
        return False

    if finish in hallway:
        return start not in hallway     # slot to hallway okay, hallway to hallway not

    # finish in slot, check validity
    valid = {"A": 3, "B": 5, "C": 7, "D": 9}
    if finish.x == valid[pod]:
        # move to bottom _or_ bottom already occupied by this kind of pod
        return (finish.y == 3) or (board[finish.y, finish.x] == pod)

    return False


def move_cost(pod, finish):

    costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
    m_dist = abs(finish.x - pod.location.x) + abs(finish.y - pod.location.y)
    return m_dist * costs[pod.kind]


# moves = get_moves(get_pods(board), board)

Solution = namedtuple("Solution", ["cost", "moves", "state"])


def solved(state):

    for kind, locations in homes.items():
        for location in locations:
            if state[location.y, location.x] != kind:
                return False

    return True


solutions = [Solution(0, [], board)]
proposals = 0
while True:
    proposed: Solution
    proposed = heappop(solutions)
    if solved(proposed.state):
        break
    proposals += 1
    if proposals % 1000 == 0:
        print(f"{proposals=}")
        print_board(proposed.state)
    pods = get_pods(proposed.state)
    moves = get_moves(pods, proposed.state)
    for move in moves:
        if move not in proposed.moves:
            new_cost = proposed.cost + move.cost
            proposed_moves = list(proposed.moves)
            proposed_moves.append(move)
            new_state = np.array(proposed.state, dtype=proposed.state.dtype)
            new_state[move.amphipod.location.y, move.amphipod.location.x] = FREE
            new_state[move.finish.y, move.finish.x] = move.amphipod.kind
            heappush(solutions, Solution(new_cost, proposed_moves, new_state))

pass
