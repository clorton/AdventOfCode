#! /usr/bin/env python3


def requirement(mass):

    req = mass // 3
    req -= 2

    return req


def requirement2(mass):

    total = 0
    fuel = requirement(mass)
    while fuel > 0:
        total += fuel
        fuel = requirement(fuel)

    return total


def main():

    requirement2(14)
    requirement2(1969)
    requirement2(100756)

    with open('day-01.txt', 'r') as file:
        lines = file.readlines()

    masses = [int(line) for line in lines]

    initial = 0
    for mass in masses:
        initial += requirement(mass)

    print(f'Part 1 - Initial fuel requirement is {initial}')     # 3297866 :)

    # total = 0
    # extra = initial
    # while extra > 0:
    #     total += extra
    #     extra = requirement(extra)
    #
    # print(f'Final total fuel is {total}')   # 4946754 :( - too high

    fuel = 0
    for mass in masses:
        fuel += requirement2(mass)

    print(f'Part 2 - Final total fuel is {fuel}')    # 4943923 :)

    return


if __name__ == '__main__':
    main()
