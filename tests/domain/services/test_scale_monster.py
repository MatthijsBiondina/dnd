from app.domain.models.monster import Monster, MonsterStats
from app.domain.services.scale_monster import scale_monster


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


def test_scaling_to_same_cr_returns_identical_stats():
    monster = make_monster()
    scaled = scale_monster(monster, target_cr=1)
    assert scaled.cr == monster.cr
    assert scaled.ac == monster.ac
    assert scaled.hp == monster.hp
    assert scaled.atk_bonus == monster.atk_bonus
    assert scaled.damage == monster.damage
    assert scaled.save_dc == monster.save_dc


def test_scaling_to_higher_cr_increases_xp():
    monster = make_monster()
    scaled = scale_monster(monster, target_cr=2)
    assert scaled.xp == 450


def test_scaling_to_lower_cr_decreases_xp():
    monster = make_monster()
    scaled = scale_monster(monster, target_cr=0.5)
    assert scaled.xp == 100


def test_scaling_to_higher_cr_increases_proficiency_bonus():
    monster = make_monster(challenge_rating=1)
    scaled = scale_monster(monster, target_cr=5)
    assert scaled.proficiency_bonus == 3


def test_scaling_to_lower_cr_decreases_proficiency_bonus():
    monster = make_monster(challenge_rating=5)
    scaled = scale_monster(monster, target_cr=1)
    assert scaled.proficiency_bonus == 2


def test_scaling_preserves_relative_ac():
    # CR 1 expected AC is 13, monster has 15 (+2 above expected)
    # CR 5 expected AC is 15, so scaled should be 17 (+2 above expected)
    monster = make_monster(challenge_rating=1, armor_class=15)
    scaled = scale_monster(monster, target_cr=5)
    assert scaled.ac == 17


def test_scaling_ac_floors_at_one():
    # CR 5 expected AC is 15, monster has AC 1 (-14 below expected)
    # CR 1 expected AC is 13, so scaled would be -1, should floor at 1
    monster = make_monster(challenge_rating=5, armor_class=1)
    scaled = scale_monster(monster, target_cr=1)
    assert scaled.ac == 1


def test_scaling_preserves_relative_attack_bonus():
    # CR 1 expected atk is +3, monster has +5 (+2 above)
    # CR 5 expected atk is +6, so scaled should be +8
    monster = make_monster(challenge_rating=1, attack_bonus=5)
    scaled = scale_monster(monster, target_cr=5)
    assert scaled.atk_bonus == 8


def test_scaling_attack_bonus_floors_at_one():
    monster = make_monster(challenge_rating=5, attack_bonus=1)
    scaled = scale_monster(monster, target_cr=1)
    assert scaled.atk_bonus == 1


def test_scaling_preserves_relative_save_dc():
    # CR 1 expected save is 13, monster has 15 (+2 above)
    # CR 5 expected save is 15, so scaled should be 17
    monster = make_monster(challenge_rating=1, save_dc=15)
    scaled = scale_monster(monster, target_cr=5)
    assert scaled.save_dc == 17


def test_scaling_save_dc_floors_at_one():
    monster = make_monster(challenge_rating=5, save_dc=1)
    scaled = scale_monster(monster, target_cr=1)
    assert scaled.save_dc == 1


def test_scaling_preserves_relative_hp():
    # CR 1 range: 71-85, monster has 78 (50% through range)
    # CR 5 range: 131-145, 50% through = 138
    monster = make_monster(challenge_rating=1, hit_points=78)
    scaled = scale_monster(monster, target_cr=5)
    assert scaled.hp == 138


def test_scaling_hp_above_range_preserved():
    # CR 1 range: 71-85, monster has 90 (above range)
    # CR 5 range: 131-145, same percentage = 150
    monster = make_monster(challenge_rating=1, hit_points=90)
    scaled = scale_monster(monster, target_cr=5)
    assert scaled.hp == 150


def test_scaling_hp_floors_at_one():
    monster = make_monster(challenge_rating=5, hit_points=1)
    scaled = scale_monster(monster, target_cr=1)
    assert scaled.hp == 1


def test_scaling_preserves_relative_damage():
    # CR 1 range: 9-14, monster has 11 (40% through range)
    # CR 5 range: 33-38, 40% through = 35
    monster = make_monster(challenge_rating=1, damage=11)
    scaled = scale_monster(monster, target_cr=5)
    assert scaled.damage == 35


def test_scaling_damage_floors_at_one():
    monster = make_monster(challenge_rating=5, damage=1)
    scaled = scale_monster(monster, target_cr=1)
    assert scaled.damage == 1
