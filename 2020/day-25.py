#! /usr/bin/env python3

key1 = 15733400
key2 = 6408062


# part 1
def transform(subject_number, loop_size):
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value %= 20201227
    return value


def calculate_loop_size(subject_number, key):
    value = 1
    loops = 0
    while value != key:
        value *= subject_number
        value %= 20201227
        loops += 1
    return loops

loop_size_one = calculate_loop_size(7, key1)
loop_size_two = calculate_loop_size(7, key2)

encryption_key_one = transform(key2, loop_size_one)
encryption_key_two = transform(key1, loop_size_two)

print(f"Encryption keys are {encryption_key_one} and {encryption_key_two}.")

# part 2

print(".oO( done )")
