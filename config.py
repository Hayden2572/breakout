# config.py
# Глобальная конфигурация игры

# Размеры окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Цвета (RGB)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 100, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GRAY = (100, 100, 100)
COLOR_CYAN = (0, 255, 255)
COLOR_MAGENTA = (255, 0, 255)

# Платформа (паддл)
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
PADDLE_Y = WINDOW_HEIGHT - 30

# Шар
BALL_SIZE = 8
BALL_SPEED = 5
BALL_MAX_SPEED = 10

# Кирпичи
BRICK_WIDTH = 70
BRICK_HEIGHT = 15
BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_SPACING = 5

# Уровни
LEVEL_SPEED_INCREMENT = 1.2  # Множитель скорости с каждым уровнем
NUM_LIVES = 3

# Шрифт
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24

STATS_FILE = "game_stats.json"
STATS_DIR = "stats"
DIFFICULTY_MULTIPLIERS = {...}
DIFFICULTY_LIVES = {...}

# Статистика
STATS_FILE = "game_stats.json"
STATS_DIR = "stats"

# Максимальный уровень
MAX_LEVEL = 5

# Параметры статистики
STATS_FILE = "game_stats.json"
STATS_DIR = "stats"

# Множители сложности (скорость)
DIFFICULTY_MULTIPLIERS = {
    "easy": 0.8,
    "medium": 1.0,
    "hard": 1.3,
}

# Количество жизней по сложности
DIFFICULTY_LIVES = {
    "easy": 5,
    "medium": 3,
    "hard": 1,
}