from typing import List

from app.encounters.encounter_difficulty import Difficulty


class EncounterBuilder:
    def __init__(self, party: List[int], difficulty: Difficulty):
        self.party: List[int] = party
        self.difficulty: Difficulty = difficulty

    def run(self):
        return []
