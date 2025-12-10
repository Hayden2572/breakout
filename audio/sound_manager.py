import pygame
import numpy as np
import math

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.muted = False
        self._generate_sounds()
    
    def _generate_sounds(self):
        """Генерируем все звуки программно"""
        self.sounds = {
            'paddle_hit': self._generate_paddle_hit(),
            'brick_hit': self._generate_brick_hit(),
            'wall_hit': self._generate_wall_hit(),
            'game_over': self._generate_game_over(),
            'power_up': self._generate_power_up(),
            'victory': self._generate_victory(),
        }
    
    def _generate_tone(self, frequency, duration, volume=0.5, fade=0.05):
        """Базовая функция генерации тона"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            t = float(i) / sample_rate
            wave = math.sin(2 * math.pi * frequency * t)
            arr[i] = [wave * volume, wave * volume]
        
        # Fade in/out
        fade_frames = int(fade * sample_rate)
        arr[:fade_frames] *= np.linspace(0, 1, fade_frames)
        arr[-fade_frames:] *= np.linspace(1, 0, fade_frames)
        
        sound = pygame.sndarray.make_sound(arr.astype(np.int16))
        return sound
    
    def _generate_paddle_hit(self):
        """Короткий низкий звук для платформы"""
        # Басовый удар
        sound = self._generate_tone(220, 0.08, 0.4, 0.03)
        return sound
    
    def _generate_brick_hit(self):
        """Хрустящий звук для кирпича"""
        # Два тона подряд
        sound1 = self._generate_tone(800, 0.04, 0.6, 0.02)
        sound2 = self._generate_tone(1200, 0.04, 0.4, 0.02)
        
        # Объединяем
        frames1 = sound1.get_length() * 22050
        frames2 = sound2.get_length() * 22050
        total_frames = int(frames1 + frames2)
        arr = np.zeros((total_frames, 2))
        
        sound1_arr = pygame.sndarray.array(sound1)
        sound2_arr = pygame.sndarray.array(sound2)
        
        arr[:len(sound1_arr)] = sound1_arr
        arr[len(sound1_arr):] = sound2_arr
        
        return pygame.sndarray.make_sound(arr.astype(np.int16))
    
    def _generate_wall_hit(self):
        """Глухой отскок от стены"""
        sound = self._generate_tone(150, 0.06, 0.3, 0.04)
        return sound
    
    def _generate_game_over(self):
        """Длинный грустный звук"""
        sound = self._generate_tone(200, 1.2, 0.3, 0.1)
        # Добавляем спад частоты
        sample_rate = 22050
        frames = int(1.2 * sample_rate)
        arr = pygame.sndarray.array(sound)
        
        for i in range(frames//2, frames):
            t = float(i) / sample_rate
            fade = 1.0 - (i - frames//2) / (frames//2)
            arr[i] *= fade
        
        return pygame.sndarray.make_sound(arr.astype(np.int16))
    
    def _generate_power_up(self):
        """Восходящий звук бонуса"""
        sample_rate = 22050
        duration = 0.3
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            t = float(i) / sample_rate
            freq = 400 + 800 * (i / frames)  # от 400 до 1200 Hz
            wave = math.sin(2 * math.pi * freq * t)
            arr[i] = [wave * 0.5, wave * 0.5]
        
        return pygame.sndarray.make_sound(arr.astype(np.int16))
    
    def _generate_victory(self):
        """Праздничный звук"""
        sound1 = self._generate_tone(523, 0.15, 0.6)  # До
        sound2 = self._generate_tone(659, 0.15, 0.6)  # Ми
        sound3 = self._generate_tone(784, 0.2, 0.8)   # Соль
        
        frames1 = int(0.15 * 22050)
        frames2 = int(0.15 * 22050)
        frames3 = int(0.2 * 22050)
        total_frames = frames1 + frames2 + frames3
        
        arr = np.zeros((total_frames, 2))
        arr[:frames1] = pygame.sndarray.array(sound1)
        arr[frames1:frames1+frames2] = pygame.sndarray.array(sound2)

        arr[frames1+frames2:] = pygame.sndarray.array(sound3)
        
        return pygame.sndarray.make_sound(arr.astype(np.int16))
    
    def play(self, sound_name):
        """Проиграть звук"""
        if not self.muted and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass  # игнорируем ошибки
    
    def toggle_mute(self):
        """Вкл/выкл звук"""
        self.muted = not self.muted
    
    def set_volume(self, volume):
        """Установить громкость (0.0 - 1.0)"""
        pygame.mixer.music.set_volume(volume)
        for sound in self.sounds.values():
            sound.set_volume(volume)
