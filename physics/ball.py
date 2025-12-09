import math
from config import *

class Ball:
    """
    Класс для управления шаром в игре.
    Отвечает за:
    - Движение шара
    - Столкновения со стенами
    - Столкновения с платформой
    - Столкновения с кирпичами
    - Скорость и ускорение
    """

    def __init__(self, x, y, speed=BALL_SPEED):
        """
        Инициализация шара
        
        Args:
            x: начальная позиция X
            y: начальная позиция Y
            speed: начальная скорость шара
        """
        self.x = x
        self.y = y
        self.radius = BALL_SIZE // 2
        self.speed = speed
        
        # Направление движения (углы в радианах)
        # Начинаем с угла 45 градусов вверх-вправо
        self.angle = math.radians(45)
        
        # Скорость по осям
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -math.sin(self.angle) * self.speed  # минус, т.к. Y увеличивается вниз
        
        self.is_active = False  # Движется ли шар (или прилипнут к платформе)

    def update(self):
        """Обновить позицию шара"""
        if self.is_active:
            self.x += self.dx
            self.y += self.dy
            
            # Проверка столкновения со стенами (левая и правая)
            if self.x - self.radius <= 0:
                self.x = self.radius
                self.dx = abs(self.dx)  # Отскок вправо
            elif self.x + self.radius >= WINDOW_WIDTH:
                self.x = WINDOW_WIDTH - self.radius
                self.dx = -abs(self.dx)  # Отскок влево
            
            # Проверка столкновения с верхней стеной
            if self.y - self.radius <= 0:
                self.y = self.radius
                self.dy = abs(self.dy)  # Отскок вниз

    def attach_to_paddle(self, paddle_x, paddle_width):
        """
        Прилепить шар к платформе (начало игры)
        
        Args:
            paddle_x: X-позиция платформы
            paddle_width: ширина платформы
        """
        self.is_active = False
        self.x = paddle_x + paddle_width // 2
        self.y = PADDLE_Y - 10

    def launch(self):
        """Запустить шар с платформы"""
        if not self.is_active:
            self.is_active = True
            # Пересчитаем скорость по компонентам при запуске
            self.dx = math.cos(self.angle) * self.speed
            self.dy = -math.sin(self.angle) * self.speed

    def check_paddle_collision(self, paddle_rect):
        """Проверить столкновение с платформой"""
        if not self.is_active:
            return False
        
        ball_rect = self._get_rect()
        
        if ball_rect.colliderect(paddle_rect):
            # Отскок вверх
            self.y = paddle_rect.top - self.radius
            self.dy = -abs(self.dy)
            
            # Угол отскока зависит от позиции удара
            # -1.0 (левый край) до +1.0 (правый край)
            relative_intersect = (self.x - paddle_rect.centerx) / (paddle_rect.width / 2)
            relative_intersect = max(-1, min(1, relative_intersect))
            
            # Угол от -60° до +60°
            max_angle = math.pi / 3  # 60 градусов
            bounce_angle = relative_intersect * max_angle
            
            # Пересчитываем скорость
            self.dx = self.speed * math.sin(bounce_angle)
            self.dy = -self.speed * math.cos(bounce_angle)  # Отрицательное = вверх
            
            return True
        
        return False


    def check_brick_collision(self, brick_rect):
        """
        Проверить столкновение с кирпичом
        
        Args:
            brick_rect: pygame.Rect объекта кирпича
            
        Returns:
            Кортеж (столкновение произошло, сторона столкновения)
            Сторона: 'top', 'bottom', 'left', 'right'
        """
        if not self.is_active:
            return False, None
        
        ball_rect = self._get_rect()
        
        if not ball_rect.colliderect(brick_rect):
            return False, None
        
        # Определяем, с какой стороны кирпича произошло столкновение
        # Проверяем расстояние до каждой стороны
        
        distances = {
            'top': abs(self.y - brick_rect.bottom),
            'bottom': abs(self.y - brick_rect.top),
            'left': abs(self.x - brick_rect.right),
            'right': abs(self.x - brick_rect.left),
        }
        
        side = min(distances, key=distances.get)
        
        # Отскок в зависимости от стороны столкновения
        if side == 'top' or side == 'bottom':
            self.dy = -self.dy
            if side == 'top':
                self.y = brick_rect.bottom + self.radius
            else:
                self.y = brick_rect.top - self.radius
        else:  # left or right
            self.dx = -self.dx
            if side == 'left':
                self.x = brick_rect.right + self.radius
            else:
                self.x = brick_rect.left - self.radius
        
        return True, side

    def is_out_of_bounds(self):
        """
        Проверить, вышел ли шар за нижнюю границу (проигрыш)
        
        Returns:
            True если шар упал вниз
        """
        return self.y > WINDOW_HEIGHT

    def increase_speed(self, factor=1.1):
        """
        Увеличить скорость шара
        
        Args:
            factor: множитель увеличения скорости
        """
        self.speed = min(self.speed * factor, BALL_MAX_SPEED)
        magnitude = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if magnitude > 0:
            self.dx = (self.dx / magnitude) * self.speed
            self.dy = (self.dy / magnitude) * self.speed

    def _get_rect(self):
        """
        Получить pygame.Rect объекта для коллизий
        
        Returns:
            pygame.Rect
        """
        import pygame
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def reset(self, paddle_x, paddle_width):
        """Сбросить шар в начальное состояние"""
        self.attach_to_paddle(paddle_x, paddle_width)
        self.speed = BALL_SPEED
        self.angle = math.radians(45)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -math.sin(self.angle) * self.speed
