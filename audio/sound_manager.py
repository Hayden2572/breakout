# audio/sound_manager.py

import pygame
import os

class SoundManager:
    """Менеджер звуков и музыки"""
    
    def __init__(self):
        pygame.mixer.init()
        self.sounds_dir = "audio/sounds/"
        
        # Словарь загруженных звуков
        self.sounds = {
            'paddle_hit': None,
            'brick_hit': None,
            'wall_hit': None,
            'ball_lost': None,
            'game_over': None,
            'level_complete': None,
            'victory': None,
            'ball_launch': None,
            'level_start': None,
        }
        
        self.music_volume = 0.5
        self.sound_volume = 0.7

        def _load_sounds(self):
            """Загрузить все звуки из папки"""
            sound_files = {
                'paddle_hit': 'paddle_hit.wav',
                'brick_hit': 'brick_hit.wav',
                'wall_hit': 'wall_hit.wav',
                'ball_lost': 'ball_lost.wav',
                'game_over': 'game_over.wav',
                'level_complete': 'level_complete.wav',
                'victory': 'victory.wav',
                'ball_launch': 'ball_launch.wav',
                'level_start': 'level_start.wav',
            }
            
            for sound_key, filename in sound_files.items():
                try:
                    path = os.path.join(self.sounds_dir, filename)
                    if os.path.exists(path):
                        self.sounds[sound_key] = pygame.mixer.Sound(path)
                        self.sounds[sound_key].set_volume(self.sound_volume)
                except pygame.error as e:
                    print(f"Не удалось загрузить звук {filename}: {e}")