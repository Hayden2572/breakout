import pygame
from config import *


class Renderer:
    """
    Класс для отрисовки всех игровых объектов.
    Отвечает за визуализацию платформы, шара, кирпичей и меню.
    """

    def __init__(self, screen):
        """
        Инициализация рендера
        
        Args:
            screen: pygame.Surface главное окно
        """
        self.screen = screen
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

    def draw_paddle(self, paddle):
        """
        Отрисовать платформу
        
        Args:
            paddle: объект Paddle
        """
        rect = paddle.get_rect()
        pygame.draw.rect(self.screen, COLOR_WHITE, rect, border_radius=5)
        # Добавить градиент или эффект
        pygame.draw.rect(self.screen, COLOR_CYAN, rect, 2, border_radius=5)

    def draw_ball(self, ball):
        """
        Отрисовать шар
        
        Args:
            ball: объект Ball
        """
        pygame.draw.circle(self.screen, COLOR_YELLOW, (int(ball.x), int(ball.y)), ball.radius)
        # Добавить белый контур для эффекта
        pygame.draw.circle(self.screen, COLOR_WHITE, (int(ball.x), int(ball.y)), ball.radius, 1)

    def draw_bricks(self, bricks):
        """
        Отрисовать все кирпичи
        
        Args:
            bricks: список объектов Brick
        """
        for brick in bricks:
            if not brick.is_destroyed:
                rect = brick.get_rect()
                # Основной кирпич
                pygame.draw.rect(self.screen, brick.color, rect, border_radius=3)
                # Контур для глубины
                pygame.draw.rect(self.screen, COLOR_WHITE, rect, 1, border_radius=3)
                # Верхняя грань для 3D эффекта
                pygame.draw.line(
                    self.screen,
                    (min(brick.color[0] + 50, 255), 
                     min(brick.color[1] + 50, 255), 
                     min(brick.color[2] + 50, 255)),
                    (rect.left, rect.top),
                    (rect.right, rect.top),
                    2
                )

    def draw_menu(self):
        """Отрисовать экран меню"""
        # Может быть пустым или содержать простой фон
        self.screen.fill(COLOR_BLACK)
