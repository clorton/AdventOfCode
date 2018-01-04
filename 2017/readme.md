## Advent of Code 2017

Day One: [Inverse Captcha](http://adventofcode.com/2017/day/1)
- ...find the sum of all digits that match the next digit in the list.
- ...instead of considering the next digit, it wants you to consider the digit halfway around the circular list.

Day Two: [Corruption Checksum](http://adventofcode.com/2017/day/2)
- For each row, determine the difference between the largest value and the smallest value; the checksum is the sum of all of these differences.
- ...the goal is to find the only two numbers in each row where one evenly divides the other - that is, where the result of the division operation is a whole number. They would like you to find those numbers on each line, divide them, and add up each line's result.

Day Three: [Spiral Memory](http://adventofcode.com/2017/day/3)
- Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while spiraling outward. ...requested data must be carried back to square 1 by programs that can only move up, down, left, or right. They always take the shortest path: the Manhattan Distance between the location of the data and square 1.
- As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1. Then, in the same allocation order as shown above, they store the sum of the values in all adjacent squares, including diagonals.

Day Four: [High-Entropy Passphrases](http://adventofcode.com/2017/day/4)
- A passphrase consists of a series of words (lowercase letters) separated by spaces. To ensure security, a valid passphrase must contain no duplicate words.
- Now, a valid passphrase must contain no two words that are anagrams of each other...

Day Five: [A Maze of Twisty Trampolines, All Alike](http://adventofcode.com/2017/day/5)
- An urgent interrupt arrives from the CPU: it's trapped in a maze of jump instructions, and it would like assistance from any programs with spare cycles to help find the exit.
- Now, the jumps are even stranger: after each jump, if the offset was three or more, instead decrease it by 1. Otherwise, increase it by 1 as before.

Day Six: [Memory Reallocation](http://adventofcode.com/2017/day/6)
- In this area, there are sixteen memory banks; each memory bank can hold any number of blocks. The goal of the reallocation routine is to balance the blocks between the memory banks.
- Out of curiosity, the debugger would also like to know the size of the loop: starting from a state that has already been seen, how many block redistribution cycles must be performed before that same state is seen again?

Day Seven: [Recursive Circus](http://adventofcode.com/2017/day/7)
- Wandering further through the circuits of the computer, you come upon a tower of programs that have gotten themselves into a bit of trouble. A recursive algorithm has gotten out of hand, and now they're balanced precariously in a large tower.
- The programs explain the situation: they can't get down. Rather, they could get down, if they weren't expending all of their energy trying to keep the tower balanced. Apparently, one program has the wrong weight, and until it's fixed, they're stuck here.

Day Eight: [I Heard You Like Registers](http://adventofcode.com/2017/day/8)
- You receive a signal directly from the CPU. Because of your recent assistance with jump instructions, it would like you to compute the result of a series of unusual register instructions. Each instruction consists of several parts: the register to modify, whether to increase or decrease that register's value, the amount by which to increase or decrease it, and a condition. If the condition fails, skip the instruction without modifying the register. The registers all start at 0.
- To be safe, the CPU also needs to know the highest value held in any register during this process so that it can decide how much memory to allocate to these operations.

Day Nine: [Stream Processing](http://adventofcode.com/2017/day/9)
- A large stream blocks your path. According to the locals, it's not safe to cross the stream at the moment because it's full of garbage. You look down at the stream; rather than water, you discover that it's a stream of characters.
- Now, you're ready to remove the garbage. To prove you've removed it, you need to count all of the characters within the garbage.

Day Ten: [Knot Hash](http://adventofcode.com/2017/day/10)
- This hash function simulates tying a knot in a circle of string with 256 marks on it. Based on the input to be hashed, the function repeatedly selects a span of string, brings the ends together, and gives the span a half-twist to reverse the order of the marks within it. After doing this many times, the order of the marks is used to build the resulting hash.
- The logic you've constructed forms a single round of the Knot Hash algorithm; running the full thing requires many of these rounds.

Day Eleven: [Hex Ed](http://adventofcode.com/2017/day/11)
- You have the path the child process took. Starting where he started, you need to determine the fewest number of steps required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)
- How many steps away is the furthest he ever got from his starting position?

Day Twelve: [Digital Plumber](http://adventofcode.com/2017/day/12)
- Programs in this village communicate using a fixed system of pipes. Messages are passed between programs using these pipes, but most programs aren't connected to each other directly. Instead, programs pass messages between each other until the message reaches the intended recipient.
- There are more programs than just the ones in the group containing program ID 0. The rest of them have no way of reaching that group, and still might have no way of reaching each other.

Day Thirteen: [Packet Scanners](http://adventofcode.com/2017/day/13)
- You need to cross a vast firewall. The firewall consists of several layers, each with a security scanner that moves back and forth across the layer. To succeed, you must not be detected by a scanner.
- Now, you need to pass through the firewall without being caught - easier said than done.

Day Fourteen: [Disk Defragmentation](http://adventofcode.com/2017/day/14)
- The disk in question consists of a 128x128 grid; each square of the grid is either free or used. On this disk, the state of the grid is tracked by the bits in a sequence of knot hashes.
- Now, all the defragmenter needs to know is the number of regions. A region is a group of used squares that are all adjacent, not including diagonals. Every used square is in exactly one region: lone used squares form their own isolated regions, while several adjacent squares all count as a single region.

Day Fifteen: [Dueling Generators](http://adventofcode.com/2017/day/15)
- Here, you encounter a pair of dueling generators. The generators, called generator A and generator B, are trying to agree on a sequence of numbers. However, one of them is malfunctioning, and so the sequences don't always match.
- In the interest of trying to align a little better, the generators get more picky about the numbers they actually give to the judge.

Day Sixteen: [Permutation Promenade](http://adventofcode.com/2017/day/16)
- You come upon a very unusual sight; a group of programs here appear to be dancing.
- Keeping the positions they ended up in from their previous dance, the programs perform it again and again: including the first dance, a total of one billion (1000000000) times.

Day Seventeen: [Spinlock](http://adventofcode.com/2017/day/17)
- Suddenly, whirling in the distance, you notice what looks like a massive, pixelated hurricane: a deadly spinlock.
- The spinlock does not short-circuit. Instead, it gets more angry. At least, you assume that's what happened; it's spinning significantly faster than it was a moment ago.

Day Eighteen: [Duet](http://adventofcode.com/2017/day/18)
- You discover a tablet containing some strange assembly code labeled simply "Duet".
- As you congratulate yourself for a job well done, you notice that the documentation has been on the back of the tablet this entire time. While you actually got most of the instructions correct, there are a few key differences. This assembly code isn't about sound at all - it's meant to be run twice at the same time.

Day Nineteen: [A Series of Tubes](http://adventofcode.com/2017/day/19)
- Somehow, a network packet got lost and ended up here. It's trying to follow a routing diagram (your puzzle input), but it's confused about where to go.
- The packet is curious how many steps it needs to go.

Day Twenty: [Particle Swarm](http://adventofcode.com/2017/day/20)
- Suddenly, the GPU contacts you, asking for help. Someone has asked it to simulate too many particles, and it won't be able to finish them all in time to render the next frame at this rate.
- To simplify the problem further, the GPU would like to remove any particles that collide.

Day Twenty-One: [Fractal Art](http://adventofcode.com/2017/day/21)
- You find a program trying to generate some art. It uses a strange process that involves repeatedly enhancing the detail of an image through a set of rules.
- How many pixels stay on after 18 iterations?

Day Twenty-Two: [Sporifica Virus](http://adventofcode.com/2017/day/22)
- Diagnostics indicate that the local grid computing cluster has been contaminated with the Sporifica Virus. The grid computing cluster is a seemingly-infinite two-dimensional grid of compute nodes. Each node is either clean or infected by the virus.
- As you go to remove the virus from the infected nodes, it evolves to resist your attempt.

Day Twenty-Three: [Coprocessor Conflagration](http://adventofcode.com/2017/day/23)
- You decide to head directly to the CPU and fix the printer from there. As you get close, you find an experimental coprocessor doing so much work that the local programs are afraid it will halt and catch fire. This would cause serious issues for the rest of the computer, so you head in and see what you can do.
- Now, it's time to fix the problem. The debug mode switch is wired directly to register a. You flip the switch, which makes register a now start at 1 when the program is executed. Immediately, the coprocessor begins to overheat. Whoever wrote this program obviously didn't choose a very efficient implementation. You'll need to optimize the program if it has any hope of completing before Santa needs that printer working.

Day Twenty-Four: [Electromagnetic Moat](http://adventofcode.com/2017/day/24)
- The CPU itself is a large, black building surrounded by a bottomless pit. Enormous metal tubes extend outward from the side of the building at regular intervals and descend down into the void. There's no way to cross, but you need to get inside. No way, of course, other than building a bridge out of the magnetic components strewn about nearby.
- What is the strength of the longest bridge you can make? If you can make multiple bridges of the longest length, pick the strongest one.

Day Twenty-Five: [The Halting Problem](http://adventofcode.com/2017/day/25)
- "Programs these days, don't know their origins. That's the Turing machine! It's what makes the whole computer work." You try to explain that Turing machines are merely models of computation, but he cuts you off. "No, see, that's just what they want you to think. Ultimately, inside every CPU, there's a Turing machine driving the whole thing! Too bad this one's broken. We're doomed!"
- The Turing machine, and soon the entire computer, springs back to life. A console glows dimly nearby, awaiting your command.
