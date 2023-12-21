# Advent of Code CLI

https://github.com/tobias-walle/advent-of-code-cli

```sh
cargo install --git https://github.com/tobias-walle/advent-of-code-cli
```

## Rust and Cargo

```sh
curl https://sh.rustup.rs -sSf | sh
```

## Example

```sh
# You can get the session from the cookies of https://adventofcode.com
# It has a relatively long lifetime so you can set it in your .bashrc and co
export AOC_SESSION="<your-session>"
mkdir ./template # Feel free to add your code boilerplate in this folder
aoc new -y 2023 -d 9 # This will create the "day_9" folder and downloads the problem into it
# After you solved the problem
cd day_9
aoc submit -l 1
# Download the second problem
aoc download
# Submit it
aoc submit -l 2
```

```sh
export AOC_SESSION="53616c7465645f5faadf4926fa3f0e116ee0c1aac9dfa1712ab9cce5d14cd104fe864f9f1a20ef9e2137233a07ef40d411a07aef46873d5e21d6e94f98cbac72"
cd 2023
# This will create the "day_22" folder and download the problem into it
aoc new -y 2023 -d 22
```