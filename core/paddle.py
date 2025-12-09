# core/paddle.py
# РАЗРАБОТЧИК #2: Архитектура и игровой цикл
# Ответственность: логика платформы (паддла)

from config import *


class Paddle:
    """
    Класс платформы (паддла) для отскока шара.
    Управляется клавишами влево и вправо.
    """

    def __init__(self):
        """Инициализация платформы"""
        self.x = (WINDOW_WIDTH - PADDLE_WIDTH) // 2
        self.y = PADDLE_Y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED

    def move_left(self):
        """Переместить платформу влево"""
        self.x = max(0, self.x - self.speed)

    def move_right(self):
        """Переместить платформу вправо"""
        self.x = min(WINDOW_WIDTH - self.width, self.x + self.speed)

    def reset(self):
        """Вернуть платформу в центр"""
        self.x = (WINDOW_WIDTH - PADDLE_WIDTH) // 2

    def get_rect(self):
        """
        Получить pygame.Rect для коллизий
        
        Returns:
            pygame.Rect
        """
        import pygame
        return pygame.Rect(self.x, self.y, self.width, self.height)
