from app.domain.models.monster import Monster, MonsterStats
from app.repositories.cr_repo import MONSTER_STATISTICS_BY_CHALLENGE_RATING, CRColumn
from app.utils.math import inverse_lerp, lerp


def _lookup_cr_row(cr: float) -> dict:
    row = MONSTER_STATISTICS_BY_CHALLENGE_RATING[
        MONSTER_STATISTICS_BY_CHALLENGE_RATING[CRColumn.CR] == cr
    ]
    return {col: int(val) for col, val in row.iloc[0].items()}


def _scale_offset(value: int, source_expected: int, target_expected: int) -> int:
    offset = value - source_expected
    return max(1, target_expected + offset)


def _scale_range(
    value: int, source_min: int, source_max: int, target_min: int, target_max: int
) -> int:
    t = inverse_lerp(value, source_min, source_max)
    return max(1, int(lerp(t, target_min, target_max)))


def scale_monster(monster: Monster, target_cr: float) -> Monster:
    source = _lookup_cr_row(monster.cr)
    target = _lookup_cr_row(target_cr)

    return Monster(
        stats=MonsterStats(
            challenge_rating=target_cr,
            armor_class=_scale_offset(monster.ac, source[CRColumn.AC], target[CRColumn.AC]),
            hit_points=_scale_range(
                monster.hp,
                source[CRColumn.HP_MIN],
                source[CRColumn.HP_MAX],
                target[CRColumn.HP_MIN],
                target[CRColumn.HP_MAX],
            ),
            attack_bonus=_scale_offset(
                monster.atk_bonus, source[CRColumn.ATK], target[CRColumn.ATK]
            ),
            damage=_scale_range(
                monster.damage,
                source[CRColumn.DMG_MIN],
                source[CRColumn.DMG_MAX],
                target[CRColumn.DMG_MIN],
                target[CRColumn.DMG_MAX],
            ),
            save_dc=_scale_offset(monster.save_dc, source[CRColumn.SAVE], target[CRColumn.SAVE]),
        )
    )
