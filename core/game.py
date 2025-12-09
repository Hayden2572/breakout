import pygame
from core.paddle import Paddle
from core.level import Level
from physics.ball import Ball
from graphics.renderer import Renderer
from graphics.ui import UIManager
from audio.sound_manager import SoundManager
from config import *


class GameState:
    """Перечисление состояний игры"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    LEVEL_COMPLETE = "level_complete"
    GAME_OVER = "game_over"
    WIN = "win"


class Game:
    """
    Главный класс игры.
    Отвечает за:
    - Инициализацию игры
    - Главный игровой цикл
    - Управление состояниями
    - Обработку событий
    - Обновление логики игры
    """

    def __init__(self):
        """Инициализация игры"""
        pygame.init()
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Breakout Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Компоненты игры
        self.paddle = Paddle()
        self.ball = Ball(WINDOW_WIDTH // 2, PADDLE_Y - 10)
        self.level = Level(1)
        
        # Менеджеры
        self.renderer = Renderer(self.screen)
        self.ui_manager = UIManager()
        self.sound_manager = SoundManager()
        
        # Состояние игры
        self.state = GameState.MENU
        self.last_level_number = 0
        
        # Инициализация уровня
        self._init_level()

    def _init_level(self):
        """Инициализировать уровень"""
        self.level.generate()
        self.paddle.reset()
        self.ball.reset(self.paddle.x, self.paddle.width)
        self.sound_manager.play_level_start()

    def handle_events(self):
        """Обработать события (клавиатура, закрытие окна)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == GameState.MENU:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.PLAYING and not self.ball.is_active:
                        self.ball.launch()
                        self.sound_manager.play_ball_launch()
                    elif self.state == GameState.LEVEL_COMPLETE:
                        self.level = self.level.next_level()
                        self._init_level()
                        self.state = GameState.PLAYING
                    elif self.state == GameState.GAME_OVER or self.state == GameState.WIN:
                        self.__init__()
                        self.state = GameState.MENU
                
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                
                elif event.key == pygame.K_p and self.state == GameState.PLAYING:
                    self.state = GameState.PAUSED
                
                elif event.key == pygame.K_p and self.state == GameState.PAUSED:
                    self.state = GameState.PLAYING
        
        # Обработка постоянно нажатых клавиш
        if self.state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move_left()
            if keys[pygame.K_RIGHT]:
                self.paddle.move_right()

    def update(self):
        """Обновить логику игры"""
        if self.state != GameState.PLAYING:
            return
        
        # Обновить позицию шара
        self.ball.update()
        
        # Проверить столкновение с платформой
        self.ball.check_paddle_collision(self.paddle.get_rect())
        
        # Проверить столкновения с кирпичами
        for brick in self.level.bricks.get_active_bricks():
            collided, side = self.ball.check_brick_collision(brick.get_rect())
            if collided:
                brick.destroy()
                self.level.on_brick_destroyed()
                self.sound_manager.play_brick_hit()
                self.ball.increase_speed(1.01)
        
        # Удалить разрушенные кирпичи
        self.level.bricks.remove_destroyed()
        
        # Проверить, вышел ли шар за границы
        if self.ball.is_out_of_bounds():
            if not self.level.on_ball_lost():
                self.state = GameState.GAME_OVER
                self.sound_manager.play_game_over()
            else:
                self.ball.reset(self.paddle.x, self.paddle.width)
                self.sound_manager.play_ball_lost()
        
        # Проверить, завершён ли уровень
        if self.level.is_complete():
            self.state = GameState.LEVEL_COMPLETE
            if self.level.level_number == 5:  # Макс уровень
                self.state = GameState.WIN
                self.sound_manager.play_victory()
            else:
                self.sound_manager.play_level_complete()

    def render(self):
        """Отрисовать всё на экран"""
        self.screen.fill(COLOR_BLACK)
        
        # Отрисовка в зависимости от состояния
        if self.state == GameState.MENU:
            self.renderer.draw_menu()
            self.ui_manager.draw_main_menu(self.screen)
        
        elif self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            # Отрисовка игровых объектов
            self.renderer.draw_paddle(self.paddle)
            self.renderer.draw_ball(self.ball)
            self.renderer.draw_bricks(self.level.bricks.get_active_bricks())
            
            # Отрисовка UI
            self.ui_manager.draw_game_ui(
                self.screen,
                self.level.level_number,
                self.level.score,
                self.level.lives
            )
            
            if self.state == GameState.PAUSED:
                self.ui_manager.draw_pause_screen(self.screen)
        
        elif self.state == GameState.LEVEL_COMPLETE:
            self.renderer.draw_paddle(self.paddle)
            self.renderer.draw_ball(self.ball)
            self.renderer.draw_bricks(self.level.bricks.get_active_bricks())
            self.ui_manager.draw_level_complete(self.screen, self.level.level_number)
        
        elif self.state == GameState.GAME_OVER:
            self.ui_manager.draw_game_over(self.screen, self.level.score)
        
        elif self.state == GameState.WIN:
            self.ui_manager.draw_victory(self.screen, self.level.score)
        
        pygame.display.flip()

    def run(self):
        """Главный игровой цикл"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()


def main():
    """Точка входа в игру"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
