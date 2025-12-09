from core.brick import BrickGroup
from config import *

class Level:
    """
    Класс для управления уровнями игры.
    Отвечает за прогрессию, усложнение, переход между уровнями.
    """

    def __init__(self, level_number=1):
        """
        Инициализация уровня
        
        Args:
            level_number: номер уровня (начиная с 1)
        """
        self.level_number = level_number
        self.bricks = BrickGroup()
        self.score = 0
        self.lives = NUM_LIVES
        self.speed_multiplier = LEVEL_SPEED_INCREMENT ** (level_number - 1)

    def generate(self):
        """Генерировать кирпичи для текущего уровня"""
        # Усложняем с каждым уровнем
        rows = BRICK_ROWS
        cols = BRICK_COLS
        
        # На более высоких уровнях больше кирпичей
        if self.level_number > 1:
            cols = min(BRICK_COLS + (self.level_number - 1), 12)
        
        self.bricks.generate_level(rows, cols)

    def add_score(self, points):
        """
        Добавить очки за разрушенный кирпич
        
        Args:
            points: количество очков
        """
        self.score += points * self.level_number  # На высоких уровнях больше очков

    def on_brick_destroyed(self):
        """Вызвать при разрушении кирпича"""
        self.add_score(10)

    def on_ball_lost(self):
        """Вызвать при потере шара"""
        self.lives -= 1
        return self.lives > 0  # Возвращает True если жизни остались

    def is_complete(self):
        """
        Проверить, завершён ли уровень (все кирпичи разрушены)
        
        Returns:
            True если уровень пройден
        """
        return self.bricks.is_level_complete()

    def next_level(self):
        """
        Создать следующий уровень
        
        Returns:
            новый объект Level
        """
        return Level(self.level_number + 1)

    def reset_lives(self):
        """Восстановить жизни"""
        self.lives = NUM_LIVES
