import pygame
from const import *
from ball import Ball


class SoundManager:
    """
    Manage all the sound effects for the game.
    """
    pygame.mixer.init()

    # Load sounds
    START_SOUND = pygame.mixer.Sound(START)
    POWERUP_SOUND = pygame.mixer.Sound(POWERUP)
    EXPLOSION_SOUND = pygame.mixer.Sound(EXPLOSION)
    SHOOTING_SOUND = pygame.mixer.Sound(SHOOT)

    @staticmethod
    def play_start_sound():
        """Play the start sound effect."""
        SoundManager.START_SOUND.play()

    @staticmethod
    def play_powerup_sound():
        """Play the power-up sound effect."""
        SoundManager.POWERUP_SOUND.play()

    @staticmethod
    def play_explosion_sound():
        """Play the explosion sound effect."""
        SoundManager.EXPLOSION_SOUND.play()

    @staticmethod
    def play_shooting_sound():
        """Play the shooting sound effect."""
        SoundManager.SHOOTING_SOUND.play()