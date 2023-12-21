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


def get_durations(lines):
    durations = lines[0].split(":")[1]
    return [int(d) for d in durations.split()]


def get_records(lines):
    records = lines[1].split(":")[1]
    return [int(d) for d in records.split()]


def calc_distances(duration):
    # n is milliseconds to hold down the charge button before moving
    # charge rate is 1 millimeter per second more for each millisecond charging
    distances = [n * 1 * (duration - n) for n in range(duration + 1)]
    return distances


def solve(txt):
    lines = txt.splitlines()
    durations = get_durations(lines)
    records = get_records(lines)
    nways = [len([dist for dist in calc_distances(dur) if dist > rec]) for dur, rec in zip(durations, records)]
    return reduce(mul, nways)


def test():
    txt = read_sibling_file("example.txt")
    expected = reduce(mul, [4, 8, 9])
    assert solve(txt) == expected


if __name__ == "__main__":
    main()
