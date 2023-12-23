"""
https://adventofcode.com/2023/day/2
"""
import pytest


def get_data():
    ret = []
    testdata = [
        ("example.txt", 8),
        ("input.txt", 2278),
    ]
    for name, expected in testdata:
        fname = __file__.replace("test_p1.py", name)
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

    max_red = 12
    max_green = 13
    max_blue = 14

    impossible_red = {i for i, red in reds if red > max_red}
    impossible_green = {i for i, green in greens if green > max_green}
    impossible_blue = {i for i, blue in blues if blue > max_blue}

    ok = {i for i, _ in games} - impossible_red - impossible_green - impossible_blue
    return sum(ok)


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected
