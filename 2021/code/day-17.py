#! /usr/bin/env python3

from datetime import datetime
from math import sqrt, ceil

t_start = datetime.now()

minimum_x = 281
maximum_x = 311
minimum_y = -74
maximum_y = -54

# Part 1

# Every positive dy will be a parabola which returns to y=0 and then descends (dy+1) steps further
# -(dy+1) = minimum_y
# dy + 1 = -minimum_y
# dy = -minimum_y - 1

best_dy = -(minimum_y+1)
print(f"Maximum height comes from an initial dy of {best_dy}")
maximum_height = best_dy * (best_dy+1) // 2
print(f"Maximum height will be {maximum_height}")

# Part 2


def step(x, y, dx, dy):

    x += dx
    y += dy
    if dx != 0:
        dx -= dx / abs(dx)
    dy -= 1

    return x, y, dx, dy


def find_dx(min_x, max_x):

    valid = []

    # dx decreases from its initial value to 0 so the sum of the steps
    # is dx * (dx+1) / 2, this sum must at least reach the minimum x
    # n*(n+1)//2 >= min_x
    # (n^2 + n)//2 = min_x
    # n^2 + n = 2 * min_x
    # n^2 + n - 2*min_x = 0
    # n = (-b +- sqrt(b^2 - 4ac))/(2*a)
    n = (-1 + sqrt(1 - 4 * -2 * min_x))/2
    start_dx = int(ceil(n))
    stop_dx = max_x

    for test in range(start_dx, stop_dx+1):
        x = 0
        y = 0
        dx = test
        dy = 0
        while dx != 0:
            x, y, dx, dy = step(x, y, dx, dy)
            if (min_x <= x) and (x <= max_x):
                valid.append(test)
                break

    return valid


def part2():
    valid_dx = find_dx(minimum_x, maximum_x)
    valid_count = 0
    for test_dx in valid_dx:
        for test_dy in range(minimum_y, best_dy+1):
            x = 0
            y = 0
            dx = test_dx
            dy = test_dy
            while y > minimum_y:
                x, y, dx, dy = step(x, y, dx, dy)
                if (minimum_x <= x) and (x <= maximum_x) and (minimum_y <= y) and (y <= maximum_y):
                    valid_count += 1
                    break

    return valid_count


print(f"Valid trajectories = {part2()}")

t_finish = datetime.now()
print(f"Elapsed = {t_finish-t_start}")

pass
