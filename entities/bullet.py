import math
import pygame
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_BULLET_SPEED, PLAYER_BULLET_RADIUS, ENEMY_BULLET_SPEED,  ENEMY_BULLET_RADIUS, YELLOW, RED,)

class Bullet:
    def __init__(self, x: float, y: float, angle: float, owner: str = "player"):
        self.x     = x
        self.y     = y
        self.angle = angle
        self.owner = owner

        if owner == "player":
            self.speed  = PLAYER_BULLET_SPEED
            self.radius = PLAYER_BULLET_RADIUS
            self.color  = YELLOW
            self.damage = 1
        else:
            self.speed  = ENEMY_BULLET_SPEED
            self.radius = ENEMY_BULLET_RADIUS
            self.color  = RED
            self.damage = 10

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def is_off_screen(self) -> bool:
        """Return True when the bullet has left the visible area."""
        margin = 50
        return (self.x < -margin or self.x > SCREEN_WIDTH  + margin or
                self.y < -margin or self.y > SCREEN_HEIGHT + margin)
