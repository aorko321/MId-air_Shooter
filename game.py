import pygame
import math
import sys

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, FPS,
    ENEMY_SPAWN_RATE, HIGH_SCORE_FILE,
    STATE_MENU, STATE_PLAYING, STATE_GAME_OVER, STATE_HIGHSCORES,
    WHITE, RED, GREEN, CYAN, YELLOW, GRAY, LIGHT_GRAY, GOLD,
    DARK_BG, GRID_COLOR, ORANGE,
)

from entities import Player, Enemy, Bullet, Storage

class ShooterGame:
    def __init__(self):
        pygame.init()
        self.screen   = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)
        self.clock    = pygame.time.Clock()