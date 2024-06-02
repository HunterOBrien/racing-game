"""
Racing game v3
 v1 Creates Window (not working yet)
 v2 Adds class with variables for later
 v3 Blits car background and enemy cars, run class created spawns enemies within random x range
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
        # speed background moves
        self.bg_speed = 3
        # count of background tiles
        self.count = 0

    def car(self, x, y):
        # spawns car with correct x and y coords
        self.gameDisplay.blit(self.carImg, (x, y))

    def run(self):
        # checks if car crashed
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

            # fills screen
            self.gameDisplay.fill(self.black)

            self.bg_y1 += self.bg_speed
            self.bg_y2 += self.bg_speed

            self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
            self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

            if self.bg_y1 >= self.display_height:
                self.bg_y1 = -600

            if self.bg_y2 >= self.display_height:
                self.bg_y2 = -600

            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height

                # random spawn location
                self.enemy_car_startx = random.randrange(310, 450)
                self.count += 1

            # spawns enemy car within rand range
            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.gameDisplay.blit(self.enemy_car, (self.enemy_car_startx, self.enemy_car_starty))

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        quit()


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.run()
