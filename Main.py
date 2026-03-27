# HEAD  
#This is the main file that runs the game. 
# It imports the pygame class from the game module and creates an instance of it,
#  then calls the run method to show the game with the most recent updates.

from game import pygame

import game as game_
if __name__ == "__main__":
    game = game_.ShooterGame()
    game.run()
    