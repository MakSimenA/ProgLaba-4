from enum import Enum
class CharacterClass(Enum):
    WARRIOR = (100)
    THIEF = (90)
    MAGE = (80)
    def __init__(self, starting_health):
        self.starting_health = starting_health
    @property
    def getStartingHealth(self):
        return self.starting_health