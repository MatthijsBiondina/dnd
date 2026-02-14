import pytest

from app.domain.models.monster import Monster, MonsterStats, MonsterStatsValidationException


def make_monster(**overrides) -> Monster:
    defaults = dict(
        challenge_rating=1,
        armor_class=13,
        hit_points=75,
        attack_bonus=4,
        damage=10,
        save_dc=13,
    )
    return Monster(stats=MonsterStats(**(defaults | overrides)))


class TestMonsterCRLookup:
    def test_cr(self):
        assert make_monster().cr == 1

    def test_xp(self):
        assert make_monster().xp == 200

    def test_proficiency_bonus(self):
        assert make_monster().proficiency_bonus == 2

    def test_invalid_cr_raises(self):
        with pytest.raises(MonsterStatsValidationException):
            make_monster(challenge_rating=999)


class TestMonsterValidation:
    @pytest.mark.parametrize(
        "field", ["armor_class", "hit_points", "attack_bonus", "damage", "save_dc"]
    )
    def test_zero_raises(self, field):
        with pytest.raises(MonsterStatsValidationException):
            make_monster(**{field: 0})

    @pytest.mark.parametrize(
        "field", ["armor_class", "hit_points", "attack_bonus", "damage", "save_dc"]
    )
    def test_negative_raises(self, field):
        with pytest.raises(MonsterStatsValidationException):
            make_monster(**{field: -1})

    @pytest.mark.parametrize("field", ["armor_class", "hit_points", "attack_bonus", "damage"])
    def test_non_int_raises(self, field):
        with pytest.raises(MonsterStatsValidationException):
            make_monster(**{field: 3.5})

    def test_save_dc_none_is_valid(self):
        monster = make_monster(save_dc=None)
        assert monster.save_dc is None
