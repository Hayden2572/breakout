import pygame
from config import *


class UIManager:
    """
    Менеджер пользовательского интерфейса.
    Отвечает за отрисовку меню, текстов, экранов победы/поражения.
    """

    def __init__(self):
        """Инициализация менеджера UI"""
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

    def draw_main_menu(self, screen):
        """
        Отрисовать главное меню
        
        Args:
            screen: pygame.Surface
        """
        # Заголовок
        title = self.font_large.render("BREAKOUT", True, COLOR_CYAN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Инструкция
        instruction = self.font_medium.render("Press SPACE to Start", True, COLOR_WHITE)
        instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(instruction, instruction_rect)
        
        # Контролы
        controls = self.font_small.render("LEFT/RIGHT arrows to move paddle", True, COLOR_GRAY)
        controls_rect = controls.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150))
        screen.blit(controls, controls_rect)

    def draw_game_ui(self, screen, level, score, lives):
        """
        Отрисовать игровой UI (уровень, счёт, жизни)
        
        Args:
            screen: pygame.Surface
            level: номер уровня
            score: текущий счёт
            lives: количество жизней
        """
        # Левый верхний угол: Уровень
        level_text = self.font_small.render(f"Level: {level}", True, COLOR_GREEN)
        screen.blit(level_text, (10, 10))
        
        # Центр вверху: Счёт
        score_text = self.font_small.render(f"Score: {score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 10))
        screen.blit(score_text, score_rect)
        
        # Правый верхний угол: Жизни
        lives_text = self.font_small.render(f"Lives: {lives}", True, COLOR_RED)
        lives_rect = lives_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
        screen.blit(lives_text, lives_rect)

    def draw_pause_screen(self, screen):
        """
        Отрисовать экран паузы
        
        Args:
            screen: pygame.Surface
        """
        # Полупрозрачное наложение
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLOR_BLACK)
        screen.blit(overlay, (0, 0))
        
        # Текст паузы
        pause_text = self.font_large.render("PAUSED", True, COLOR_YELLOW)
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(pause_text, pause_rect)
        
        # Инструкция
        resume_text = self.font_small.render("Press P to Resume", True, COLOR_WHITE)
        resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        screen.blit(resume_text, resume_rect)

    def draw_level_complete(self, screen, level):
        """
        Отрисовать экран завершения уровня
        
        Args:
            screen: pygame.Surface
            level: номер уровня
        """
        # Полупрозрачное наложение
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLOR_BLACK)
        screen.blit(overlay, (0, 0))
        
        # Текст завершения
        complete_text = self.font_large.render(f"LEVEL {level} COMPLETE!", True, COLOR_GREEN)
        complete_rect = complete_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        screen.blit(complete_text, complete_rect)
        
        # Инструкция
        next_text = self.font_small.render("Press SPACE for Next Level", True, COLOR_WHITE)
        next_rect = next_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        screen.blit(next_text, next_rect)

    def draw_game_over(self, screen, score):
        """
        Отрисовать экран Game Over
        
        Args:
            screen: pygame.Surface
            score: финальный счёт
        """
        # Полупрозрачное наложение
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLOR_BLACK)
        screen.blit(overlay, (0, 0))
        
        # Текст Game Over
        game_over_text = self.font_large.render("GAME OVER", True, COLOR_RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
        screen.blit(game_over_text, game_over_rect)
        
        # Счёт
        score_text = self.font_medium.render(f"Final Score: {score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(score_text, score_rect)
        
        # Инструкция
        retry_text = self.font_small.render("Press SPACE to Return to Menu", True, COLOR_WHITE)
        retry_rect = retry_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        screen.blit(retry_text, retry_rect)

    def draw_victory(self, screen, score):
        """
        Отрисовать экран победы
        
        Args:
            screen: pygame.Surface
            score: финальный счёт
        """
        # Полупрозрачное наложение
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLOR_BLACK)
        screen.blit(overlay, (0, 0))
        
        # Текст победы
        victory_text = self.font_large.render("YOU WIN!", True, COLOR_GREEN)
        victory_rect = victory_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
        screen.blit(victory_text, victory_rect)
        
        # Счёт
        score_text = self.font_medium.render(f"Final Score: {score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(score_text, score_rect)
        
        # Инструкция
        menu_text = self.font_small.render("Press SPACE to Return to Menu", True, COLOR_WHITE)
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        screen.blit(menu_text, menu_rect)
