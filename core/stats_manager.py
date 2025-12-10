"""
Модуль для управления статистикой игры Breakout.
Сохраняет результаты в JSON формат и предоставляет методы для анализа.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# Импорт из config
try:
    from config import STATS_FILE, STATS_DIR
except ImportError:
    STATS_FILE = "game_stats.json"
    STATS_DIR = "stats"


class StatsManager:
    """Класс для управления статистикой игр."""
    
    def __init__(self):
        """Инициализация менеджера статистики."""
        self._ensure_stats_dir()
    
    def _ensure_stats_dir(self) -> None:
        """Создать директорию для статистики если её нет."""
        if not os.path.exists(STATS_DIR):
            os.makedirs(STATS_DIR)
    
    def _get_stats_path(self) -> str:
        """Получить полный путь к файлу статистики."""
        return os.path.join(STATS_DIR, STATS_FILE)
    
    def save_game_result(
        self,
        player_name: str,
        score: int,
        level_reached: int,
        difficulty: str,
        game_duration: float,
        win: bool
    ) -> bool:
        """
        Сохранить результат игры.
        
        Args:
            player_name: Имя игрока.
            score: Финальный счет.
            level_reached: Достигнутый уровень.
            difficulty: Сложность (easy/medium/hard).
            game_duration: Длительность игры в секундах.
            win: True если игрок победил.
        
        Returns:
            True если сохранение успешно.
        """
        try:
            stats_path = self._get_stats_path()
            
            # Загрузить существующую статистику
            if os.path.exists(stats_path):
                with open(stats_path, 'r', encoding='utf-8') as f:
                    all_stats = json.load(f)
            else:
                all_stats = []
            
            # Создать запись об игре
            game_record = {
                "timestamp": datetime.now().isoformat(),
                "player_name": player_name,
                "score": score,
                "level_reached": level_reached,
                "difficulty": difficulty,
                "game_duration": round(game_duration, 2),
                "won": win
            }
            
            all_stats.append(game_record)
            
            # Сохранить обновленную статистику
            with open(stats_path, 'w', encoding='utf-8') as f:
                json.dump(all_stats, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Ошибка сохранения статистики: {e}")
            return False
    
    def load_all_stats(self) -> List[Dict[str, Any]]:
        """
        Загрузить всю статистику.
        
        Returns:
            Список всех игровых записей.
        """
        try:
            stats_path = self._get_stats_path()
            if os.path.exists(stats_path):
                with open(stats_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки статистики: {e}")
        
        return []
    
    def get_player_stats(self, player_name: str) -> List[Dict[str, Any]]:
        """
        Получить статистику конкретного игрока.
        
        Args:
            player_name: Имя игрока.
        
        Returns:
            Список игр этого игрока.
        """
        all_stats = self.load_all_stats()
        return [stat for stat in all_stats if stat["player_name"] == player_name]
    
    def get_high_scores(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Получить топ рекордов.
        
        Args:
            limit: Количество рекордов.
        
        Returns:
            Список топ игр отсортированных по счету.
        """
        all_stats = self.load_all_stats()
        sorted_stats = sorted(all_stats, key=lambda x: x["score"], reverse=True)
        return sorted_stats[:limit]
    
    def get_statistics_summary(self) -> Optional[Dict[str, Any]]:
        """
        Получить общую статистику.
        
        Returns:
            Словарь с общей статистикой или None если данных нет.
        """
        all_stats = self.load_all_stats()
        if not all_stats:
            return None
        
        total_games = len(all_stats)
        wins = sum(1 for stat in all_stats if stat["won"])
        losses = total_games - wins
        
        scores = [stat["score"] for stat in all_stats]
        durations = [stat["game_duration"] for stat in all_stats]
        
        return {
            "total_games": total_games,
            "wins": wins,
            "losses": losses,
            "win_rate": round((wins / total_games) * 100, 2) if total_games else 0,
            "average_score": round(sum(scores) / total_games, 2) if total_games else 0,
            "max_score": max(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "average_duration": round(sum(durations) / total_games, 2) if total_games else 0,
            "unique_players": len(set(stat["player_name"] for stat in all_stats))
        }
    
    def clear_stats(self) -> bool:
        """
        Очистить всю статистику.
        
        Returns:
            True если очистка успешна.
        """
        try:
            stats_path = self._get_stats_path()
            if os.path.exists(stats_path):
                os.remove(stats_path)
            return True
        except Exception as e:
            print(f"Ошибка очистки статистики: {e}")
            return False
