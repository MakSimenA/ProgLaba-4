class GameLogger:
    _instance = None
    def __init__(self, *args, **kwargs):
        raise RuntimeError("Нельзя создавать экземпляры напрямую. Используйте get_instance()")
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = super(GameLogger, cls).__new__(cls)
        return cls._instance
    def log(self, message):
        print(f"[GAME LOG]: {message}")