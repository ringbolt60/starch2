# --------------------------------------------------
import itertools
import random

import pytest


class Dice:
    """Generator producing a stream of six sided dice rolls."""

    def __init__(self, seed: int | None = None, mocks=None):
        self.seed: int | None = seed
        if mocks:
            self.mocks = itertools.cycle(mocks)
        else:
            self.mocks = None  # type: ignore
        self.generator = random.Random(self.seed)

    def next(self):
        if self.mocks:
            return self.mocks.__next__()
        else:
            return self.generator.randint(1, 6)


# --------------------------------------------------
def test_dice():
    d6 = Dice()
    total = 0
    for _ in range(1000):
        roll = d6.next()
        assert 1 <= roll <= 6
        total += roll
    assert 1000 <= total <= 6000
    assert total / 1000 == pytest.approx(3.5, abs=0.5)

    d6_seeded = Dice(seed=1)
    expected = [2, 5, 1, 3, 1, 4, 4, 4, 6, 4]
    actual = []
    for _ in range(10):
        actual.append(d6_seeded.next())
    assert actual == expected

    d6_mock = Dice(mocks=[1, 2, 3])
    expected = [1, 2, 3, 1, 2, 3, 1]
    actual = []
    for _ in range(7):
        actual.append(d6_mock.next())
    assert actual == expected
