from dataclasses import dataclass

from app.repositories.cr_repo import MONSTER_STATISTICS_BY_CHALLENGE_RATING, CRColumn


@dataclass
class MonsterStats:
    challenge_rating: float
    armor_class: int
    hit_points: int
    attack_bonus: int
    damage: int
    save_dc: int | None


class Monster:
    def __init__(self, stats: MonsterStats):
        self.cr, self.xp, self.proficiency_bonus = self._lookup_cr_stats(stats.challenge_rating)
        self.ac = self._ensure_positive_int(stats.armor_class, "Armor class")
        self.hp = self._ensure_positive_int(stats.hit_points, "Hit points")
        self.atk_bonus = self._ensure_positive_int(stats.attack_bonus, "Attack bonus")
        self.damage = self._ensure_positive_int(stats.damage, "Damage")
        self.save_dc = self._ensure_optional_positive_int(stats.save_dc, "Save DC")

    def _lookup_cr_stats(self, challenge_rating: float) -> tuple[float, int, int]:
        row = MONSTER_STATISTICS_BY_CHALLENGE_RATING[
            MONSTER_STATISTICS_BY_CHALLENGE_RATING[CRColumn.CR] == challenge_rating
        ]
        if row.empty:
            raise MonsterStatsValidationException(f"Invalid challenge rating: {challenge_rating}")
        r = row.iloc[0]
        return challenge_rating, int(r[CRColumn.XP]), int(r[CRColumn.PROF_BONUS])

    def _ensure_positive_int(self, value: int, name: str) -> int:
        if type(value) is not int:
            raise MonsterStatsValidationException(f"{name} must be an integer, got {type(value)}")
        if value <= 0:
            raise MonsterStatsValidationException(f"{name} must be greater than 0, got {value}")
        return value

    def _ensure_optional_positive_int(self, value: int | None, name: str) -> int | None:
        if value is None:
            return None
        return self._ensure_positive_int(value, name)


class MonsterStatsValidationException(Exception):
    pass
