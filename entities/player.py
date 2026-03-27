import pygame
import math

from entities.bullet import Bullet
from constants import ( SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER_SHOOT_COOLDOWN, PLAYER_RADIUS, PLAYER_MAX_HEALTH, WHITE, CYAN, GRAY, GREEN, ORANGE, RED,)

class Player:
    def __init__(self, x: float, y: float):
        self.x              = float(x)
        self.y              = float(y)
        self.angle          = 0.0
        self.radius         = PLAYER_RADIUS
        self.health         = PLAYER_MAX_HEALTH
        self.max_health     = PLAYER_MAX_HEALTH
        self.shoot_cooldown = 0.0
        self.score          = 0
        self.invincible     = 0.0   # seconds of i-frames remaining after taking damage


    def take_damage(self, damage: int) -> bool:
        """Apply damage if not invincible. Return True if the player is dead."""
        if self.invincible > 0:
            return False
        self.health    -= damage
        self.invincible = 0.5       # 0.5 s of invincibility after each hit
        return self.health <= 0

    def shoot(self):
        """Fire a Bullet from the ship nose if the cooldown has expired."""
        if self.shoot_cooldown <= 0:
            bx = self.x + math.cos(math.radians(self.angle)) * self.radius
            by = self.y + math.sin(math.radians(self.angle)) * self.radius
            self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
            return Bullet(bx, by, self.angle, owner="player")
        return None

    def update(self, keys, delta_time: float):
        """Process movement keys, clamp to screen bounds, and tick cooldowns."""
        vx = vy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:    vy = -PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  vy =  PLAYER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  vx = -PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: vx =  PLAYER_SPEED
        if vx and vy:           # normalise diagonal movement
            vx *= 0.7071
            vy *= 0.7071

        self.x = max(self.radius, min(SCREEN_WIDTH  - self.radius, self.x + vx))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y + vy))

        if self.shoot_cooldown > 0: self.shoot_cooldown -= delta_time
        if self.invincible     > 0: self.invincible     -= delta_time

    def aim_at(self, mx: int, my: int):
        """Rotate the ship to face the mouse cursor position."""
        self.angle = math.degrees(math.atan2(my - self.y, mx - self.x))


    def draw(self, surface: pygame.Surface):
        """Draw the player ship; flash white while invincible."""
        color = WHITE if (self.invincible > 0 and int(self.invincible * 10) % 2) else CYAN
        tip = (int(self.x + math.cos(math.radians(self.angle))       * self.radius * 1.5),
               int(self.y + math.sin(math.radians(self.angle))       * self.radius * 1.5))
        lpt = (int(self.x + math.cos(math.radians(self.angle + 130)) * self.radius),
               int(self.y + math.sin(math.radians(self.angle + 130)) * self.radius))
        rpt = (int(self.x + math.cos(math.radians(self.angle - 130)) * self.radius),
               int(self.y + math.sin(math.radians(self.angle - 130)) * self.radius))
        pygame.draw.polygon(surface, color, [tip, lpt, rpt])
        pygame.draw.polygon(surface, WHITE, [tip, lpt, rpt], 1)

    def draw_hud(self, surface: pygame.Surface, font: pygame.font.Font):
        """Render the HP bar and live score on screen."""
        # Health bar
        bw, bh  = 200, 18
        bx, by  = 10, 10
        ratio   = max(0.0, self.health / self.max_health)
        hw      = int(bw * ratio)
        bar_col = GREEN if ratio > 0.5 else (ORANGE if ratio > 0.25 else RED)
        pygame.draw.rect(surface, GRAY,    (bx, by, bw, bh))
        pygame.draw.rect(surface, bar_col, (bx, by, hw, bh))
        pygame.draw.rect(surface, WHITE,   (bx, by, bw, bh), 2)
        surface.blit(font.render(f"HP: {max(0, self.health)}", True, WHITE), (bx + 5, by + 1))

        # Score (top-right)
        stxt = font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(stxt, (SCREEN_WIDTH - stxt.get_width() - 10, 10))
