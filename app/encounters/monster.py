from fractions import Fraction
from typing import Dict, Protocol, Union

CR_TO_XP: Dict[Union[Fraction, int], int] = {
    0: 10,
    Fraction(1, 8): 25,
    Fraction(1, 4): 50,
    Fraction(1, 2): 100,
    1: 200,
    2: 450,
    3: 700,
    4: 1100,
    5: 1800,
    6: 2300,
    7: 2900,
    8: 3900,
    9: 5000,
    10: 5900,
    11: 7200,
    12: 8400,
    13: 10_000,
    14: 11_500,
    15: 13_000,
    16: 15_000,
    17: 18_000,
    18: 20_000,
    19: 22_000,
    20: 25_000,
    21: 33_000,
    22: 41_000,
    23: 50_000,
    24: 62_000,
    25: 75_000,
    26: 90_000,
    27: 105_000,
    28: 120_000,
    29: 135_000,
    30: 155_000,
}


class Monster:
    def __init__(self, cr: float):
        self.cr: float = cr
        self.xp: int = CR_TO_XP[self.cr]
