"""
https://adventofcode.com/2023/day/6
"""
import os
from pathlib import Path
from functools import reduce
from operator import mul


def read_sibling_file(name):
    d = os.path.dirname(os.path.realpath(__file__))
    f = Path(d, name)
    with open(f, "rt") as fid:
        return fid.read()


def main():
    txt = read_sibling_file("input.txt")
    print(solve(txt))


def get_duration(lines):
    s = lines[0].split(":")[1]
    return int("".join([d for d in s.split()]))


def get_record(lines):
    s = lines[1].split(":")[1]
    return int("".join([d for d in s.split()]))


def calc_distances(duration):
    # n is milliseconds to hold down the charge button before moving
    # charge rate is 1 millimeter per second more for each millisecond charging
    distances = [n * 1 * (duration - n) for n in range(duration + 1)]
    return distances


def solve(txt):
    lines = txt.splitlines()
    duration = get_duration(lines)
    record = get_record(lines)
    nways = len([dist for dist in calc_distances(duration) if dist > record])
    return nways


def test():
    txt = read_sibling_file("example.txt")
    expected = 71503
    assert solve(txt) == expected


if __name__ == "__main__":
    main()
