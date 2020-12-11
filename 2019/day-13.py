#!/usr/bin/env python3

from intcode import Computer

EMPTY = " "
WALL = "#"
BLOCK = "X"
PADDLE = "="
BALL = "*"


def main():

    with open("day-13.txt", "r") as file:
        inputs = [line.strip() for line in file.readlines()]

    program = [int(entry) for entry in inputs[0].split(",")]

    # Part 1

    computer = Computer(program, [])
    outputs = []
    while True:
        output = computer.run()
        if output is None:
            break
        outputs.append(output)

    max_x = 0
    max_y = 0
    for i in range(0, len(outputs), 3):
        max_x = max(max_x, outputs[i])
        max_y = max(max_y, outputs[i+1])

    board = [[EMPTY for _ in range(max_x+1)] for __ in range(max_y+1)]

    for i in range(0, len(outputs), 3):
        x = outputs[i]
        y = outputs[i+1]
        tile = outputs[i+2]
        if tile == 0:
            board[y][x] = EMPTY
        elif tile == 1:
            board[y][x] = WALL
        elif tile == 2:
            board[y][x] = BLOCK
        elif tile == 3:
            board[y][x] = PADDLE
        elif tile == 4:
            board[y][x] = BALL
        else:
            raise RuntimeError(f"Unknown tile {tile}")

    blocks = 0
    for row in board:
        for column in row:
            blocks += 1 if column == BLOCK else 0

    for row in board:
        print(f"{''.join(row)}")

    print(f"Found {blocks} blocks on the board.")

    # Part 2

    game = list(program)
    game[0] = 2
    arcade = Computer(game, [])
    screen = [[EMPTY for _ in range(max_x+1)] for __ in range(max_y+1)]
    joystick = [0]
    ball_x = None
    paddle_x = None

    counter = 0
    while True:
        output = arcade.run(joystick)
        counter += 1
        if output is None:
            # for row in screen:
            #     print(f"{''.join(row)}")
            break
        outputs = [output, arcade.run(), arcade.run()]
        counter += 2
        if len(outputs) == 3:
            x, y, tile = outputs
            if x == -1:
                print(f"Score is {tile}")
            elif tile == 0:
                screen[y][x] = EMPTY
            elif tile == 1:
                screen[y][x] = WALL
            elif tile == 2:
                screen[y][x] = BLOCK
            elif tile == 3:
                screen[y][x] = PADDLE
                paddle_x = x
                if ball_x is not None and paddle_x is not None:
                    joystick = [-1 if ball_x < paddle_x else 1 if ball_x > paddle_x else 0]
            elif tile == 4:
                screen[y][x] = BALL
                ball_x = x
                if ball_x is not None and paddle_x is not None:
                    joystick = [-1 if ball_x < paddle_x else 1 if ball_x > paddle_x else 0]
            else:
                raise RuntimeError(f"Unknown tile {tile}")

    return


if __name__ == "__main__":
    main()
