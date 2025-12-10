

import pygame
import os


class SoundManager:
   

    def __init__(self):
        
        pygame.mixer.init()
        
        
        self.sounds_dir = "audio/sounds/"
        
        
        self.sounds = {
            'paddle_hit': None,      # При ударе шара по платформе
            'brick_hit': None,       # При ударе шара по кирпичу
            'wall_hit': None,        # При ударе шара по стене
            'ball_lost': None,       # При потере шара
            'game_over': None,       # При проигрыше
            'level_complete': None,  # При завершении уровня
            'victory': None,         # При победе
            'ball_launch': None,     # При запуске шара
            'level_start': None,     # При начале уровня
        }
        
        self.music_volume = 0.5
        self.sound_volume = 0.7
        
        self._load_sounds()

    def _load_sounds(self):
        
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

    def play_paddle_hit(self):
        """Проиграть звук удара шара по платформе"""
        self._play_sound('paddle_hit')

    def play_brick_hit(self):
        """Проиграть звук удара шара по кирпичу"""
        self._play_sound('brick_hit')

    def play_wall_hit(self):
        """Проиграть звук удара шара по стене"""
        self._play_sound('wall_hit')

    def play_ball_lost(self):
        """Проиграть звук потери шара"""
        self._play_sound('ball_lost')

    def play_game_over(self):
        """Проиграть звук Game Over"""
        self._play_sound('game_over')

    def play_level_complete(self):
        """Проиграть звук завершения уровня"""
        self._play_sound('level_complete')

    def play_victory(self):
        """Проиграть звук победы"""
        self._play_sound('victory')

    def play_ball_launch(self):
        """Проиграть звук запуска шара"""
        self._play_sound('ball_launch')

    def play_level_start(self):
        """Проиграть звук начала уровня"""
        self._play_sound('level_start')

    def _play_sound(self, sound_key):
        
        if sound_key in self.sounds and self.sounds[sound_key] is not None:
            try:
                self.sounds[sound_key].play()
            except pygame.error as e:
                print(f"Ошибка при проигрывании звука {sound_key}: {e}")

    def set_sound_volume(self, volume):
        
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound is not None:
                sound.set_volume(self.sound_volume)

    def mute_all(self):
       
        self.set_sound_volume(0.0)

    def unmute_all(self):
        
        self.set_sound_volume(0.7)
