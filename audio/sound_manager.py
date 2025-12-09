
import pygame
import os

class SoundManager:
    
    def __init__(self):
        pygame.mixer.init()
        self.sounds_dir = "audio/sounds/"
        
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
        self._play_sound('paddle_hit')
    
    def play_brick_hit(self):
        self._play_sound('brick_hit')
    
    def play_wall_hit(self):
        self._play_sound('wall_hit')
    
    def play_ball_lost(self):
        self._play_sound('ball_lost')
    
    def play_game_over(self):
        self._play_sound('game_over')
    
    def play_level_complete(self):
        self._play_sound('level_complete')
    
    def play_victory(self):
        self._play_sound('victory')
    
    def play_ball_launch(self):
        self._play_sound('ball_launch')
    
    def play_level_start(self):
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