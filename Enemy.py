from abc import ABC, abstractmethod


class Enemy(ABC):
    _name = None
    _health = None
    _damage = None

    def __init__(self, name, health, damage):
        self._name = name
        self._health = health
        self._damage = damage

    def getName(self):
        return self._name

    def getHealth(self):
        return self._health

    @abstractmethod
    def takeDamage(self, damage):
        pass

    @abstractmethod
    def attack(self, player):
        pass

    def isAlive(self):
        return self._health > 0


from GameLogger import GameLogger


class BaseEnemyDecorator(Enemy):
    _wrapee: Enemy = None

    def __init__(self, wrapee: Enemy):
        self._wrapee = wrapee
        self._logger = GameLogger.get_instance()

    def getName(self):
        return self._wrapee.getName()

    def getHealth(self):
        return self._wrapee.getHealth()

    def isAlive(self):
        return self._wrapee.isAlive()

    def takeDamage(self, damage):
        self._wrapee.takeDamage(damage)

    def attack(self, player):
        self._wrapee.attack(player)


class LegendaryEnemyDecorator(BaseEnemyDecorator):
    ADDITIONAL_DAMAGE = 20

    def __init__(self, wrapee: Enemy):
        super().__init__(wrapee)

    def getName(self):
        return f"Легендарный {super().getName()}"

    def attack(self, player):
        super().attack(player)
        self._logger.log("Враг легендарный и наносит дополнительный урон!!!")
        player.takeDamage(self.ADDITIONAL_DAMAGE)


class WindfuryEnemyDecorator(BaseEnemyDecorator):
    def __init__(self, wrapee):
        super().__init__(wrapee)

    def getName(self):
        return f"Обладающий Неистовством Ветра {super().getName()}"

    def attack(self, player):
        super().attack(player)
        self._logger.log("Неистовство ветра позволяет врагу атаковать второй раз!!!")
        super().attack(player)