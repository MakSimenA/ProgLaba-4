from abc import ABC, abstractmethod
class Weapon(ABC):
    def getDamage(self):
        pass
    def use(self):
        pass