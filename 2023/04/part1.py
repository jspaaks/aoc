"""
https://adventofcode.com/2023/day/4
"""
import os
from pathlib import Path


def main():
    d = os.path.dirname(os.path.realpath(__file__))
    f = Path(d, "input.txt")
    with open(f, "rt") as fid:
        txt = fid.read()
    print(solve(txt))


def calc_score(line):
    numbers = line.split(":", maxsplit=1)[1]
    winning_str, have_str = numbers.split("|")
    winning = {int(elem) for elem in winning_str.split()}
    have = {int(elem) for elem in have_str.split()}
    overlap = len(winning.intersection(have))
    return 2**(overlap - 1) if overlap >= 1 else 0


def solve(txt):
    return sum([calc_score(line) for line in txt.splitlines()])


def test():
    txt = "".join([
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\n",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\n",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\n",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\n",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11\n",
    ])
    expected = sum([8, 2, 2, 1, 0, 0])
    assert solve(txt) == expected


if __name__ == "__main__":
    main()
