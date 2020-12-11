#!/usr/bin python3


def passes(value):

    doubled = False
    decreasing = False

    digits = [(value // (10 ** power)) % 10 for power in range(6)]
    digits.reverse()

    prev = digits[0]
    for digit in range(1, 6):
        current = digits[digit]
        doubled |= current == prev
        decreasing |= current < prev
        prev = current

    return doubled and not decreasing


def additional(value):

    double = False
    decreasing = False

    digits = [(value // (10 ** power)) % 10 for power in range(6)]
    digits.reverse()

    prev = digits[0]
    same = 1
    for digit in range(1, 6):
        current = digits[digit]
        if current == prev:
            same += 1
        else:
            double |= same == 2
            same = 1
        decreasing |= current < prev
        prev = current

    double |= same == 2

    return double and not decreasing


def main():

    start = 165432
    end = 707912

    count = 0
    for test in range(start, end+1):
        if passes(test):
            count += 1

    print(f'{count} values meet the criteria.')

    count = 0
    for test in range(start, end+1):
        if additional(test):
            count += 1

    print(f'{count} values meet the additional criteria')

    return


if __name__ == '__main__':
    main()
