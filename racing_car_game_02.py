"""
Racing game v2
 v1 Creates Window (not working yet)
 v2 Adds class with variables for later
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

        # window
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Car Racing Game")

        # root file path for loading images
        self.root_path = str(Path(__file__).parent)

        self.initialize()


    def initialize(self):

        # used to restart game if crashed
        self.crashed = False

        # images
        self.carImg = pygame.image.load(self.root_path + "/img/car.png")

        # sets coordinates for car spawn ( car does not need to move so no speed)
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        # enemy_car (has speed moves toward player)
        self.enemy_car = pygame.image.load(self.root_path + "/img/enemy_car_1.png")
        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # Adds background image sets location (has speed to make it seem like car moving)
        self.bgImg = pygame.image.load(self.root_path + "/img/back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0
