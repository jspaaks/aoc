"""
https://adventofcode.com/2023/day/8
"""
import math
import re
import pytest


def get_data():
    ret = []
    testdata = [
        ("example3.txt", 6),
        ("input.txt", 12_927_600_769_609),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p2_2.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def get_choices(lines):
    choices = [{"L": 0, "R": 1}[elem] for elem in list(lines[0])]
    return choices, len(choices)


def get_nodes(lines):
    tuples = [re.match(r'([12A-Z]+) = \(([12A-Z]+), ([12A-Z]+)\).*', line).groups() for line in lines[2:]]
    starts = {t[0] for t in tuples if t[0][-1] == "A"}
    return starts, {t[0]: (t[1], t[2]) for t in tuples}


def solve(txt):
    lines = txt.splitlines()
    choices, nchoices = get_choices(lines)
    starts, nodes = get_nodes(lines)
    periods = []
    for name in starts:
        ifollow = 0
        while name[-1] != "Z":
            choice = choices[ifollow % nchoices]
            name = nodes[name][choice]
            ifollow += 1
        periods.append(ifollow)
    return math.lcm(*periods)  # not sure why this approach yields a correct answer


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
