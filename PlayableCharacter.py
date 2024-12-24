from abc import ABC, abstractmethod
import random
from enum import Enum
from GameLogger import GameLogger
from CharacterClass import CharacterClass
from Weapon import Weapon
from Armor import Armor
from Enemy import Enemy


class PlayableCharacter:
    def __init__(self, builder):
        self._logger = GameLogger.get_instance()
        self._name = builder._name
        self._character_class = builder._character_class
        self._weapon = builder._weapon
        self._armor = builder._armor
        self._health = self._character_class.getStartingHealth

    class Builder:
        def __init__(self):
            self._name = None
            self._character_class = None
            self._weapon = None
            self._armor = None

        def setName(self, name):
            self._name = name
            return self

        def setCharacterClass(self, characterClass):
            self._character_class = characterClass
            return self

        def setWeapon(self, weapon):
            self._weapon = weapon
            return self

        def setArmor(self, armor):
            self._armor = armor
            return self

        def build(self):
            return PlayableCharacter(self)

    def takeDamage(self, damage):
        reducedDamage = round(damage * (1 - self._armor.getDefense()))
        if reducedDamage < 0:
            reducedDamage = 0
        self._health -= reducedDamage
        self._armor.use()
        self._logger.log(f"{self._name} получил урон: {reducedDamage}")
        if self._health > 0:
            self._logger.log(f"У {self._name} осталось {self._health} здоровья")

    def attack(self, enemy):
        self._logger.log(f"{self._name} атакует врага {enemy.getName()}")
        self._weapon.use()
        enemy.takeDamage(self._weapon.getDamage())

    def is_alive(self):
        return self._health > 0

    def getName(self):
        return self._name


class Sword(Weapon):
    def __init__(self):
        self._damage = 20
        self._logger = GameLogger.get_instance()

    def getDamage(self):
        return self._damage

    def use(self):
        self._logger.log("Удар мечом!")


class Bow(Weapon):
    def __init__(self):
        self._damage = 15
        self._criticalChance = 0.3
        self._cricitalModifier = 2
        self._logger = GameLogger.get_instance()

    def getDamage(self):
        if random.random() <= self._criticalChance:
            self._logger.log("Критический урон!")
            return self._damage * self._cricitalModifier
        return self._damage

    def use(self):
        self._logger.log("Выстрел из лука!")


class Staff(Weapon):
    def __init__(self):
        self._damage = 25
        self._scatter = 0.2
        self._logger = GameLogger.get_instance()

    def getDamage(self):
        factor = 1 + (random.random() * 2 * self._scatter - self._scatter)
        return round(self._damage * factor)

    def use(self):
        self._logger.log("Воздух накаляется, из посоха вылетает огненный шар!")


class HeavyArmor(Armor):
    def __init__(self):
        self._defense = 0.3
        self._logger = GameLogger.get_instance()

    def getDefense(self):
        return self._defense

    def use(self):
        self._logger.log("Тяжелая броня блокирует значительную часть урона")


class LightArmor(Armor):
    def __init__(self):
        self._defense = 0.2
        self._logger = GameLogger.get_instance()

    def getDefense(self):
        return self._defense

    def use(self):
        self._logger.log("Легкая броня блокирует урон")


class Robe(Armor):
    def __init__(self):
        self._defense = 0.1
        self._logger = GameLogger.get_instance()

    def getDefense(self):
        return self._defense

    def use(self):
        self._logger.log("Роба блокирует немного урона")


class EquipmentChest(ABC):
    def getWeapon(self):
        pass

    def getArmor(self):
        pass


class WarriorEquipmentChest(EquipmentChest):
    def getWeapon(self):
        return Sword()

    def getArmor(self):
        return HeavyArmor()


class MagicalEquipmentChest(EquipmentChest):
    def getWeapon(self):
        return Staff()

    def getArmor(self):
        return Robe()


class ThiefEquipmentChest(EquipmentChest):
    def getWeapon(self):
        return Bow()

    def getArmor(self):
        return LightArmor()


class Location(ABC):
    @abstractmethod
    def spawnEnemy(self):
        pass


class Goblin(Enemy):
    def __init__(self):
        super().__init__("Гоблин", 50, 10)
        self._logger = GameLogger.get_instance()

    def takeDamage(self, _damage):
        self._logger.log(f"{self._name} получает {_damage} урона!")
        self._health -= _damage
        if self._health > 0:
            self._logger.log(f"У {self._name} осталось {self._health} здоровья")

    def attack(self, player):
        self._logger.log(f"{self._name} атакует {player._name}!")
        player.takeDamage(self._damage)


from Enemy import Enemy


class Dragon(Enemy):
    def __init__(self):
        super().__init__("Дракон", 100, 30)
        self._resistance = 0.2
        self._gameLogger = GameLogger.get_instance()

    def takeDamage(self, _damage):
        _damage = round(_damage * (1 - self._resistance))
        self._gameLogger.log(f"{self._name} получает {_damage} урона!")
        self._health -= _damage
        if self._health > 0:
            self._gameLogger.log(f"У {self._name} осталось {self._health} здоровья")

    def attack(self, player):
        self._gameLogger.log("Дракон дышит огнем!")
        player.takeDamage(self._damage)


class Forest(Location):
    def spawnEnemy(self):
        return Goblin()


class DragonBarrow(Location):
    def spawnEnemy(self):
        return Dragon()