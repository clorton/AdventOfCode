from pathlib import Path

from tqdm import tqdm

HERE = Path(__file__).parent

with Path(HERE / "day-02.txt").open("rt") as file:
    ranges = [tuple(map(int, range.split("-"))) for range in file.readline().strip().split(",")]

parti = True
partii = True

if parti:
    total = 0
    for i, (start, end) in enumerate(ranges):
        # brute force
        for id in tqdm(range(start, end+1), desc=f"{i+1}/{len(ranges)}"):
            sid = str(id)
            if (l := len(sid)) % 2 == 0:
                front = sid[:l//2]
                back = sid[l//2:]
                if back == front:
                    total += id

    print(f"Part I: {total=}")

##### Part II #####

"""
- 11-22 still has two invalid IDs, 11 and 22.
- 95-115 now has two invalid IDs, 99 and 111.
- 998-1012 now has two invalid IDs, 999 and 1010.
- 1188511880-1188511890 still has one invalid ID, 1188511885.
- 222220-222224 still has one invalid ID, 222222.
- 1698522-1698528 still contains no invalid IDs.
- 446443-446449 still has one invalid ID, 446446.
- 38593856-38593862 still has one invalid ID, 38593859.
- 565653-565659 now has one invalid ID, 565656.
- 824824821-824824827 now has one invalid ID, 824824824.
- 2121212118-2121212124 now has one invalid ID, 2121212121.

Adding up all the invalid IDs in this example produces 4174379265.
"""

test = [
    (11,22),
    (95,115),
    (998,1012),
    (1188511880,1188511890),
    (222220,222224),
    (1698522,1698528),
    (446443,446449),
    (38593856,38593862),
    (565653,565659),
    (824824821,824824827),
    (2121212118,2121212124)
]

if partii:
    # ranges = test

    total = 0
    for i, (start, end) in enumerate(ranges):
        # brute force
        for id in tqdm(range(start, end+1), desc=f"{i+1}/{len(ranges)}"):
            sid = str(id)
            for length in range(1, (len(sid) // 2) + 1):
                pattern = sid[:length]
                remainder = sid[length:]
                compare = "".join([pattern] * (len(remainder) // len(pattern)))

                if compare == remainder:
                    total += id
                    break

    print(f"Part II: {total=}")

print("done")
