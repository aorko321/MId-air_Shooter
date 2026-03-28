SCREEN_WIDTH  = 1366
SCREEN_HEIGHT = 768
SCREEN_TITLE  = "M!d-air Shooter"
FPS           = 60

PLAYER_SPEED          = 5
PLAYER_SHOOT_COOLDOWN = 0.22
PLAYER_RADIUS         = 15
PLAYER_MAX_HEALTH     = 100

PLAYER_BULLET_SPEED  = 10
PLAYER_BULLET_RADIUS = 5
ENEMY_BULLET_SPEED   = 4
ENEMY_BULLET_RADIUS  = 5

ENEMY_SPAWN_RATE  = 2.0
ENEMY_SPEED_MIN   = 1.0
ENEMY_SPEED_MAX   = 2.5
ENEMY_RADIUS      = 15
ENEMY_TYPES       = ["Normal", "Shooter"]
ENEMY_SHOOT_CD    = 1.5

HIGH_SCORE_FILE = "highscores.csv"
MAX_SCORES      = 10
CSV_FIELDS      = ["name", "score", "wave", "date"]

STATE_MENU       = "menu"
STATE_PLAYING    = "playing"
STATE_GAME_OVER  = "game_over"
STATE_HIGHSCORES = "highscores"

WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
RED        = (220,  50,  50)
GREEN      = ( 50, 200,  50)
ORANGE     = (255, 140,   0)
CYAN       = (  0, 200, 220)
YELLOW     = (255, 220,   0)
PURPLE     = (160,  32, 240)
DARK_BG    = ( 20,  20,  40)
GRID_COLOR = ( 30,  30,  50)
GRAY       = (100, 100, 100)
LIGHT_GRAY = (180, 180, 180)
GOLD       = (255, 215,   0)
