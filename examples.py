"""
Примеры использования игры Breakout.

Этот модуль содержит примеры кода для различных вариантов запуска игры
и работы с статистикой.
"""

from main import Game, create_argument_parser
from stats_manager import StatsManager


def example_1_basic_game():
    """Пример 1: Базовый запуск игры."""
    print("=" * 60)
    print("Пример 1: Базовая игра со стандартными параметрами")
    print("=" * 60)
    
    game = Game(player_name="Player", difficulty="medium", max_levels=5)
    game.run()


def example_2_custom_game():
    """Пример 2: Игра с пользовательскими параметрами."""
    print("=" * 60)
    print("Пример 2: Игра с кастомными параметрами")
    print("=" * 60)
    
    # Создать жесткую игру для опытного игрока
    game = Game(player_name="ProPlayer", difficulty="hard", max_levels=10)
    game.run()


def example_3_easy_mode():
    """Пример 3: Легкий режим для новичков."""
    print("=" * 60)
    print("Пример 3: Легкий режим")
    print("=" * 60)
    
    game = Game(player_name="Beginner", difficulty="easy", max_levels=3)
    game.run()


def example_4_show_statistics():
    """Пример 4: Просмотр статистики всех игр."""
    print("=" * 60)
    print("Пример 4: Общая статистика")
    print("=" * 60)
    
    stats = StatsManager()
    summary = stats.get_statistics_summary()
    
    if summary:
        print(f"Всего игр сыграно: {summary['total_games']}")
        print(f"Побед: {summary['wins']}")
        print(f"Проигрышей: {summary['losses']}")
        print(f"Процент побед: {summary['win_rate']}%")
        print(f"Средний счет: {summary['average_score']}")
        print(f"Максимальный счет: {summary['max_score']}")
        print(f"Минимальный счет: {summary['min_score']}")
        print(f"Среднее время игры: {summary['average_duration']}сек")
        print(f"Уникальных игроков: {summary['unique_players']}")
    else:
        print("Нет сохраненной статистики")


def example_5_show_player_stats():
    """Пример 5: Статистика конкретного игрока."""
    print("=" * 60)
    print("Пример 5: Статистика игрока")
    print("=" * 60)
    
    stats = StatsManager()
    player_name = input("Введите имя игрока: ")
    
    player_stats = stats.get_player_stats(player_name)
    
    if player_stats:
        print(f"\nИгры игрока {player_name}:")
        for i, game in enumerate(player_stats, 1):
            print(f"\nИгра #{i}")
            print(f"  Дата: {game['timestamp']}")
            print(f"  Счет: {game['score']}")
            print(f"  Уровень: {game['level_reached']}")
            print(f"  Сложность: {game['difficulty']}")
            print(f"  Время: {game['game_duration']}сек")
            print(f"  Результат: {'Победа' if game['won'] else 'Проигрыш'}")
    else:
        print(f"Нет данных для игрока {player_name}")


def example_6_high_scores():
    """Пример 6: Топ рекордов."""
    print("=" * 60)
    print("Пример 6: Топ 10 рекордов")
    print("=" * 60)
    
    stats = StatsManager()
    high_scores = stats.get_high_scores(10)
    
    if high_scores:
        print("\nТоп рекордов:")
        for i, game in enumerate(high_scores, 1):
            difficulty_icon = {
                "easy": "🟢",
                "medium": "🟡",
                "hard": "🔴"
            }.get(game['difficulty'], "❓")
            
            result_icon = "✓" if game['won'] else "✗"
            
            print(f"{i:2}. {game['player_name']:20} {game['score']:6} "
                  f"уровень {game['level_reached']} {difficulty_icon} {result_icon}")
    else:
        print("Нет сохраненной статистики")


def example_7_compare_difficulties():
    """Пример 7: Сравнение сложностей."""
    print("=" * 60)
    print("Пример 7: Анализ по сложности")
    print("=" * 60)
    
    stats = StatsManager()
    all_games = stats.load_all_stats()
    
    difficulties = {"easy": [], "medium": [], "hard": []}
    
    for game in all_games:
        if game['difficulty'] in difficulties:
            difficulties[game['difficulty']].append(game['score'])
    
    for diff, scores in difficulties.items():
        if scores:
            avg_score = sum(scores) / len(scores)
            max_score = max(scores)
            min_score = min(scores)
            print(f"\n{diff.upper()}:")
            print(f"  Игр: {len(scores)}")
            print(f"  Средний счет: {avg_score:.0f}")
            print(f"  Максимум: {max_score}")
            print(f"  Минимум: {min_score}")


def example_8_quick_stats():
    """Пример 8: Быстрый просмотр статистики."""
    print("=" * 60)
    print("Пример 8: Быстрая статистика")
    print("=" * 60)
    
    stats = StatsManager()
    summary = stats.get_statistics_summary()
    
    if summary:
        # Красивый вывод
        print(f"\n📊 СТАТИСТИКА ИГРЫ")
        print(f"{'─' * 40}")
        print(f"Всего игр:      {summary['total_games']:3} |  Побед: {summary['wins']:3} "
              f"| Проигрышей: {summary['losses']:3}")
        print(f"Процент побед:  {summary['win_rate']:5}%")
        print(f"Средний счет:   {summary['average_score']:6.0f}")
        print(f"Рекорд:         {summary['max_score']:6}")
        print(f"Время игры:     {summary['average_duration']:6.1f}сек")
        print(f"Игроков:        {summary['unique_players']:3}")
        print(f"{'─' * 40}\n")
    else:
        print("📭 Нет сохраненной статистики\n")


def example_9_menu():
    """Пример 9: Интерактивное меню."""
    print("=" * 60)
    print("Пример 9: Интерактивное меню")
    print("=" * 60)
    
    while True:
        print("\n🎮 ГЛАВНОЕ МЕНЮ")
        print("1. Новая игра (medium)")
        print("2. Новая игра (easy)")
        print("3. Новая игра (hard)")
        print("4. Просмотреть статистику")
        print("5. Просмотреть рекорды")
        print("6. Выход")
        
        choice = input("\nВыберите опцию (1-6): ").strip()
        
        if choice == "1":
            name = input("Введите ваше имя: ")
            game = Game(player_name=name, difficulty="medium")
            game.run()
            
        elif choice == "2":
            name = input("Введите ваше имя: ")
            game = Game(player_name=name, difficulty="easy")
            game.run()
            
        elif choice == "3":
            name = input("Введите ваше имя: ")
            game = Game(player_name=name, difficulty="hard")
            game.run()
            
        elif choice == "4":
            example_8_quick_stats()
            
        elif choice == "5":
            example_6_high_scores()
            
        elif choice == "6":
            print("До свидания! 👋")
            break
        
        else:
            print("❌ Неверная опция")


def example_10_tournament_mode():
    """Пример 10: Режим турнира."""
    print("=" * 60)
    print("Пример 10: Режим турнира")
    print("=" * 60)
    
    players = []
    
    # Ввод участников
    print("\nВведите имена игроков (пусто для завершения):")
    counter = 1
    while True:
        name = input(f"Игрок {counter}: ").strip()
        if not name:
            break
        players.append(name)
        counter += 1
    
    if not players:
        print("Нет участников!")
        return
    
    print(f"\nТурнир: {len(players)} участников")
    print(f"Участники: {', '.join(players)}")
    
    difficulty = input("\nУровень сложности (easy/medium/hard): ").strip().lower()
    if difficulty not in ["easy", "medium", "hard"]:
        difficulty = "medium"
    
    # Запустить игры
    for player in players:
        print(f"\n{'='*40}")
        print(f"Ход игрока: {player}")
        print(f"{'='*40}")
        
        game = Game(player_name=player, difficulty=difficulty)
        game.run()
    
    # Показать результаты
    print(f"\n{'='*60}")
    print("РЕЗУЛЬТАТЫ ТУРНИРА")
    print(f"{'='*60}")
    
    stats = StatsManager()
    for player in players:
        player_games = stats.get_player_stats(player)
        if player_games:
            last_game = player_games[-1]  # Последняя игра
            print(f"{player:20} - Счет: {last_game['score']:5} | "
                  f"Уровень: {last_game['level_reached']} | "
                  f"{'Победа' if last_game['won'] else 'Проигрыш'}")
    
    # Определить победителя
    all_players_stats = []
    for player in players:
        player_games = stats.get_player_stats(player)
        if player_games:
            total_score = sum(g['score'] for g in player_games)
            all_players_stats.append((player, total_score))
    
    if all_players_stats:
        all_players_stats.sort(key=lambda x: x[1], reverse=True)
        print(f"\n🏆 ПОБЕДИТЕЛЬ: {all_players_stats[0][0]} "
              f"({all_players_stats[0][1]} очков)")


# Главное меню примеров
def main():
    """Главная функция для выбора примера."""
    print("\n" + "=" * 60)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ИГРЫ BREAKOUT")
    print("=" * 60)
    
    examples = {
        "1": ("Базовая игра", example_1_basic_game),
        "2": ("Кастомная игра", example_2_custom_game),
        "3": ("Легкий режим", example_3_easy_mode),
        "4": ("Общая статистика", example_4_show_statistics),
        "5": ("Статистика игрока", example_5_show_player_stats),
        "6": ("Топ рекордов", example_6_high_scores),
        "7": ("Анализ по сложности", example_7_compare_difficulties),
        "8": ("Быстрая статистика", example_8_quick_stats),
        "9": ("Интерактивное меню", example_9_menu),
        "10": ("Режим турнира", example_10_tournament_mode),
    }
    
    for key, (title, _) in examples.items():
        print(f"{key:2}. {title}")
    
    print("\n0. Выход")
    
    choice = input("\nВыберите пример (0-10): ").strip()
    
    if choice == "0":
        print("До свидания!")
        return
    
    if choice in examples:
        example_func = examples[choice][1]
        example_func()
    else:
        print("❌ Неверный выбор")


if __name__ == "__main__":
    main()
