#!/usr/bin/python

import numpy


def main():

    # buffer = [0]
    # index = 0
    # for i in range(1, 2018):
    #     increment = 382 % len(buffer)
    #     index += increment
    #     index %= len(buffer)
    #     head = buffer[0:index+1]
    #     head.append(i)
    #     tail = buffer[index+1:] if index + 1 < len(buffer) else []
    #     head.extend(tail)
    #     buffer = head
    #     index += 1
    #
    # location = buffer.index(2017)
    # print('Next value is {0}'.format(buffer[(location+1)%len(buffer)]))
    #
    # buffer = [0]
    # index = 0
    # for i in range(1, 50000000):
    #     increment = 382 % len(buffer)
    #     index += increment
    #     index %= len(buffer)
    #     head = buffer[0:index+1]
    #     head.append(i)
    #     tail = buffer[index+1:] if index + 1 < len(buffer) else []
    #     head.extend(tail)
    #     buffer = head
    #     index += 1
    #
    # location = buffer.index(0)
    # print('Next value is {0}'.format(buffer[(location+1)%len(buffer)]))

    angry_spinlock(2018, 2017)
    angrier_spinlock(count=10, step=3)
    angrier_spinlock(count=50000000, step=382)

    return


def angry_spinlock(count, target):

    buffer = numpy.zeros(count)
    index = 0
    length = 1
    for i in range(1, count):
        increment = 382 % length
        index += increment
        index %= length
        for j in range(length, index, -1):
            buffer[j] = buffer[j-1]
        buffer[index] = i
        index += 1
        length += 1

    for i in range(len(buffer)):
        if buffer[i] == target:
            print('Next value is {0}'.format(buffer[(i+1)%len(buffer)]))
            break

    return


def angrier_spinlock(count=50000000, step=382):

    index = 0
    length = 1
    next = None
    for i in range(1, count):
        index += 382 % length
        index %= length
        if index == 0:
            next = i
        index += 1
        length += 1

    print('Next value is {0}'.format(next))

    return


if __name__ == '__main__':
    main()
