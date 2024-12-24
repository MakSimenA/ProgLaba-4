from GameLogger import GameLogger
from PlayableCharacter import Location, DragonBarrow, Forest
from CharacterClass import CharacterClass
from PlayableCharacter import PlayableCharacter
from PlayableCharacter import MagicalEquipmentChest, WarriorEquipmentChest, ThiefEquipmentChest
from Enemy import BaseEnemyDecorator, LegendaryEnemyDecorator, WindfuryEnemyDecorator
from PlayerProfile import PlayerProfileCacheRepository
from WeaponToEnemy import WeaponEquipmentFacade, WeaponToEnemyAdapter
import random

class HauntedManor(Location):
    def __init__(self):
        random_class = random.choice(list(CharacterClass))
        self.weapon_equipment_facade = WeaponEquipmentFacade(random_class)  # weapon_equipment_facade это композиция

    def spawnEnemy(self):
        weapon = self.weapon_equipment_facade.getWeapon()
        enchanted_weapon = WeaponToEnemyAdapter(weapon)
        return enchanted_weapon


def get_chest(character_class):
    if character_class == CharacterClass.MAGE:
        return MagicalEquipmentChest()
    elif character_class == CharacterClass.WARRIOR:
        return WarriorEquipmentChest()
    elif character_class == CharacterClass.THIEF:
        return ThiefEquipmentChest()
    else:
        raise ValueError("Неизвестный класс персонажа")


def get_location(location_name):
    if location_name.lower() == "мистический лес":
        return Forest()
    elif location_name.lower() == "проклятый особняк":
        return HauntedManor()
    elif location_name.lower() == "логово дракона":
        return DragonBarrow()
    else:
        raise ValueError("Неверная локация")


def add_enemy_modifiers(enemy):
    decorator = BaseEnemyDecorator(enemy)
    second_modifier_probability = 0.3
    second_modifier_proc = random.random() <= second_modifier_probability
    if random.random() < 0.5:
        decorator = LegendaryEnemyDecorator(decorator)
        if second_modifier_proc:
            decorator = WindfuryEnemyDecorator(decorator)
    else:
        decorator = WindfuryEnemyDecorator(decorator)
        if second_modifier_proc:
            decorator = LegendaryEnemyDecorator(decorator)
    return decorator


def get_score(location_name, strong_enemy):
    base_score = 0
    if location_name.lower() == "мистический лес":
        base_score = 10
    elif location_name.lower() == "проклятый особняк":
        base_score = 50
    elif location_name.lower() == "логово дракона":
        base_score = 100
    else:
        raise ValueError("Неверная локация")
    if strong_enemy:
        return base_score * 2
    return base_score


repository = PlayerProfileCacheRepository()
print("Создайте своего персонажа: ")
print("Введите имя: ")
name = input()
playerProfile = repository.get_profile(name)
print(f"Текущий счет игрока {playerProfile.get_name()}: {playerProfile.get_score()}")
character_class = CharacterClass[input("Выберите класс из списка: " + str([cls.name for cls in CharacterClass]) + ' ')]
starting_equipment_chest = get_chest(character_class)
starting_armor = starting_equipment_chest.getArmor()
starting_weapon = starting_equipment_chest.getWeapon()
player = PlayableCharacter.Builder().setName(name).setCharacterClass(character_class).setWeapon(
    starting_weapon).setArmor(starting_armor).build()
game_logger = GameLogger.get_instance()
game_logger.log(f"{player.getName()} очнулся на распутье!")
location_name = input("Куда вы двинетесь? выберите локацию: (мистический лес, проклятый особняк, логово дракона) ")
location = get_location(location_name)
game_logger.log(f"{player.getName()} отправился в {location_name}")
enemy = location.spawnEnemy()
strong_enemy_curse = random.random() < 0.5
if strong_enemy_curse:
    game_logger.log(f"Боги особенно немилостивы к {name}, сегодня его ждет страшная битва...")
    enemy = add_enemy_modifiers(enemy)
game_logger.log(f"у {player.getName()} на пути возникает {enemy.getName()}, начинается бой!")
random = random.Random()
while player.is_alive() and enemy.isAlive():
    print("Введите что-нибудь чтобы атаковать!")
    input()
    player.attack(enemy)
    stunned = random.choice([True, False])
    if stunned:
        game_logger.log(f"{enemy.getName()} был оглушен атакой {player.getName()}!")
        continue
    enemy.attack(player)
print()
if not player.is_alive():
    game_logger.log(f"{player.getName()} был убит...")
    repository.update_high_score(name, 0)
    player_profile = repository.get_profile(name)
    print(f"Новый счет игрока {player_profile.get_name()}: {player_profile.get_score()}")
game_logger.log(f"Злой {enemy.getName()} был побежден! {player.getName()} отправился дальше по тропе судьбы...")
score = get_score(location_name, strong_enemy_curse)
repository.update_high_score(name, score)
player_profile = repository.get_profile(name)
print(f"Новый счет игрока {player_profile.get_name()}: {player_profile.get_score()}")