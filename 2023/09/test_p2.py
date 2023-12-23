"""
https://adventofcode.com/2023/day/9
"""
import pytest


def get_data():
    ret = []
    testdata = [
        ("example.txt", sum([-3, 0, 5])),
        ("input.txt", 975),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p2.py", name)
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
    diff.reverse()
    n = len(diff)
    pred = [0]
    for i in range(1, n):
        pred.append(diff[i][0] - pred[i - 1])
    pred.reverse()
    return pred[0]


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
