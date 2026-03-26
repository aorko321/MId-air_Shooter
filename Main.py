#This is the main file that runs the game. 
# It imports the pygame class from the game module and creates an instance of it,
#  then calls the run method to show the game with the most recent updates.
from game import pygame

if __name__ == "__main__":
    game = pygame()
    game.run()