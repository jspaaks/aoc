import pytest


def get_data():
    txt = "\n".join([
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ])
    expected = sum([48, 12, 1560, 630, 36])
    return [
        pytest.param((txt, expected), id="example")
    ]


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


def main():
    with open("input.txt", "rt") as fid:
        txt = fid.read()
    print(solve(txt))


@pytest.mark.parametrize("data", get_data())
def test(data):
    txt, expected = data
    assert solve(txt) == expected


if __name__ == "__main__":
    main()
