MId-air_Shooter/
├── Main.py              ← entry point, run this
├── game.py              ← ShooterGame class (loop, states, rendering)
├── constants.py         ← all shared constants and colours
├── highscores.csv       ← sample data (auto-created on first run too)
└── entities/
    ├── __init__.py      ← exposes all classes cleanly
    ├── bullet.py        ← Bullet class (player + enemy projectiles)
    ├── enemy.py         ← Enemy class
    ├── player.py        ← Player class
    └── storage.py       ← Storage class (CSV read/write)




Main.py:
This is the main file that runs the game. It imports the pygame class from the game module and creates an instance of it, then calls the run method to show the game with the most recent updates.


game.py:
ShooterGame — top-level game controller.
Owns the main loop, state machine, update logic, and all rendering.
Imports entity classes from the entities/ package.
States-
    menu        – main menu with Start, High Scores, and Quit buttons
    playing     – active gameplay
    game_over   – death screen with optional name entry for the leaderboard
    highscores  – leaderboard table loaded live from CSV


constants.py:
All shared game constants and colour definitions.


__init__.py:
Exposes all entity classes so they can be imported directly from the package


player.py:
Player entity — handles movement, aiming, shooting, health, and HUD rendering.


