from GameLogger import GameLogger
from Enemy import Enemy
import random
class WeaponToEnemyAdapter(Enemy):
    _DISPEL_PROBABILITY = 0.2
    def __init__(self, weapon):
        self._logger = GameLogger.get_instance()
        self._name = "Магическое оружие"
        self._health = 50
        self._weapon = weapon
    def takeDamage(self, damage):
        self._logger.log(f"{self._name} получает {damage} урона!")
        self._health -= damage
        dispel_roll = random.random()
        if dispel_roll <= self._DISPEL_PROBABILITY:
            self._logger.log("Атака рассеяла заклятие с оружия!")
            self._health = 0
        if self._health > 0:
            self._logger.log(f"У {self._name} осталось {self._health} здоровья")
    def attack(self, player):
        self._logger.log(f"{self._name} атакует {player._name}!")
        player.takeDamage(self._weapon.getDamage())
from CharacterClass import CharacterClass
from PlayableCharacter import MagicalEquipmentChest
from PlayableCharacter import WarriorEquipmentChest
from PlayableCharacter import ThiefEquipmentChest
class WeaponEquipmentFacade:
    def __init__(self, character_class):
        if character_class == CharacterClass.MAGE:
            self.equipment_chest = MagicalEquipmentChest()
        elif character_class == CharacterClass.WARRIOR:
            self.equipment_chest = WarriorEquipmentChest()
        elif character_class == CharacterClass.THIEF:
            self.equipment_chest = ThiefEquipmentChest()
        else:
            raise ValueError("Неизвестный класс персонажа")
    def getWeapon(self):
        return self.equipment_chest.getWeapon()