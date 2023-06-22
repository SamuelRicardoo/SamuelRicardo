import os
import pygame


pygame.mixer.init()  # Inicializa o mixer do Pygame

sound_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sound')

sound_score = os.path.join(sound_path, 'score_sound.wav')
SCORE_SOUND = pygame.mixer.Sound(sound_score)
SCORE_SOUND.set_volume(1)

sound_jump = os.path.join(sound_path, 'smw_jump.wav')
JUMP_SOUND = pygame.mixer.Sound(sound_jump)
JUMP_SOUND.set_volume(1)

sound_reset = os.path.join(sound_path, 'reset.wav')
RESET_SOUND = pygame.mixer.Sound(sound_reset)
RESET_SOUND.set_volume(1)

sound_start = os.path.join(sound_path, 'inicio.wav')
START_SOUND = pygame.mixer.Sound(sound_start)
START_SOUND.set_volume(1)

colison_sound = os.path.join(sound_path, 'colisao.wav')
COLISON_SOUND = pygame.mixer.Sound(colison_sound)
COLISON_SOUND.set_volume(1)
