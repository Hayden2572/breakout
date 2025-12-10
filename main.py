"""
Обновленный модуль главной игры Breakout.

Содержит главный класс Game с поддержкой аргументов командной строки,
интеграцией с менеджером статистики и звуковыми эффектами.
"""

import pygame
import argparse
import time
from typing import Optional
from config import *
from core.stats_manager import StatsManager
from audio.sound_manager import SoundManager  # ← ДОБАВЛЕНО


class Paddle:
    """Класс платформы для отскока шара."""
    
    def __init__(self, speed_multiplier: float = 1.0):
        """
        Инициализация платформы.
        
        Args:
            speed_multiplier: Множитель скорости платформы.
        """
        self.x = (WINDOW_WIDTH - PADDLE_WIDTH) // 2
        self.y = PADDLE_Y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = int(PADDLE_SPEED * speed_multiplier)

    def move_left(self) -> None:
        """Переместить платформу влево."""
        self.x = max(0, self.x - self.speed)

    def move_right(self) -> None:
        """Переместить платформу вправо."""
        self.x = min(WINDOW_WIDTH - self.width, self.x + self.speed)

    def reset(self) -> None:
        """Вернуть платформу в центр."""
        self.x = (WINDOW_WIDTH - PADDLE_WIDTH) // 2

    def get_rect(self):
        """Получить pygame.Rect для коллизий."""
        import pygame
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Brick:
    """Класс одного кирпича в игре."""
    
    def __init__(self, x: int, y: int, width: int = BRICK_WIDTH, height: int = BRICK_HEIGHT):
        """
        Инициализация кирпича.
        
        Args:
            x: Позиция X.
            y: Позиция Y.
            width: Ширина кирпича.
            height: Высота кирпича.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_destroyed = False
        self.color = COLOR_BLUE

    def get_rect(self):
        """Получить pygame.Rect для коллизий."""
        import pygame
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def destroy(self) -> None:
        """Разрушить кирпич."""
        self.is_destroyed = True

    def set_color(self, color: tuple) -> None:
        """Установить цвет кирпича."""
        self.color = color


class BrickGroup:
    """Группа кирпичей уровня."""
    
    def __init__(self):
        """Инициализация группы кирпичей."""
        self.bricks = []

    def generate_level(self, rows: int = BRICK_ROWS, cols: int = BRICK_COLS) -> None:
        """Генерировать уровень с кирпичами."""
        self.bricks = []
        total_width = cols * BRICK_WIDTH + (cols - 1) * BRICK_SPACING
        start_x = (WINDOW_WIDTH - total_width) // 2
        start_y = 30
        
        colors = [COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_CYAN, COLOR_MAGENTA]
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (BRICK_WIDTH + BRICK_SPACING)
                y = start_y + row * (BRICK_HEIGHT + BRICK_SPACING)
                brick = Brick(x, y)
                brick.set_color(colors[row % len(colors)])
                self.bricks.append(brick)

    def get_active_bricks(self):
        """Получить список активных кирпичей."""
        return [brick for brick in self.bricks if not brick.is_destroyed]

    def is_level_complete(self) -> bool:
        """Проверить, завершён ли уровень."""
        return len(self.get_active_bricks()) == 0

    def remove_destroyed(self) -> None:
        """Удалить разрушенные кирпичи."""
        self.bricks = [brick for brick in self.bricks if not brick.is_destroyed]


class Ball:
    """Класс шара."""
    
    def __init__(self, x: float, y: float, speed_multiplier: float = 1.0, sound_manager=None):
        """
        Инициализация шара.
        
        Args:
            x: Начальная позиция X.
            y: Начальная позиция Y.
            speed_multiplier: Множитель скорости шара.
            sound_manager: Менеджер звуков.
        """
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = BALL_SIZE
        self.speed = BALL_SPEED * speed_multiplier
        self.max_speed = BALL_MAX_SPEED * speed_multiplier
        self.is_active = False
        self.sound_manager = sound_manager  # ← ДОБАВЛЕНО

    def launch(self) -> None:
        """Запустить шар."""
        import math
        angle = -60
        rad = math.radians(angle)
        self.vx = self.speed * math.cos(rad)
        self.vy = self.speed * math.sin(rad)
        self.is_active = True
        
        # Звук запуска
        if self.sound_manager:
            self.sound_manager.play_ball_launch()  # ← ДОБАВЛЕНО

    def update(self) -> None:
        """Обновить позицию шара."""
        self.x += self.vx
        self.y += self.vy
        
        # Отскок от стен
        if self.x - self.radius < 0 or self.x + self.radius > WINDOW_WIDTH:
            self.vx = -self.vx
            self.x = max(self.radius, min(WINDOW_WIDTH - self.radius, self.x))
            if self.sound_manager:
                self.sound_manager.play_wall_hit()  # ← ДОБАВЛЕНО

        if self.y - self.radius < 0:
            self.vy = -self.vy
            self.y = max(self.radius, self.y)
            if self.sound_manager:
                self.sound_manager.play_wall_hit()  # ← ДОБАВЛЕНО

    def is_out_of_bounds(self) -> bool:
        """Проверить, вышел ли шар за нижнюю границу."""
        return self.y > WINDOW_HEIGHT

    def reset(self, paddle_x: int, paddle_width: int) -> None:
        """Сбросить шар на платформу."""
        self.x = paddle_x + paddle_width // 2
        self.y = PADDLE_Y - 10
        self.vx = 0
        self.vy = 0
        self.is_active = False

    def check_paddle_collision(self, paddle_rect) -> bool:
        """Проверить столкновение с платформой."""
        import pygame
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                               self.radius * 2, self.radius * 2)
        
        if ball_rect.colliderect(paddle_rect):
            self.vy = -abs(self.vy)
            self.y = paddle_rect.top - self.radius
            
            # Изменить угол в зависимости от места попадания
            collision_point = (self.x - paddle_rect.left) / paddle_rect.width
            collision_point = max(0, min(1, collision_point))
            
            import math
            angle = (collision_point - 0.5) * 100
            self.vx = self.speed * math.sin(math.radians(angle))
            self.vy = -abs(self.vy)
            
            return True
        return False

    def check_brick_collision(self, brick_rect):
        """Проверить столкновение с кирпичом."""
        import pygame
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                               self.radius * 2, self.radius * 2)
        
        if ball_rect.colliderect(brick_rect):
            # Определить сторону коллизии
            if self.vy > 0:  # Снизу
                self.vy = -abs(self.vy)
                self.y = brick_rect.top - self.radius
                return True, "bottom"
            elif self.vy < 0:  # Сверху
                self.vy = abs(self.vy)
                self.y = brick_rect.bottom + self.radius
                return True, "top"
            elif self.vx > 0:  # Справа
                self.vx = -abs(self.vx)
                self.x = brick_rect.left - self.radius
                return True, "right"
            else:  # Слева
                self.vx = abs(self.vx)
                self.x = brick_rect.right + self.radius
                return True, "left"
        return False, None

    def increase_speed(self, factor: float) -> None:
        """Увеличить скорость шара."""
        speed = (self.vx**2 + self.vy**2) ** 0.5
        if speed < self.max_speed:
            new_speed = min(speed * factor, self.max_speed)
            if speed > 0:
                self.vx = self.vx / speed * new_speed
                self.vy = self.vy / speed * new_speed


class Level:
    """Класс для управления уровнями игры."""
    
    def __init__(self, level_number: int = 1, difficulty: str = "medium"):
        """
        Инициализация уровня.
        
        Args:
            level_number: Номер уровня.
            difficulty: Уровень сложности (easy, medium, hard).
        """
        self.level_number = level_number
        self.bricks = BrickGroup()
        self.score = 0
        self.difficulty = difficulty
        self.speed_multiplier = (LEVEL_SPEED_INCREMENT ** (level_number - 1)) * \
                                DIFFICULTY_MULTIPLIERS.get(difficulty, 1.0)
        
        lives = DIFFICULTY_LIVES.get(difficulty, NUM_LIVES)
        self.lives = lives

    def generate(self) -> None:
        """Генерировать кирпичи для текущего уровня."""
        rows = BRICK_ROWS
        cols = BRICK_COLS
        
        if self.level_number > 1:
            cols = min(BRICK_COLS + (self.level_number - 1), 12)
        
        self.bricks.generate_level(rows, cols)

    def add_score(self, points: int) -> None:
        """Добавить очки за разрушенный кирпич."""
        self.score += points * self.level_number

    def on_brick_destroyed(self) -> None:
        """Вызвать при разрушении кирпича."""
        self.add_score(10)

    def on_ball_lost(self) -> bool:
        """Вызвать при потере шара."""
        self.lives -= 1
        return self.lives > 0

    def is_complete(self) -> bool:
        """Проверить, завершён ли уровень."""
        return self.bricks.is_level_complete()

    def next_level(self):
        """Создать следующий уровень."""
        return Level(self.level_number + 1, self.difficulty)


class GameState:
    """Состояния игры."""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    LEVEL_COMPLETE = "level_complete"
    GAME_OVER = "game_over"
    WIN = "win"


class Game:
    """
    Главный класс игры Breakout.
    
    Управляет игровым циклом, состояниями, логикой и рендерингом.
    """
    
    def __init__(self, player_name: str = "Player", difficulty: str = "medium", 
                 max_levels: int = MAX_LEVEL):
        """
        Инициализация игры.
        
        Args:
            player_name: Имя игрока.
            difficulty: Уровень сложности (easy, medium, hard).
            max_levels: Максимальный номер уровня.
        """
        pygame.init()
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Breakout Game")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.player_name = player_name
        self.difficulty = difficulty
        self.max_levels = max_levels
        
        # Компоненты игры
        self.level = Level(1, difficulty)
        self.paddle = Paddle(self.level.speed_multiplier)
        
        # Менеджеры
        self.stats_manager = StatsManager()
        self.sound_manager = SoundManager()  # ← ДОБАВЛЕНО
        
        # Шар с звуком
        self.ball = Ball(WINDOW_WIDTH // 2, PADDLE_Y - 10, 
                        self.level.speed_multiplier, self.sound_manager)  # ← ДОБАВЛЕНО
        
        # Состояние игры
        self.state = GameState.MENU
        self.start_time = time.time()
        
        # Шрифты
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        self._init_level()

    def _init_level(self) -> None:
        """Инициализировать текущий уровень."""
        self.level.generate()
        self.paddle.reset()
        self.ball.reset(self.paddle.x, self.paddle.width)
        
        # Звук начала уровня
        if self.state == GameState.PLAYING:
            self.sound_manager.play_level_start()  # ← ДОБАВЛЕНО

    def handle_events(self) -> None:
        """Обработать события."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == GameState.MENU:
                        self.state = GameState.PLAYING
                        self.start_time = time.time()
                        self.sound_manager.play_level_start()  # ← ДОБАВЛЕНО
                        
                    elif self.state == GameState.PLAYING and not self.ball.is_active:
                        self.ball.launch()
                        
                    elif self.state == GameState.LEVEL_COMPLETE:
                        if self.level.level_number >= self.max_levels:
                            self.state = GameState.WIN
                            self.sound_manager.play_victory()  # ← ДОБАВЛЕНО
                        else:
                            self.level = self.level.next_level()
                            self.paddle = Paddle(self.level.speed_multiplier)
                            self.ball = Ball(WINDOW_WIDTH // 2, PADDLE_Y - 10, 
                                           self.level.speed_multiplier, self.sound_manager)
                            self._init_level()
                            self.state = GameState.PLAYING
                            
                    elif self.state in (GameState.GAME_OVER, GameState.WIN):
                        self._save_result()
                        self.__init__(self.player_name, self.difficulty, self.max_levels)
                        
                elif event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    else:
                        self._save_result()
                        self.running = False

        # Постоянные нажатия клавиш
        if self.state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move_left()
            if keys[pygame.K_RIGHT]:
                self.paddle.move_right()

    def update(self) -> None:
        """Обновить логику игры."""
        if self.state != GameState.PLAYING:
            return

        self.ball.update()
        
        # Столкновение с платформой
        if self.ball.check_paddle_collision(self.paddle.get_rect()):
            self.sound_manager.play_paddle_hit()  # ← ДОБАВЛЕНО
        
        # Столкновения с кирпичами
        for brick in self.level.bricks.get_active_bricks():
            collided, _ = self.ball.check_brick_collision(brick.get_rect())
            if collided:
                brick.destroy()
                self.level.on_brick_destroyed()
                self.ball.increase_speed(1.01)
                self.sound_manager.play_brick_hit()  # ← ДОБАВЛЕНО
        
        self.level.bricks.remove_destroyed()
        
        # Потеря шара
        if self.ball.is_out_of_bounds():
            self.sound_manager.play_ball_lost()  # ← ДОБАВЛЕНО
            if not self.level.on_ball_lost():
                self.state = GameState.GAME_OVER
                self.sound_manager.play_game_over()  # ← ДОБАВЛЕНО
            else:
                self.ball.reset(self.paddle.x, self.paddle.width)
        
        # Завершение уровня
        if self.level.is_complete():
            self.state = GameState.LEVEL_COMPLETE
            self.sound_manager.play_level_complete()  # ← ДОБАВЛЕНО

    def render(self) -> None:
        """Отрисовать экран."""
        self.screen.fill(COLOR_BLACK)
        
        if self.state == GameState.MENU:
            self._draw_menu()
            
        elif self.state in (GameState.PLAYING, GameState.PAUSED):
            self._draw_game()
            if self.state == GameState.PAUSED:
                self._draw_pause()
                
        elif self.state == GameState.LEVEL_COMPLETE:
            self._draw_game()
            self._draw_level_complete()
            
        elif self.state == GameState.GAME_OVER:
            self._draw_game_over()
            
        elif self.state == GameState.WIN:
            self._draw_victory()
        
        pygame.display.flip()

    def _draw_menu(self) -> None:
        """Отрисовать меню."""
        title = self.font_large.render("BREAKOUT", True, COLOR_CYAN)
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 100))
        
        player_text = self.font_small.render(f"Player: {self.player_name}", True, COLOR_WHITE)
        self.screen.blit(player_text, (WINDOW_WIDTH // 2 - player_text.get_width() // 2, 200))
        
        difficulty_text = self.font_small.render(f"Difficulty: {self.difficulty.upper()}", 
                                                 True, COLOR_YELLOW)
        self.screen.blit(difficulty_text, (WINDOW_WIDTH // 2 - difficulty_text.get_width() // 2, 250))
        
        instruction = self.font_medium.render("Press SPACE to Start", True, COLOR_WHITE)
        self.screen.blit(instruction, (WINDOW_WIDTH // 2 - instruction.get_width() // 2, 
                                       WINDOW_HEIGHT // 2))

    def _draw_game(self) -> None:
        """Отрисовать игровой экран."""
        # Платформа
        paddle_rect = self.paddle.get_rect()
        pygame.draw.rect(self.screen, COLOR_WHITE, paddle_rect, border_radius=5)
        pygame.draw.rect(self.screen, COLOR_CYAN, paddle_rect, 2, border_radius=5)
        
        # Шар
        pygame.draw.circle(self.screen, COLOR_YELLOW, (int(self.ball.x), int(self.ball.y)), 
                          self.ball.radius)
        pygame.draw.circle(self.screen, COLOR_WHITE, (int(self.ball.x), int(self.ball.y)), 
                          self.ball.radius, 1)
        
        # Кирпичи
        for brick in self.level.bricks.get_active_bricks():
            brick_rect = brick.get_rect()
            pygame.draw.rect(self.screen, brick.color, brick_rect, border_radius=3)
            pygame.draw.rect(self.screen, COLOR_WHITE, brick_rect, 1, border_radius=3)
        
        # UI
        level_text = self.font_small.render(f"Level: {self.level.level_number}", True, COLOR_GREEN)
        self.screen.blit(level_text, (10, 10))
        
        score_text = self.font_small.render(f"Score: {self.level.score}", True, COLOR_WHITE)
        self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 10))
        
        lives_text = self.font_small.render(f"Lives: {self.level.lives}", True, COLOR_RED)
        self.screen.blit(lives_text, (WINDOW_WIDTH - lives_text.get_width() - 10, 10))

    def _draw_pause(self) -> None:
        """Отрисовать экран паузы."""
        pause_text = self.font_large.render("PAUSED", True, COLOR_YELLOW)
        self.screen.blit(pause_text, (WINDOW_WIDTH // 2 - pause_text.get_width() // 2, 
                                      WINDOW_HEIGHT // 2 - 50))
        
        resume_text = self.font_small.render("Press ESC to Resume", True, COLOR_WHITE)
        self.screen.blit(resume_text, (WINDOW_WIDTH // 2 - resume_text.get_width() // 2,
                                       WINDOW_HEIGHT // 2 + 50))

    def _draw_level_complete(self) -> None:
        """Отрисовать завершение уровня."""
        complete_text = self.font_large.render(f"LEVEL {self.level.level_number} COMPLETE!", 
                                               True, COLOR_GREEN)
        self.screen.blit(complete_text, (WINDOW_WIDTH // 2 - complete_text.get_width() // 2,
                                        WINDOW_HEIGHT // 2 - 50))
        
        next_text = self.font_small.render("Press SPACE for Next Level", True, COLOR_WHITE)
        self.screen.blit(next_text, (WINDOW_WIDTH // 2 - next_text.get_width() // 2,
                                    WINDOW_HEIGHT // 2 + 50))

    def _draw_game_over(self) -> None:
        """Отрисовать экран Game Over."""
        game_over_text = self.font_large.render("GAME OVER", True, COLOR_RED)
        self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2,
                                         WINDOW_HEIGHT // 2 - 80))
        
        score_text = self.font_medium.render(f"Score: {self.level.score}", True, COLOR_WHITE)
        self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2,
                                     WINDOW_HEIGHT // 2))
        
        level_text = self.font_small.render(f"Level Reached: {self.level.level_number}", 
                                           True, COLOR_YELLOW)
        self.screen.blit(level_text, (WINDOW_WIDTH // 2 - level_text.get_width() // 2,
                                     WINDOW_HEIGHT // 2 + 40))
        
        retry_text = self.font_small.render("Press SPACE to Return to Menu", True, COLOR_WHITE)
        self.screen.blit(retry_text, (WINDOW_WIDTH // 2 - retry_text.get_width() // 2,
                                     WINDOW_HEIGHT // 2 + 100))

    def _draw_victory(self) -> None:
        """Отрисовать экран победы."""
        victory_text = self.font_large.render("YOU WIN!", True, COLOR_GREEN)
        self.screen.blit(victory_text, (WINDOW_WIDTH // 2 - victory_text.get_width() // 2,
                                       WINDOW_HEIGHT // 2 - 80))
        
        score_text = self.font_medium.render(f"Score: {self.level.score}", True, COLOR_WHITE)
        self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2,
                                     WINDOW_HEIGHT // 2))
        
        menu_text = self.font_small.render("Press SPACE to Return to Menu", True, COLOR_WHITE)
        self.screen.blit(menu_text, (WINDOW_WIDTH // 2 - menu_text.get_width() // 2,
                                    WINDOW_HEIGHT // 2 + 60))

    def _save_result(self) -> None:
        """Сохранить результат игры."""
        game_duration = time.time() - self.start_time
        is_win = self.state == GameState.WIN
        
        self.stats_manager.save_game_result(
            player_name=self.player_name,
            score=self.level.score,
            level_reached=self.level.level_number,
            difficulty=self.difficulty,
            game_duration=game_duration,
            win=is_win
        )
        
        print(f"\n✓ Результат сохранен для игрока {self.player_name}")
        print(f"  Счет: {self.level.score}")
        print(f"  Уровень: {self.level.level_number}")
        print(f"  Сложность: {self.difficulty}")
        print(f"  Результат: {'Победа' if is_win else 'Проигрыш'}")

    def run(self) -> None:
        """Главный игровой цикл."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Создать парсер аргументов командной строки.
    
    Returns:
        ArgumentParser: Парсер с описанными аргументами.
    """
    parser = argparse.ArgumentParser(
        description="Breakout Game - классическая аркадная игра",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py --name "Player1" --difficulty hard
  python main.py -n "MyName" -d easy --levels 3
  python main.py --show-stats
        """
    )
    
    parser.add_argument(
        '-n', '--name',
        type=str,
        default='Player',
        help='Имя игрока (по умолчанию: Player)'
    )
    
    parser.add_argument(
        '-d', '--difficulty',
        type=str,
        choices=['easy', 'medium', 'hard'],
        default='medium',
        help='Уровень сложности (по умолчанию: medium)'
    )
    
    parser.add_argument(
        '-l', '--levels',
        type=int,
        default=MAX_LEVEL,
        help=f'Максимальное количество уровней (по умолчанию: {MAX_LEVEL})'
    )
    
    parser.add_argument(
        '--show-stats',
        action='store_true',
        help='Показать статистику всех игр и выйти'
    )
    
    parser.add_argument(
        '--show-player-stats',
        type=str,
        metavar='PLAYER_NAME',
        help='Показать статистику конкретного игрока и выйти'
    )
    
    parser.add_argument(
        '--show-top',
        type=int,
        default=None,
        metavar='N',
        help='Показать топ N рекордов и выйти'
    )
    
    parser.add_argument(
        '--clear-stats',
        action='store_true',
        help='Очистить всю сохраненную статистику и выйти'
    )
    
    return parser


def display_statistics(args) -> None:
    """
    Отобразить статистику согласно аргументам.
    
    Args:
        args: Аргументы командной строки.
    """
    stats_manager = StatsManager()
    
    if args.clear_stats:
        if stats_manager.clear_stats():
            print("✓ Статистика успешно очищена")
        else:
            print("✗ Ошибка при очистке статистики")
        return
    
    if args.show_player_stats:
        player_games = stats_manager.get_player_stats(args.show_player_stats)
        if player_games:
            print(f"\n{'='*60}")
            print(f"Статистика игрока: {args.show_player_stats}")
            print(f"{'='*60}")
            for i, game in enumerate(player_games, 1):
                print(f"\nИгра #{i}")
                print(f"  Дата: {game['timestamp']}")
                print(f"  Счет: {game['score']}")
                print(f"  Уровень: {game['level_reached']}")
                print(f"  Сложность: {game['difficulty']}")
                print(f"  Время: {game['game_duration']}с")
                print(f"  Результат: {'Победа' if game['won'] else 'Проигрыш'}")
        else:
            print(f"Нет данных для игрока: {args.show_player_stats}")
        return
    
    if args.show_stats:
        summary = stats_manager.get_statistics_summary()
        if summary:
            print(f"\n{'='*60}")
            print("ОБЩАЯ СТАТИСТИКА")
            print(f"{'='*60}")
            print(f"Всего игр: {summary['total_games']}")
            print(f"Побед: {summary['wins']}")
            print(f"Проигрышей: {summary['losses']}")
            print(f"Процент побед: {summary['win_rate']}%")
            print(f"Средний счет: {summary['average_score']}")
            print(f"Максимальный счет: {summary['max_score']}")
            print(f"Минимальный счет: {summary['min_score']}")
            print(f"Среднее время игры: {summary['average_duration']}с")
            print(f"Уникальных игроков: {summary['unique_players']}")
        else:
            print("Нет сохраненной статистики")
        return
    
    # Показать топ рекордов
    if args.show_top:
        top_scores = stats_manager.get_high_scores(args.show_top)
        if top_scores:
            print(f"\n{'='*60}")
            print(f"ТОП {args.show_top} РЕКОРДОВ")
            print(f"{'='*60}")
            for i, game in enumerate(top_scores, 1):
                print(f"{i:2}. {game['player_name']:20} {game['score']:6} "
                      f"уровень {game['level_reached']} ({game['difficulty']})")
        else:
            print("Нет сохраненной статистики")


def main():
    """Точка входа в программу."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Проверка режимов статистики
    stats_mode = (
        args.show_stats or 
        args.show_player_stats is not None or 
        args.clear_stats or
        args.show_top is not None
    )
    
    if stats_mode:
        display_statistics(args)
        return
    
    # Запуск игры
    print(f"\n{'='*60}")
    print("🎮 BREAKOUT GAME")
    print(f"{'='*60}")
    print(f"Игрок: {args.name}")
    print(f"Сложность: {args.difficulty}")
    print(f"Уровней: {args.levels}")
    print(f"{'='*60}\n")
    
    game = Game(args.name, args.difficulty, args.levels)
    game.run()


if __name__ == "__main__":
    main()
