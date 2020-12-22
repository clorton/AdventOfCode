#! /usr/bin/env python3

from collections import deque
from hashlib import sha256
from pathlib import Path

text = (Path(__file__).parent.absolute() / "day-22.txt").read_text()

_ = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

halfone, halftwo = text.split("\n\n")
halfone = halfone.split("\n")[1:]
halftwo = halftwo.split("\n")[1:]
player1 = deque([int(card) for card in halfone])
player2 = deque([int(card) for card in halftwo])

# part 1
while len(player1) > 0 and len(player2) > 0:
    card1 = player1.popleft()
    card2 = player2.popleft()
    if card1 > card2:
        player1.extend([card1, card2])
    else:
        player2.extend([card2, card1])

winner = player1 if len(player1) > 0 else player2
value = len(winner)
score = 0
for card in winner:
    score += card * value
    value -= 1

print(f"Winner's score is {score}")

# part 2
player1 = deque([int(card) for card in halfone])
player2 = deque([int(card) for card in halftwo])
PLAYER1 = 0
PLAYER2 = 1


def hashed(iterable):
    return sha256("".join([f"{x:02}" for x in iterable]).encode("utf-8")).hexdigest()

GAME = 0
def play_game(p1, p2):

    global GAME
    GAME += 1
    round = 0

    seen = (set(), set())
    while len(p1) > 0 and len(p2) > 0:
        round += 1
        # print(f"Round {round} (Game {GAME})")
        h1 = hashed(p1)
        h2 = hashed(p2)
        if h1 in seen[PLAYER1] and h2 in seen[PLAYER2]:
            # print(f"Saw same configuration, player 1 wins.")
            return PLAYER1, p1
        seen[PLAYER1].update([h1])
        seen[PLAYER2].update([h2])
        c1 = p1.popleft()
        c2 = p2.popleft()
        if len(p1) >= c1 and len(p2) >= c2:
            p1p = deque([p1[i] for i in range(c1)])
            p2p = deque([p2[i] for i in range(c2)])
            w, _ = play_game(p1p, p2p)
            if w == PLAYER1:
                p1.extend([c1, c2])
            else:
                p2.extend([c2, c1])
        else:
            if c1 > c2:
                p1.extend([c1, c2])
            else:
                p2.extend([c2, c1])

    return (PLAYER1, p1) if len(p1) > 0 else (PLAYER2, p2)


win, hand = play_game(player1, player2)
value = len(hand)
score = 0
for card in hand:
    score += card * value
    value -= 1

print(f"Winner's score is {score}")

print(".oO( done )")
