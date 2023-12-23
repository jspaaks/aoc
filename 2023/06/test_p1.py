"""
https://adventofcode.com/2023/day/6
"""
from functools import reduce
from operator import mul
import pytest


def get_data():
    ret = []
    testdata = [
        ("example.txt", reduce(mul, [4, 8, 9])),
        ("input.txt", 4568778),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p1.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


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


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
