#!/usr/bin/env python3


from collections import namedtuple
from math import gcd


def lcm(numbers):
    least_common_multiple = numbers[0]
    for number in numbers[1:]:
        least_common_multiple = int(least_common_multiple * number / gcd(least_common_multiple, number))

    return least_common_multiple


Position = namedtuple("Position", ["x", "y", "z"])
Velocity = namedtuple("Velocity", ["dx", "dy", "dz"])
Moon = namedtuple("Moon", ["position", "velocity"])


def main():

    # with open("day-12.txt", "r") as file:
    #     inputs = file.read().strip()

    def delta(a, b):
        return 1 if b > a else -1 if b < a else 0

    moons = [
        Moon([3, 15, 8], [0, 0, 0]),
        Moon([5, -1, -2], [0, 0, 0]),
        Moon([-10, 8, 2], [0, 0, 0]),
        Moon([8, 4, -5],  [0, 0, 0])
    ]
    time_steps = 1000

    # Test 1
    # moons = [
    #     Moon([-1, 0, 2], [0, 0, 0]),
    #     Moon([2, -10, -7], [0, 0, 0]),
    #     Moon([4, -8, 8], [0, 0, 0]),
    #     Moon([3, 5, -1],  [0, 0, 0])
    # ]
    # time_steps = 10

    # Test 2
    # moons = [
    #     Moon([-8, -10, 0], [0, 0, 0]),
    #     Moon([5, 5, 10], [0, 0, 0]),
    #     Moon([2, -7, 3], [0, 0, 0]),
    #     Moon([9, -8, -3],  [0, 0, 0])
    # ]
    # time_steps = 100

    def do_step(_moons):
        for _moon in _moons:
            for _other in _moons:
                if _other != _moon:
                    _moon.velocity[0] += delta(_moon.position[0], _other.position[0])
                    _moon.velocity[1] += delta(_moon.position[1], _other.position[1])
                    _moon.velocity[2] += delta(_moon.position[2], _other.position[2])

        for _moon in _moons:
            _moon.position[0] += _moon.velocity[0]
            _moon.position[1] += _moon.velocity[1]
            _moon.position[2] += _moon.velocity[2]

    for time_step in range(time_steps):
        do_step(moons)

    system = 0
    for moon in moons:
        potential = abs(moon.position[0]) + abs(moon.position[1]) + abs(moon.position[2])
        kinetic = abs(moon.velocity[0]) + abs(moon.velocity[1]) + abs(moon.velocity[2])
        total = potential * kinetic
        print(f"potential {potential} + kinetic {kinetic} = total {total}")
        system += total

    print(f"sum = {system}")

    # Part 2

    moons = [
        Moon([3, 15, 8], [0, 0, 0]),
        Moon([5, -1, -2], [0, 0, 0]),
        Moon([-10, 8, 2], [0, 0, 0]),
        Moon([8, 4, -5],  [0, 0, 0])
    ]

    targets = [
        Moon([3, 15, 8], [0, 0, 0]),
        Moon([5, -1, -2], [0, 0, 0]),
        Moon([-10, 8, 2], [0, 0, 0]),
        Moon([8, 4, -5],  [0, 0, 0])
    ]

    # Test 1
    # moons = [
    #     Moon([-1, 0, 2], [0, 0, 0]),
    #     Moon([2, -10, -7], [0, 0, 0]),
    #     Moon([4, -8, 8], [0, 0, 0]),
    #     Moon([3, 5, -1],  [0, 0, 0])
    # ]
    #
    # targets = [
    #     Moon([-1, 0, 2], [0, 0, 0]),
    #     Moon([2, -10, -7], [0, 0, 0]),
    #     Moon([4, -8, 8], [0, 0, 0]),
    #     Moon([3, 5, -1],  [0, 0, 0])
    # ]

    # Test 2
    # moons = [
    #     Moon([-8, -10, 0], [0, 0, 0]),
    #     Moon([5, 5, 10], [0, 0, 0]),
    #     Moon([2, -7, 3], [0, 0, 0]),
    #     Moon([9, -8, -3],  [0, 0, 0])
    # ]
    #
    # targets = [
    #     Moon([-8, -10, 0], [0, 0, 0]),
    #     Moon([5, 5, 10], [0, 0, 0]),
    #     Moon([2, -7, 3], [0, 0, 0]),
    #     Moon([9, -8, -3],  [0, 0, 0])
    # ]

    State = namedtuple("State", ["p0", "p1", "p2", "v0", "v1", "v2"])

    cycles = [0, 0, 0]
    for dimension in range(3):
        for moon in range(4):
            moons[moon].position[0] = targets[moon].position[0]
            moons[moon].position[1] = targets[moon].position[1]
            moons[moon].position[2] = targets[moon].position[2]
            moons[moon].velocity[0] = moons[moon].velocity[1] = moons[moon].velocity[2] = 0

        time_step = 0
        initial = State(moons[0].position[dimension],
                        moons[1].position[dimension],
                        moons[2].position[dimension],
                        moons[0].velocity[dimension],
                        moons[1].velocity[dimension],
                        moons[2].velocity[dimension])
        states = set()
        states.add(initial)
        steps = [initial]

        while True:
            do_step(moons)

            time_step += 1

            current = State(moons[0].position[dimension],
                            moons[1].position[dimension],
                            moons[2].position[dimension],
                            moons[0].velocity[dimension],
                            moons[1].velocity[dimension],
                            moons[2].velocity[dimension])

            if current in states:
                cycles[dimension] = time_step
                print(f"At time step {time_step} found state {current} in states - previous at {steps.index(current)}")
                break
            else:
                states.add(current)
                steps.append(current)

    print(f"Cycles = {cycles}")
    print(f"LCM of cycles is {lcm(cycles)}")

    return


if __name__ == "__main__":
    main()
