# audio/sound_manager.py

import pygame

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