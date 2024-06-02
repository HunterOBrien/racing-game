"""
Racing game v1
 v1 Creates Window (not working yet)
"""

import random
import pygame
from time import sleep
from pathlib2 import Path



class CarRacing:
    def __init__(self):

        pygame.init()
        # Create Display Window
        self.display_width = 800
        self.display_height = 600
        # rgb colour values
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        # root file path for loading images
        self.root_path = str(Path(__file__).parent)

        self.initialize()