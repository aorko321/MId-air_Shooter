import math
import random
import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    ENEMY_SPEED_MIN, ENEMY_SPEED_MAX, ENEMY_RADIUS,
    ENEMY_TYPES, ENEMY_SHOOT_CD,
    RED, PURPLE, GREEN, GRAY, WHITE,
)
from entities.bullet import Bullet


class Enemy:
    """An enemy that spawns from a random screen edge and hunts the player.

    Parameters
    ----------
    wave : current wave number — scales speed and health.
    """

    def __init__(self, wave: int = 1):
        self._spawn_on_edge()
        speed_bonus        = min(wave * 0.15, 1.5)
        self.enemy_type    = random.choice(ENEMY_TYPES)
        self.speed         = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX) + speed_bonus
        self.angle         = 0.0
        self.radius        = ENEMY_RADIUS
        hp                 = 3 + (wave // 3)
        self.health        = hp
        self.max_health    = hp
        self.shoot_cooldown = ENEMY_SHOOT_CD

    # ── Spawn helpers ──────────────────────────────────────────────────────────
    def _spawn_on_edge(self):
        """Place the enemy just outside a randomly chosen screen edge."""
        side = random.choice(["top", "right", "bottom", "left"])
        if side == "top":
            self.x, self.y = random.uniform(0, SCREEN_WIDTH), -20.0
        elif side == "right":
            self.x, self.y = float(SCREEN_WIDTH + 20), random.uniform(0, SCREEN_HEIGHT)
        elif side == "bottom":
            self.x, self.y = random.uniform(0, SCREEN_WIDTH), float(SCREEN_HEIGHT + 20)
        else:
            self.x, self.y = -20.0, random.uniform(0, SCREEN_HEIGHT)

    # ── Public interface ───────────────────────────────────────────────────────
    def take_damage(self, damage: int) -> bool:
        """Reduce health by damage. Return True if the enemy is now dead."""
        self.health -= damage
        return self.health <= 0

    def update(self, player_x: float, player_y: float, delta_time: float):
        """Move toward the player and tick the shoot cooldown."""
        dx = player_x - self.x
        dy = player_y - self.y
        self.angle = math.degrees(math.atan2(dy, dx))
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        if self.enemy_type == "Shooter":
            self.shoot_cooldown -= delta_time

    def shoot(self):
        """Return a Bullet aimed at the player if the Shooter is ready, else None."""
        if self.enemy_type == "Shooter" and self.shoot_cooldown <= 0:
            bx = self.x + math.cos(math.radians(self.angle)) * self.radius
            by = self.y + math.sin(math.radians(self.angle)) * self.radius
            self.shoot_cooldown = ENEMY_SHOOT_CD
            return Bullet(bx, by, self.angle, owner="enemy")
        return None

    def draw(self, surface: pygame.Surface):
        color = RED if self.enemy_type == "Shooter" else PURPLE
        tip = (int(self.x + math.cos(math.radians(self.angle))       * self.radius * 1.5),
               int(self.y + math.sin(math.radians(self.angle))       * self.radius * 1.5))
        lpt = (int(self.x + math.cos(math.radians(self.angle + 130)) * self.radius),
               int(self.y + math.sin(math.radians(self.angle + 130)) * self.radius))
        rpt = (int(self.x + math.cos(math.radians(self.angle - 130)) * self.radius),
               int(self.y + math.sin(math.radians(self.angle - 130)) * self.radius))
        pygame.draw.polygon(surface, color, [tip, lpt, rpt])
        pygame.draw.polygon(surface, WHITE, [tip, lpt, rpt], 1)
        self._draw_health_bar(surface)

    def _draw_health_bar(self, surface: pygame.Surface):
        bar_w = 40
        bar_h = 5
        hw    = int(bar_w * self.health / self.max_health)
        bx    = int(self.x - bar_w // 2)
        by    = int(self.y + self.radius + 6)
        pygame.draw.rect(surface, GRAY,  (bx, by, bar_w, bar_h))
        pygame.draw.rect(surface, GREEN, (bx, by, hw,    bar_h))
        pygame.draw.rect(surface, WHITE, (bx, by, bar_w, bar_h), 1)

    def is_off_screen(self) -> bool:
        return (self.x < -60 or self.x > SCREEN_WIDTH  + 60 or
                self.y < -60 or self.y > SCREEN_HEIGHT + 60)

