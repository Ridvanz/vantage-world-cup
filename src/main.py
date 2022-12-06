
#%%

import pygame, sys
import random
import settings as s
import entities as e
from controller import GameController

def main():
                                                        # Get all game states
    controller = GameController()                        # Load game controller
    controller.run()                                                                # Run this bad boy!


if __name__ == '__main__':
    main()

# P1 = e.Player()
# E1 = e.Enemy()
 
# pygame.quit()
# sys.exit()  !