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


def look_up(table, selection_value):
    result = table[-1][1]
    for row in table:
        score, entry = row
        if selection_value <= score:
            result = entry
            break
    return result
