# --- Day 22: Monkey Map ---
#
# The monkeys take you on a surprisingly easy trail through the jungle. They're
# even going in roughly the right direction according to your handheld device's
# Grove Positioning System.
#
# As you walk, the monkeys explain that the grove is protected by a force field.
# To pass through the force field, you have to enter a password; doing so
# involves tracing a specific path on a strangely-shaped board.
#
# At least, you're pretty sure that's what you have to do; the elephants aren't
# exactly fluent in monkey.
#
# The monkeys give you notes that they took when they last saw the password
# entered (your puzzle input).
#
# For example:
#
#         ...#
#         .#..
#         #...
#         ....
# ...#.......#
# ........#...
# ..#....#....
# ..........#.
#         ...#....
#         .....#..
#         .#......
#         ......#.
#
# 10R5L5R10L4R5L5
#
# The first half of the monkeys' notes is a map of the board. It is comprised of
# a set of open tiles (on which you can move, drawn .) and solid walls (tiles
# which you cannot enter, drawn #).
#
# The second half is a description of the path you must follow. It consists of
# alternating numbers and letters:
#
# A number indicates the number of tiles to move in the direction you are
# facing. If you run into a wall, you stop moving forward and continue with the
# next instruction.
#
# A letter indicates whether to turn 90 degrees clockwise (R) or
# counterclockwise (L). Turning happens in-place; it does not change your
# current tile.
#
# So, a path like 10R5 means "go forward 10 tiles, then turn clockwise 90
# degrees, then go forward 5 tiles".
#
# You begin the path in the leftmost open tile of the top row of tiles.
# Initially, you are facing to the right (from the perspective of how the map is
# drawn).
#
# If a movement instruction would take you off of the map, you wrap around to
# the other side of the board. In other words, if your next tile is off of the
# board, you should instead look in the direction opposite of your current
# facing as far as you can until you find the opposite edge of the board, then
# reappear there.
#
# For example, if you are at A and facing to the right, the tile in front of you
# is marked B; if you are at C and facing down, the tile in front of you is
# marked D:
#
#         ...#
#         .#..
#         #...
#         ....
# ...#.D.....#
# ........#...
# B.#....#...A
# .....C....#.
#         ...#....
#         .....#..
#         .#......
#         ......#.
#
# It is possible for the next tile (after wrapping around) to be a wall; this
# still counts as there being a wall in front of you, and so movement stops
# before you actually wrap to the other side of the board.
#
# By drawing the last facing you had with an arrow on each tile you visit, the
# full path taken by the above example looks like this:
#
#         >>v#    
#         .#v.    
#         #.v.    
#         ..v.    
# ...#...v..v#    
# >>>v...>#.>>    
# ..#v...#....    
# ...>>>>v..#.    
#         ...#....
#         .....#..
#         .#......
#         ......#.
#
# To finish providing the password to this strange input device, you need to
# determine numbers for your final row, column, and facing as your final
# position appears from the perspective of the original map. Rows start from 1
# at the top and count downward; columns start from 1 at the left and count
# rightward. (In the above example, row 1, column 1 refers to the empty space
# with no tile on it in the top-left corner.) Facing is 0 for right (>), 1 for
# down (v), 2 for left (<), and 3 for up (^). The final password is the sum of
# 1000 times the row, 4 times the column, and the facing.
#
# In the above example, the final row is 6, the final column is 8, and the final
# facing is 0. So, the final password is 1000 * 6 + 4 * 8 + 0: 6032.
#
# Follow the path given in the monkeys' notes. What is the final password?
#
# As you reach the force field, you think you hear some Elves in the distance.
# Perhaps they've already arrived?
#
# You approach the strange input device, but it isn't quite what the monkeys
# drew in their notes. Instead, you are met with a large cube; each of its six
# faces is a square of 50x50 tiles.
#
# To be fair, the monkeys' map does have six 50x50 regions on it. If you were to
# carefully fold the map, you should be able to shape it into a cube!
#
# In the example above, the six (smaller, 4x4) faces of the cube are:
#
#         1111
#         1111
#         1111
#         1111
# 222233334444
# 222233334444
# 222233334444
# 222233334444
#         55556666
#         55556666
#         55556666
#         55556666
#
# You still start in the same position and with the same facing as before, but
# the wrapping rules are different. Now, if you would walk off the board, you
# instead proceed around the cube. From the perspective of the map, this can
# look a little strange. In the above example, if you are at A and move to the
# right, you would arrive at B facing down; if you are at C and move down, you
# would arrive at D facing up:
#
#         ...#
#         .#..
#         #...
#         ....
# ...#.......#
# ........#..A
# ..#....#....
# .D........#.
#        # ...#..B.
#        # .....#..
#        # .#......
#        # ..C...#.
#
# Walls still block your path, even if they are on a different face of the cube.
# If you are at E facing up, your movement is blocked by the wall marked by the
# arrow:
#
#         ...#
#         .#..
#      -->#...
#         ....
# ...#..E....#
# ........#...
# ..#....#....
# ..........#.
#         ...#....
#         .....#..
#         .#......
#         ......#.
#
# Using the same method of drawing the last facing you had with an arrow on each
# tile you visit, the full path taken by the above example now looks like this:
#
#         >>v#    
#         .#v.    
#         #.v.    
#         ..v.    
# ...#..^...v#    
# .>>>>>^.#.>>    
# .^#....#....    
# .^........#.    
#         ...#..v.
#         .....#v.
#         .#v<<<<.
#         ..v...#.
#
# The final password is still calculated from your final position and facing
# from the perspective of the map. In this example, the final row is 5, the
# final column is 7, and the final facing is 3, so the final password is 1000
# * 5 + 4 * 7 + 3 = 5031.
#
# Fold the map into a cube, then follow the path given in the monkeys' notes.
# What is the final password?

import numpy as np


# with open('input22.txt') as fid01:

from pathlib import Path
INPUT = Path(__file__).parent.parent / "2022-22.txt"

with open(INPUT) as fid01:
  flines = [val for val in fid01.readlines()]

xmax = max([len(lval) for lval in flines])
mmap = np.zeros((len(flines)+2,xmax+2),dtype=int)

for k1 in range(len(flines)):
  lval = flines[k1]
  for k2 in range(len(lval)):
    if(lval[k2] == '.'):
      mmap[k1+1,k2+1] = 1
    if(lval[k2] == '#'):
      mmap[k1+1,k2+1] = 2

ilist = list()
iline = flines[-1].strip()
numq  = ''
for ichr in iline:
  if(ichr =='L' or ichr == 'R'):
    ilist.append(int(numq))
    ilist.append(ichr)
    numq = ''
  else:
    numq = numq + ichr
if(numq):
  ilist.append(int(numq))


cpos = [1,np.argwhere(mmap[1,:]==1)[0][0]]
ched = 0


def get_face(cur_pos):
  if(cpos[0]<=50):
    if(cpos[1]<=100):
      return 1
    else:
      return 2
  elif(cpos[0]<=100):
    return 3
  elif(cpos[0]<=150):
    if(cpos[1]<=50):
      return 4
    else:
      return 5
  else:
    return 6


ofdic = {1:[  0, 50],2:[  0,100],3:[ 50, 50],
         4:[100,  0],5:[100, 50],6:[150,  0]}

fmdic = {(1,0):(2,0),(1,1):(3,1),(1,2):(4,0),(1,3):(6,0),
         (2,0):(5,2),(2,1):(3,2),(2,2):(1,2),(2,3):(6,3),
         (3,0):(2,3),(3,1):(5,1),(3,2):(4,1),(3,3):(1,3),
         (4,0):(5,0),(4,1):(6,1),(4,2):(1,0),(4,3):(3,0),
         (5,0):(2,2),(5,1):(6,2),(5,2):(4,2),(5,3):(3,3),
         (6,0):(5,3),(6,1):(2,1),(6,2):(1,1),(6,3):(4,3)}


for istr in ilist:
  if(istr == 'R'):
    ched = (ched+1)%4
  elif(istr == 'L'):
    ched = (ched-1)%4
  else:
    dx = istr

    while(dx > 0):
      if(ched==0):
        mlin = mmap[cpos[0],:]
        spos = cpos[1]+1
        if(np.all(mlin[spos:(spos+dx)]==1)):
          cpos[1] = cpos[1]+dx
          dx = 0
        else:
          bpos    = np.argwhere(mlin[spos:(spos+dx)]!=1)[0][0]+spos
          btyp    = mlin[bpos]
          cpos[1] = bpos-1
          dx      = dx - (bpos-spos)

          if(btyp == 2):
            dx = 0
          else:
            cfac = get_face(cpos)
            (ffac,fhed) = fmdic[(cfac,ched)]
            rcord = (cpos[0]-1)%50+1
            xyoff = ofdic[ffac]
            if(fhed==0):
              fcrd = [rcord,  1]
            elif(fhed==1):
              fcrd = [ 1, rcord]
            elif(fhed==2):
              fcrd = [51-rcord,50]
            else:
              fcrd = [50, rcord]
            fcrd = [fcrd[0]+xyoff[0],fcrd[1]+xyoff[1]]
            if(mmap[fcrd[0],fcrd[1]] == 1):
              dx = dx - 1
              cpos = fcrd
              cfac = ffac
              ched = fhed
            elif(mmap[fcrd[0],fcrd[1]] == 2):
              dx = 0
            else:
              1/0

      elif(ched==1):
        mlin = mmap[:,cpos[1]]
        spos = cpos[0]+1
        if(np.all(mlin[spos:(spos+dx)]==1)):
          cpos[0] = cpos[0]+dx
          dx = 0
        else:
          bpos    = np.argwhere(mlin[spos:(spos+dx)]!=1)[0][0]+spos
          btyp    = mlin[bpos]
          cpos[0] = bpos-1
          dx      = dx - (bpos-spos)

          if(btyp == 2):
            dx = 0
          else:
            cfac = get_face(cpos)
            (ffac,fhed) = fmdic[(cfac,ched)]
            rcord = (cpos[1]-1)%50+1
            xyoff = ofdic[ffac]
            if(fhed==0):
              fcrd = [rcord,  1]
            elif(fhed==1):
              fcrd = [ 1, rcord]
            elif(fhed==2):
              fcrd = [rcord, 50]
            else:
              fcrd = [50, 51-rcord]
            fcrd = [fcrd[0]+xyoff[0],fcrd[1]+xyoff[1]]
            if(mmap[fcrd[0],fcrd[1]] == 1):
              dx = dx - 1
              cpos = fcrd
              cfac = ffac
              ched = fhed
            elif(mmap[fcrd[0],fcrd[1]] == 2):
              dx = 0
            else:
              1/0

      elif(ched==2):
        mlin = mmap[cpos[0],:]
        spos = cpos[1]
        mpos = max(spos-dx,0)
        if(np.all(mlin[mpos:spos]==1)):
          cpos[1] = cpos[1]-dx
          dx = 0
        else:
          bpos    = np.argwhere(mlin[mpos:spos]!=1)[-1][0]+mpos
          btyp    = mlin[bpos]
          cpos[1] = bpos+1
          dx      = dx - (spos-bpos) + 1

          if(btyp == 2):
            dx = 0
          else:
            cfac = get_face(cpos)
            (ffac,fhed) = fmdic[(cfac,ched)]
            rcord = (cpos[0]-1)%50+1
            xyoff = ofdic[ffac]
            if(fhed==0):
              fcrd = [51-rcord, 1]
            elif(fhed==1):
              fcrd = [ 1, rcord]
            elif(fhed==2):
              fcrd = [rcord, 50]
            else:
              fcrd = [50, rcord]
            fcrd = [fcrd[0]+xyoff[0],fcrd[1]+xyoff[1]]
            if(mmap[fcrd[0],fcrd[1]] == 1):
              dx = dx - 1
              cpos = fcrd
              cfac = ffac
              ched = fhed
            elif(mmap[fcrd[0],fcrd[1]] == 2):
              dx = 0
            else:
              1/0

      elif(ched==3):
        mlin = mmap[:,cpos[1]]
        spos = cpos[0]
        mpos = max(spos-dx,0)
        if(np.all(mlin[mpos:spos]==1)):
          cpos[0] = cpos[0]-dx
          dx = 0
        else:
          bpos    = np.argwhere(mlin[mpos:spos]!=1)[-1][0]+mpos
          btyp    = mlin[bpos]
          cpos[0] = bpos+1
          dx      = dx - (spos-bpos) + 1

          if(btyp == 2):
            dx = 0
          else:
            cfac = get_face(cpos)
            (ffac,fhed) = fmdic[(cfac,ched)]
            rcord = (cpos[1]-1)%50+1
            xyoff = ofdic[ffac]
            if(fhed==0):
              fcrd = [rcord,  1]
            elif(fhed==1):
              fcrd = [ 1, 51-rcord]
            elif(fhed==2):
              fcrd = [rcord, 50]
            else:
              fcrd = [50, rcord]
            fcrd = [fcrd[0]+xyoff[0],fcrd[1]+xyoff[1]]

            if(mmap[fcrd[0],fcrd[1]] == 1):
              dx = dx - 1
              cpos = fcrd
              cfac = ffac
              ched = fhed
            elif(mmap[fcrd[0],fcrd[1]] == 2):
              dx = 0
            else:
              1/0

print()
print(cpos, ched, 1000*cpos[0]+4*cpos[1]+ched)


#for lval in mmap:
#  print((''.join([str(val) for val in lval.tolist()])).replace('0',' ').replace('1','.').replace('2','#'))
