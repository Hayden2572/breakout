# core/brick.py
# РАЗРАБОТЧИК #2: Архитектура и игровой цикл
# Ответственность: логика кирпичей

from config import *


class Brick:
    """
    Класс одного кирпича в игре.
    Кирпич может быть разрушен при столкновении с шаром.
    """

    def __init__(self, x, y, width=BRICK_WIDTH, height=BRICK_HEIGHT):
        """
        Инициализация кирпича
        
        Args:
            x: позиция X
            y: позиция Y
            width: ширина кирпича
            height: высота кирпича
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_destroyed = False
        
        # Цвет кирпича (можно сделать случайным или от уровня)
        self.color = COLOR_BLUE

    def get_rect(self):
        """
        Получить pygame.Rect для коллизий
        
        Returns:
            pygame.Rect
        """
        import pygame
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def destroy(self):
        """Разрушить кирпич"""
        self.is_destroyed = True

    def set_color(self, color):
        """
        Установить цвет кирпича
        
        Args:
            color: кортеж (R, G, B)
        """
        self.color = color


class BrickGroup:
    """
    Группа кирпичей (уровень).
    Управляет созданием и проверкой состояния всех кирпичей.
    """

    def __init__(self):
        """Инициализация группы кирпичей"""
        self.bricks = []

    def generate_level(self, rows=BRICK_ROWS, cols=BRICK_COLS):
        """
        Генерировать уровень с кирпичами
        
        Args:
            rows: количество рядов кирпичей
            cols: количество столбцов кирпичей
        """
        self.bricks = []
        
        # Расчёт начальной позиции (центрируем сетку кирпичей)
        total_width = cols * BRICK_WIDTH + (cols - 1) * BRICK_SPACING
        start_x = (WINDOW_WIDTH - total_width) // 2
        start_y = 30
        
        colors = [COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_CYAN, COLOR_MAGENTA]
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (BRICK_WIDTH + BRICK_SPACING)
                y = start_y + row * (BRICK_HEIGHT + BRICK_SPACING)
                
                brick = Brick(x, y)
                # Цвет зависит от ряда
                brick.set_color(colors[row % len(colors)])
                self.bricks.append(brick)

    def remove_destroyed(self):
        """Удалить разрушенные кирпичи из списка"""
        self.bricks = [brick for brick in self.bricks if not brick.is_destroyed]

    def get_active_bricks(self):
        """
        Получить список активных (неразрушенных) кирпичей
        
        Returns:
            list of Brick
        """
        return [brick for brick in self.bricks if not brick.is_destroyed]

    def is_level_complete(self):
        """
        Проверить, завершён ли уровень (все кирпичи разрушены)
        
        Returns:
            True если все кирпичи разрушены
        """
        return len(self.get_active_bricks()) == 0

    def reset(self):
        """Сбросить уровень (все кирпичи восстановлены)"""
        for brick in self.bricks:
            brick.is_destroyed = False
