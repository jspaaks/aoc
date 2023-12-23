"""
https://adventofcode.com/2023/day/6
"""
import pytest


def get_data():
    ret = []
    testdata = [
        ("example.txt", 71503),
        ("input.txt", 28973936),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p2.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


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


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
