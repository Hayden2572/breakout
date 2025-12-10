"""
Модульные тесты для игры Breakout.

Содержит тесты для ключевых компонентов игры:
- Статистики
- Платформы
- Кирпичей
- Шара
- Уровней
"""

import unittest
import os
import json
import tempfile
from unittest.mock import patch, MagicMock
from config import STATS_DIR, STATS_FILE, DIFFICULTY_LIVES, DIFFICULTY_MULTIPLIERS
from core.stats_manager import StatsManager
from main import Paddle, Brick, BrickGroup, Ball, Level, Game


class TestStatsManager(unittest.TestCase):
    """Тесты для менеджера статистики."""

    def setUp(self):
        """Подготовка к тестам."""
        self.temp_dir = tempfile.mkdtemp()
        self.stats_manager = StatsManager()

    def tearDown(self):
        """Очистка после тестов."""
        self.stats_manager.clear_stats()

    def test_save_game_result(self):
        """Тест сохранения результата игры."""
        result = self.stats_manager.save_game_result(
            player_name="TestPlayer",
            score=1500,
            level_reached=3,
            difficulty="medium",
            game_duration=120.5,
            win=False
        )
        
        self.assertTrue(result)
        
        # Проверить, что файл был создан
        stats_path = self.stats_manager._get_stats_path()
        self.assertTrue(os.path.exists(stats_path))

    def test_load_all_stats(self):
        """Тест загрузки всей статистики."""
        # Сохранить несколько результатов
        for i in range(3):
            self.stats_manager.save_game_result(
                player_name=f"Player{i}",
                score=1000 + i * 100,
                level_reached=i + 1,
                difficulty="medium",
                game_duration=100.0,
                win=i % 2 == 0
            )
        
        all_stats = self.stats_manager.load_all_stats()
        self.assertEqual(len(all_stats), 3)

    def test_get_player_stats(self):
        """Тест получения статистики игрока."""
        # Сохранить несколько игр для одного игрока
        for i in range(2):
            self.stats_manager.save_game_result(
                player_name="Player1",
                score=1000 + i * 100,
                level_reached=1,
                difficulty="medium",
                game_duration=100.0,
                win=True
            )
        
        # Сохранить игру для другого игрока
        self.stats_manager.save_game_result(
            player_name="Player2",
            score=2000,
            level_reached=2,
            difficulty="hard",
            game_duration=200.0,
            win=False
        )
        
        player1_stats = self.stats_manager.get_player_stats("Player1")
        self.assertEqual(len(player1_stats), 2)

    def test_get_high_scores(self):
        """Тест получения рекордов."""
        scores = [2000, 1000, 3000, 500, 2500]
        
        for i, score in enumerate(scores):
            self.stats_manager.save_game_result(
                player_name=f"Player{i}",
                score=score,
                level_reached=1,
                difficulty="medium",
                game_duration=100.0,
                win=False
            )
        
        high_scores = self.stats_manager.get_high_scores(3)
        
        self.assertEqual(len(high_scores), 3)
        self.assertEqual(high_scores[0]["score"], 3000)
        self.assertEqual(high_scores[1]["score"], 2500)
        self.assertEqual(high_scores[2]["score"], 2000)

    def test_get_statistics_summary(self):
        """Тест получения общей статистики."""
        # Сохранить несколько результатов
        self.stats_manager.save_game_result("Player1", 1000, 2, "medium", 100.0, True)
        self.stats_manager.save_game_result("Player1", 500, 1, "easy", 50.0, False)
        self.stats_manager.save_game_result("Player2", 2000, 3, "hard", 200.0, True)
        
        summary = self.stats_manager.get_statistics_summary()
        
        self.assertEqual(summary["total_games"], 3)
        self.assertEqual(summary["wins"], 2)
        self.assertEqual(summary["losses"], 1)
        self.assertEqual(summary["unique_players"], 2)

    def test_clear_stats(self):
        """Тест очистки статистики."""
        # Сохранить результат
        self.stats_manager.save_game_result(
            "Player1", 1000, 1, "medium", 100.0, True
        )
        
        # Очистить
        result = self.stats_manager.clear_stats()
        self.assertTrue(result)
        
        # Проверить, что статистика пуста
        all_stats = self.stats_manager.load_all_stats()
        self.assertEqual(len(all_stats), 0)


class TestPaddle(unittest.TestCase):
    """Тесты для класса платформы."""

    def setUp(self):
        """Подготовка к тестам."""
        self.paddle = Paddle()

    def test_paddle_initialization(self):
        """Тест инициализации платформы."""
        self.assertEqual(self.paddle.width, 100)
        self.assertEqual(self.paddle.height, 15)
        self.assertGreater(self.paddle.x, 0)

    def test_move_left(self):
        """Тест движения влево."""
        initial_x = self.paddle.x
        self.paddle.move_left()
        self.assertLess(self.paddle.x, initial_x)

    def test_move_right(self):
        """Тест движения вправо."""
        initial_x = self.paddle.x
        self.paddle.move_right()
        self.assertGreater(self.paddle.x, initial_x)

    def test_move_left_boundary(self):
        """Тест границы влево."""
        self.paddle.x = 5
        self.paddle.move_left()
        self.assertGreaterEqual(self.paddle.x, 0)

    def test_reset(self):
        """Тест сброса позиции."""
        self.paddle.move_left()
        self.paddle.reset()
        # Проверить, что платформа вернулась в центр
        from config import WINDOW_WIDTH
        expected_x = (WINDOW_WIDTH - 100) // 2
        self.assertEqual(self.paddle.x, expected_x)

    def test_speed_multiplier(self):
        """Тест множителя скорости."""
        paddle_fast = Paddle(speed_multiplier=2.0)
        self.assertEqual(paddle_fast.speed, 16)  # 8 * 2


class TestBrick(unittest.TestCase):
    """Тесты для класса кирпича."""

    def setUp(self):
        """Подготовка к тестам."""
        self.brick = Brick(100, 50)

    def test_brick_initialization(self):
        """Тест инициализации кирпича."""
        self.assertEqual(self.brick.x, 100)
        self.assertEqual(self.brick.y, 50)
        self.assertFalse(self.brick.is_destroyed)

    def test_destroy_brick(self):
        """Тест разрушения кирпича."""
        self.brick.destroy()
        self.assertTrue(self.brick.is_destroyed)

    def test_set_color(self):
        """Тест установки цвета."""
        color = (255, 0, 0)
        self.brick.set_color(color)
        self.assertEqual(self.brick.color, color)


class TestBrickGroup(unittest.TestCase):
    """Тесты для группы кирпичей."""

    def setUp(self):
        """Подготовка к тестам."""
        self.group = BrickGroup()

    def test_generate_level(self):
        """Тест генерации уровня."""
        self.group.generate_level(rows=2, cols=3)
        self.assertEqual(len(self.group.bricks), 6)

    def test_get_active_bricks(self):
        """Тест получения активных кирпичей."""
        self.group.generate_level(rows=1, cols=3)
        
        # Разрушить один кирпич
        self.group.bricks[0].destroy()
        
        active = self.group.get_active_bricks()
        self.assertEqual(len(active), 2)

    def test_is_level_complete(self):
        """Тест проверки завершения уровня."""
        self.group.generate_level(rows=1, cols=2)
        
        self.assertFalse(self.group.is_level_complete())
        
        # Разрушить все кирпичи
        for brick in self.group.bricks:
            brick.destroy()
        
        self.assertTrue(self.group.is_level_complete())

    def test_remove_destroyed(self):
        """Тест удаления разрушенных кирпичей."""
        self.group.generate_level(rows=1, cols=3)
        
        self.group.bricks[0].destroy()
        self.group.remove_destroyed()
        
        self.assertEqual(len(self.group.bricks), 2)


class TestBall(unittest.TestCase):
    """Тесты для класса шара."""

    def setUp(self):
        """Подготовка к тестам."""
        self.ball = Ball(400, 300)

    def test_ball_initialization(self):
        """Тест инициализации шара."""
        self.assertEqual(self.ball.x, 400)
        self.assertEqual(self.ball.y, 300)
        self.assertFalse(self.ball.is_active)

    def test_launch_ball(self):
        """Тест запуска шара."""
        self.ball.launch()
        self.assertTrue(self.ball.is_active)
        self.assertNotEqual(self.ball.vx, 0)
        self.assertNotEqual(self.ball.vy, 0)

    def test_is_out_of_bounds(self):
        """Тест проверки выхода за границы."""
        from config import WINDOW_HEIGHT
        
        self.ball.y = WINDOW_HEIGHT + 10
        self.assertTrue(self.ball.is_out_of_bounds())

    def test_reset_ball(self):
        """Тест сброса шара."""
        self.ball.launch()
        self.ball.reset(200, 100)
        
        self.assertFalse(self.ball.is_active)
        self.assertEqual(self.ball.vx, 0)
        self.assertEqual(self.ball.vy, 0)

    def test_speed_multiplier(self):
        """Тест множителя скорости."""
        ball_fast = Ball(400, 300, speed_multiplier=2.0)
        self.assertEqual(ball_fast.speed, 10)  # 5 * 2


class TestLevel(unittest.TestCase):
    """Тесты для класса уровня."""

    def setUp(self):
        """Подготовка к тестам."""
        self.level = Level(level_number=1)

    def test_level_initialization(self):
        """Тест инициализации уровня."""
        self.assertEqual(self.level.level_number, 1)
        self.assertEqual(self.level.score, 0)

    def test_add_score(self):
        """Тест добавления очков."""
        self.level.add_score(100)
        self.assertGreater(self.level.score, 0)

    def test_on_ball_lost(self):
        """Тест потери шара."""
        initial_lives = self.level.lives
        self.level.on_ball_lost()
        self.assertEqual(self.level.lives, initial_lives - 1)

    def test_difficulty_multiplier(self):
        """Тест множителя сложности."""
        easy_level = Level(1, "easy")
        medium_level = Level(1, "medium")
        hard_level = Level(1, "hard")
        
        self.assertLess(easy_level.speed_multiplier, medium_level.speed_multiplier)
        self.assertGreater(hard_level.speed_multiplier, medium_level.speed_multiplier)

    def test_difficulty_lives(self):
        """Тест жизней в зависимости от сложности."""
        easy_level = Level(1, "easy")
        hard_level = Level(1, "hard")
        
        self.assertGreater(easy_level.lives, hard_level.lives)

    def test_next_level(self):
        """Тест перехода на следующий уровень."""
        next_level = self.level.next_level()
        self.assertEqual(next_level.level_number, 2)


class TestArgumentParser(unittest.TestCase):
    """Тесты для парсера аргументов."""

    def setUp(self):
        """Подготовка к тестам."""
        from main import create_argument_parser
        self.parser = create_argument_parser()

    def test_default_arguments(self):
        """Тест значений по умолчанию."""
        args = self.parser.parse_args([])
        
        self.assertEqual(args.name, "Player")
        self.assertEqual(args.difficulty, "medium")
        self.assertEqual(args.levels, 5)
        self.assertFalse(args.show_stats)

    def test_custom_arguments(self):
        """Тест пользовательских аргументов."""
        args = self.parser.parse_args([
            "-n", "TestPlayer",
            "-d", "hard",
            "-l", "10"
        ])
        
        self.assertEqual(args.name, "TestPlayer")
        self.assertEqual(args.difficulty, "hard")
        self.assertEqual(args.levels, 10)

    def test_show_stats_argument(self):
        """Тест аргумента показа статистики."""
        args = self.parser.parse_args(["--show-stats"])
        self.assertTrue(args.show_stats)

    def test_invalid_difficulty(self):
        """Тест некорректной сложности."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["-d", "impossible"])


def run_tests():
    """Запустить все тесты."""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == "__main__":
    run_tests()
