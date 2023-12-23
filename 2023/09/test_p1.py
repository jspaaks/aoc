"""
https://adventofcode.com/2023/day/9
"""
import pytest


def get_data():
    ret = []
    testdata = [
        ("example.txt", sum([18, 28, 68])),
        ("input.txt", 1641934234),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p1.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def calc_diffs(history):
    diffs = []
    diff = history
    for _ in range(len(history) - 1):
        diffs.append(diff)
        if set(diff) == {0}:
            break
        diff = [b - a for b, a in zip(diff[1:], diff[0:-1])]
    return diffs


def read_histories(lines):
    return [[int(elem) for elem in line.split()] for line in lines]


def predict(diff):
    return sum([elem[-1] for elem in diff])


def solve(txt):
    lines = txt.splitlines()
    histories = read_histories(lines)
    diffs = [calc_diffs(h) for h in histories]
    predictions = [predict(d) for d in diffs]
    return sum(predictions)


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
