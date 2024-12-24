class PlayerProfile:
    def __init__(self, name: str, score: int):
        self.name = name
        self.score = score

    def get_name(self):
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_score(self):
        return self.score

    def set_score(self, score: int):
        self.score = score

    def serialize(self) -> bytes:
        return pickle.dumps(self)

    @staticmethod
    def deserialize(data: bytes) -> 'PlayerProfile':
        return pickle.loads(data)


from abc import ABC, abstractmethod


class PlayerProfileRepository(ABC):
    @abstractmethod
    def get_profile(self, name: str):
        pass

    @abstractmethod
    def update_high_score(self, name, score):
        pass


import os
import pickle
from pathlib import Path
from PlayerProfile import PlayerProfile


class PlayerProfileDBRepository(PlayerProfileRepository):
    SCORE_FILENAME = Path("score.txt")

    def __init__(self):
        try:
            if not self.SCORE_FILENAME.exists():
                self.SCORE_FILENAME.touch()
                self._update({})
        except OSError as e:
            raise RuntimeError(f"Ошибка при создании файла: {e}")

    def _read_file(self):
        try:
            with open(self.SCORE_FILENAME, 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, pickle.PickleError):
            return {}

    def _update(self, player_profile_map):
        try:
            with open(self.SCORE_FILENAME, 'wb') as file:
                pickle.dump(player_profile_map, file)
        except OSError as e:
            raise RuntimeError(f"Ошибка при записи в файл: {e}")

    def get_profile(self, name):
        print("Из базы данных достается информация о профилях игроков..")
        player_profile_map = self._read_file()
        if name not in player_profile_map:
            print("В базе данных создается новый профиль...")
            player_profile_map[name] = PlayerProfile(name, 0)
            self._update(player_profile_map)
        return player_profile_map[name]

    def update_high_score(self, name, score):
        print("В базе данных обновляются очки игрока...")
        player_profile_map = self._read_file()
        if name not in player_profile_map:
            print("В базе данных создается новый профиль...")
            player_profile_map[name] = PlayerProfile(name, 0)
        player_profile_map[name].set_score(score)
        self._update(player_profile_map)


class PlayerProfileCacheRepository(PlayerProfileRepository):
    def __init__(self):
        self._cached_profiles = {}
        self._database = PlayerProfileDBRepository()

    def get_profile(self, name):
        if name not in self._cached_profiles:
            print("Профиль игрока не найден в кеше...")
            player_profile_from_database = self._database.get_profile(name)
            self._cached_profiles[name] = player_profile_from_database
        print("Профиль игрока достается из кеша...")
        return self._cached_profiles[name]

    def update_high_score(self, name, score):
        if name not in self._cached_profiles:
            print("Профиль игрока не найден в кеше...")
            self._database.update_high_score(name, score)
            player_profile_from_database = self._database.get_profile(name)
            self._cached_profiles[name] = player_profile_from_database
            return
        cached_profile = self._cached_profiles[name]
        cached_profile.set_score(score)
        self._database.update_high_score(name, score)