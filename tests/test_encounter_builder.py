from fractions import Fraction
from typing import Any, List

import pytest
from app.encounters.encounter_builder import EncounterBuilder
from app.encounters.encounter_difficulty import Difficulty
from app.encounters.monster import Monster


def test_empty_party_gives_empty_encounter():
    builder = EncounterBuilder(party=[], difficulty=Difficulty.EASY)
    encounters = builder.run()
    assert len(encounters) == 0


def lists_equal_length(list1: List[Any], list2: List[Any]) -> bool:
    return len(list1) == len(list2)


def lists_equal(list1: List[Any], list2: List[Any]) -> bool:
    return lists_equal_length(list1, list2) and all(
        e1 == e2 for e1, e2 in zip(list1, list2)
    )


def test_party_of_one_lvl_one():
    builder = EncounterBuilder(party=[1], difficulty=Difficulty.EASY)
    encounters = builder.run()
    isinstance(encounters, List)


@pytest.mark.parametrize(
    "cr,xp",
    [
        (Fraction(1, 8), 25),
        (Fraction(1, 4), 50),
        (Fraction(1, 2), 100),
        (1, 200),
        (2, 450),
    ],
)
def test_cr_maps_to_xp(cr, xp):
    assert Monster(cr=cr).xp == xp
