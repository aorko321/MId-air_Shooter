from typing import Self

import pygame          # pyright: ignore[reportMissingImports]
import math
import sys

from constants import (                # pyright: ignore[reportMissingImports]
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

        self.font     = pygame.font.SysFont("Arial", 18, bold=True)
        self.med_font = pygame.font.SysFont("Arial", 26, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 56, bold=True)

        self.storage  = Storage(HIGH_SCORE_FILE)
        self.state    = STATE_MENU

        # Menu button rectangles (built once, reused every frame)
        btn_w, btn_h = 260, 52
        cx = SCREEN_WIDTH // 2 - btn_w // 2
        self.btn_start  = pygame.Rect(cx, 260, btn_w, btn_h)
        self.btn_scores = pygame.Rect(cx, 330, btn_w, btn_h)
        self.btn_quit   = pygame.Rect(cx, 400, btn_w, btn_h)

        # Name-entry state used on the game-over screen
        self.name_input    = ""
        self.name_saved    = False
        self.is_high_score = False

        self._init_gameplay()

    # ======== Gameplay reset =============
    def _init_gameplay(self):
        """Reset all in-game objects for a fresh run."""
        self.player              = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.bullets: list       = []
        self.enemies: list       = []
        self.enemy_spawn_timer   = ENEMY_SPAWN_RATE
        self.wave                = 1
        self.enemies_killed      = 0
    
    
     # ========== Main loop ==========
    def run(self):
        """Start and maintain the game loop until the window is closed."""
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self._handle_event(event)
            self._update(dt)
            self._draw()
    
    
     # ========== Event dispatching ==========
    def _handle_event(self, event: pygame.event.Event):
        if   self.state == STATE_MENU:       self._menu_event(event)
        elif self.state == STATE_PLAYING:    self._playing_event(event)
        elif self.state == STATE_GAME_OVER:  self._game_over_event(event)
        elif self.state == STATE_HIGHSCORES: self._highscores_event(event)

    def _menu_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit(); sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.btn_start.collidepoint(pos):
                self._init_gameplay()
                self.state = STATE_PLAYING
            elif self.btn_scores.collidepoint(pos):
                self.state = STATE_HIGHSCORES
            elif self.btn_quit.collidepoint(pos):
                pygame.quit(); sys.exit()

    def _playing_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = STATE_MENU
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            b = self.player.shoot()
            if b:
                self.bullets.append(b)
    
    def _game_over_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_ESCAPE:
                self.state = STATE_MENU
                return
            if key == pygame.K_RETURN and self.is_high_score and not self.name_saved:
                name = self.name_input.strip() or "Player"
                self.storage.save(name, self.player.score, self.wave)
                self.name_saved = True
                self.state = STATE_HIGHSCORES
                return
            if self.is_high_score and not self.name_saved:
                if key == pygame.K_BACKSPACE:
                    self.name_input = self.name_input[:-1]
                elif len(self.name_input) < 16 and event.unicode.isprintable():
                    self.name_input += event.unicode
            if key == pygame.K_r:
                self._init_gameplay()
                self.state = STATE_PLAYING
       
        def _highscores_event(self, event: pygame.event.Event):
         if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                self.state = STATE_MENU
   
   # =========== Update ===============
    def _update(self, dt: float):
        if self.state != STATE_PLAYING:
            return

        keys   = pygame.key.get_pressed()
        mx, my = pygame.mouse.get_pos()

        # Space bar fires as well as mouse click
        if keys[pygame.K_SPACE]:
            b = self.player.shoot()
            if b:
                self.bullets.append(b)

        self.player.update(keys, dt)
        self.player.aim_at(mx, my)

        # Enemy spawning — interval shrinks each wave
        self.enemy_spawn_timer -= dt
        if self.enemy_spawn_timer <= 0:
            self.enemies.append(Enemy(self.wave))
            self.enemy_spawn_timer = max(0.4, ENEMY_SPAWN_RATE - self.wave * 0.1)
            
         # Advance all bullets, remove off-screen ones
        for b in self.bullets[:]:
            b.update()
            if b.is_off_screen():
                self.bullets.remove(b)

        # Advance enemies and resolve collisions
        for enemy in self.enemies[:]:
            enemy.update(self.player.x, self.player.y, dt)

            # Shooter enemies fire back
            shot = enemy.shoot()
            if shot:
                self.bullets.append(shot)

         # Enemy body touches player
            if math.hypot(enemy.x - self.player.x,
                          enemy.y - self.player.y) < (enemy.radius + self.player.radius):
                dead = self.player.take_damage(20)
                self.enemies.remove(enemy)
                if dead:
                    self._on_death()
                continue
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
                continue

         # Player bullets hit enemy
            for b in self.bullets[:]:
                if b.owner != "player":
                    continue
                if math.hypot(b.x - enemy.x, b.y - enemy.y) < (b.radius + enemy.radius):
                    if enemy.take_damage(b.damage):
                        self.enemies.remove(enemy)
                        self.player.score   += 10
                        self.enemies_killed += 1
                        if self.enemies_killed % 10 == 0:
                            self.wave += 1
                    if b in self.bullets:
                        self.bullets.remove(b)
                    break

        # ====Enemy bullets hit player=======
        for b in self.bullets[:]:
            if b.owner != "enemy":
                continue
            if math.hypot(b.x - self.player.x,
                           b.y - self.player.y) < (b.radius + self.player.radius):
                dead = self.player.take_damage(b.damage)
                self.bullets.remove(b)
                if dead:
                    self._on_death()

    def _on_death(self):
        """Switch to game-over state and check for a new high score."""
        self.name_input    = ""
        self.name_saved    = False
        self.is_high_score = self.storage.is_high_score(self.player.score)
        self.state         = STATE_GAME_OVER

    # ========== Draw ==============
    def _draw(self):
        self.screen.fill(DARK_BG)
        self._draw_grid()

        if   self.state == STATE_MENU:       self._draw_menu()
        elif self.state == STATE_PLAYING:    self._draw_playing()
        elif self.state == STATE_GAME_OVER:  self._draw_game_over()
        elif self.state == STATE_HIGHSCORES: self._draw_highscores()

        pygame.display.flip()

    def _draw_grid(self):
        for gx in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(self.screen, GRID_COLOR, (gx, 0), (gx, SCREEN_HEIGHT))
        for gy in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(self.screen, GRID_COLOR, (0, gy), (SCREEN_WIDTH, gy))

    # =========== Menu ===================
    def _draw_menu(self):
        title = self.big_font.render("MID-AIR SHOOTER", True, CYAN)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

        sub = self.font.render("Survive as long as you can!", True, LIGHT_GRAY)
        self.screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 196))

        mouse_pos = pygame.mouse.get_pos()
        for rect, label, col in [
            (self.btn_start,  "START GAME",  GREEN),
            (self.btn_scores, "HIGH SCORES", GOLD),
            (self.btn_quit,   "QUIT", RED),
        ]:
            hovered = rect.collidepoint(mouse_pos)
            bg      = (50, 50, 80) if hovered else (30, 30, 55)
            border  = col if hovered else GRAY
            pygame.draw.rect(self.screen, bg,     rect, border_radius=8)
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=8)
            txt = self.med_font.render(label, True, col if hovered else LIGHT_GRAY)
            self.screen.blit(txt, (rect.centerx - txt.get_width()  // 2,
                                   rect.centery - txt.get_height() // 2))

        hint = self.font.render(
            "WASD / Arrows: Move  |  Mouse: Aim  |  LClick / Space: Shoot  |  ESC: Quit",
            True, GRAY)
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 30))

        # ── Playing ────────────────────────────────────────────────────────────────
    def _draw_playing(self):
        for b in self.bullets: b.draw(self.screen)
        for e in self.enemies: e.draw(self.screen)
        self.player.draw(self.screen)
        self.player.draw_hud(self.screen, self.font)

        wtxt = self.font.render(f"Wave: {self.wave}", True, LIGHT_GRAY)
        self.screen.blit(wtxt, (SCREEN_WIDTH // 2 - wtxt.get_width() // 2, 10))

        esc = self.font.render("ESC: Menu", True, GRAY)
        self.screen.blit(esc, (SCREEN_WIDTH - esc.get_width() - 10, SCREEN_HEIGHT - 22))

    # ======= Game Over ==============
    def _draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        cy = 80
        for text, font, color, gap in [
            ("GAME  OVER",                  self.big_font, RED,        70),
            (f"Score: {self.player.score}", self.med_font, WHITE,      40),
            (f"Wave reached: {self.wave}",  self.med_font, LIGHT_GRAY, 50),
        ]:
            s = font.render(text, True, color)
            self.screen.blit(s, (SCREEN_WIDTH // 2 - s.get_width() // 2, cy))
            cy += gap
        if self.is_high_score and not self.name_saved:
            hs = self.med_font.render("New High Score!", True, GOLD)
            self.screen.blit(hs, (SCREEN_WIDTH // 2 - hs.get_width() // 2, cy)); cy += 44

            prompt = self.font.render("Enter your name and press ENTER:", True, LIGHT_GRAY)
            self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, cy)); cy += 32

            box = pygame.Rect(SCREEN_WIDTH // 2 - 130, cy, 260, 38)
            pygame.draw.rect(self.screen, (40, 40, 70), box, border_radius=6)
            pygame.draw.rect(self.screen, CYAN, box, 2, border_radius=6)
            cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
            name_s = self.med_font.render(self.name_input + cursor, True, WHITE)
            self.screen.blit(name_s, (box.x + 10, box.y + 6))
            cy += 56
        elif self.name_saved:
            saved = self.med_font.render("Score saved!", True, GREEN)
            self.screen.blit(saved, (SCREEN_WIDTH // 2 - saved.get_width() // 2, cy)); cy += 44

        for label, color in [("R — Play again", GREEN), ("ESC — Main menu", GRAY)]:
            s = self.font.render(label, True, color)
            self.screen.blit(s, (SCREEN_WIDTH // 2 - s.get_width() // 2, cy)); cy += 28

    # ======= High Scores ==============
    def _draw_highscores(self):
        title = self.big_font.render("HIGH SCORES", True, GOLD)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))

        scores = self.storage.load()

        if not scores:
            msg = self.med_font.render("No scores yet — be the first!", True, LIGHT_GRAY)
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 220))
        else:
            headers = ["#", "Name", "Score", "Wave", "Date"]
            col_x   = [70, 140, 370, 480, 570]
            hy      = 120
            for hdr, cx in zip(headers, col_x):
                s = self.font.render(hdr, True, CYAN)
                self.screen.blit(s, (cx, hy))
            pygame.draw.line(self.screen, GRAY,
                             (60, hy + 24), (SCREEN_WIDTH - 60, hy + 24), 1)

            for i, entry in enumerate(scores):
                row_y    = hy + 36 + i * 34
                rank_col = GOLD if i == 0 else (LIGHT_GRAY if i < 3 else WHITE)
                for val, cx in zip(
                    [f"{i+1}.", entry["name"][:14],
                     str(entry["score"]), str(entry["wave"]), entry["date"]],
                    col_x
                ):
                    s = self.font.render(val, True, rank_col)
                    self.screen.blit(s, (cx, row_y))
    back = Self.font.render("ENTER / ESC / SPACE — back to menu", True, GRAY)
    Self.screen.blit(back, (SCREEN_WIDTH // 2 - back.get_width() // 2, SCREEN_HEIGHT - 30))









        











