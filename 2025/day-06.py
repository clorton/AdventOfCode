from pathlib import Path

import numpy as np

HERE = Path(__file__).parent

with Path(HERE / "day-06.txt").open("rt") as file:
    lines = [line.strip("\n") for line in file.readlines()]

values = [list(map(int, line.split())) for line in lines[:-1]]
ops = lines[-1].split()

values = np.array(values, np.int32)
ops = np.array(ops)

some = values.sum(axis=0)
prod = values.prod(axis=0)

total = some[ops == "+"].sum()
total += prod[ops == "*"].sum()

print(f"Part I: {total=}")

##### Part II #####

"""
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  

Reading the problems right-to-left one column at a time, the problems are now quite different:

- The rightmost problem is 4 + 431 + 623 = 1058
- The second problem from the right is 175 * 581 * 32 = 3253600
- The third problem from the right is 8 + 248 + 369 = 625
- Finally, the leftmost problem is 356 * 24 * 1 = 8544

Now, the grand total is 1058 + 3253600 + 625 + 8544 = 3263827.

1  *
24  
356 
    
369+
248 
8   
    
 32*
581 
175 
    
623+
431 
  4 
"""

data = [list(line) for line in lines[:-1]]
data = np.array(data).T

nums = ["".join(data[row,:]).strip() for row in range(data.shape[0])]
nums = [int(s) if s else -1 for s in nums]
nums = np.array(nums)
seps = np.nonzero(nums == -1)[0]

total = 0
for iop, (start, stop) in enumerate(zip([-1] + list(seps), list(seps) + [len(nums)])):
    total += nums[start+1:stop].sum() if ops[iop] == "+" else nums[start+1:stop].prod()

print(f"Part II: {total=}")

print("done")
