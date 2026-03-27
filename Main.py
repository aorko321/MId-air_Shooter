# HEAD  
#This is the main file that runs the game. 
# It imports the pygame class from the game module and creates an instance of it,
#  then calls the run method to show the game with the most recent updates.

from game import pygame

from game import ShooterGame
93a32f5551c6b56fbcd6e3c369af6294b166cab7 # type: ignore

if __name__ == "__main__":
    game = ShooterGame()
    game.run()
    