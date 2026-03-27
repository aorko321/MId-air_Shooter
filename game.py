import pygame         # type: ignore
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









