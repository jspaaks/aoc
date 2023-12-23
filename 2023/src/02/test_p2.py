"""
https://adventofcode.com/2023/day/2
"""
import pytest


def get_data():
    ret = []
    testdata = [
        ("example.txt", sum([48, 12, 1560, 630, 36])),
        ("input.txt", 67953),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p2.py", name)
        with open(fname, "rt") as fid:
            txt = fid.read()
        ret.append(pytest.param((txt, expected), id=name))
    return ret


def solve(txt):
    lines = txt.splitlines()
    games = [(i + 1, line.split(":")[1].strip()) for i, line in enumerate(lines)]
    gamesets = [(i, gameset.strip()) for i, game in games for gameset in game.split(";")]
    colors = [(i, color.strip()) for i, gameset in gamesets for color in gameset.split(",")]

    reds = [(i, int(color.replace("red", "").strip())) for i, color in colors if "red" in color]
    greens = [(i, int(color.replace("green", "").strip())) for i, color in colors if "green" in color]
    blues = [(i, int(color.replace("blue", "").strip())) for i, color in colors if "blue" in color]

    power = []
    for igame, _ in games:
        r = max([red for i, red in reds if i == igame])
        g = max([green for i, green in greens if i == igame])
        b = max([blue for i, blue in blues if i == igame])
        power.append(r * g * b)
    return sum(power)


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
