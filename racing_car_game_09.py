"""
Racing game v9
 v1 Creates Window (not working yet)
 v2 Adds class with variables for later
 v3 Blits car background and enemy cars, run class created spawns enemies within random x range
 v4 Adds car movement (left + right)
 v5 adds display message if car goes over boundaries, resets game
 v6 moved background stuff into function
 v7 checks for collision with enemy car (game restarting currently bugged) does not work unless key held down
 v8 fixes restart bug (was outside for loop) also fixes movement of car
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
        # RGB color values
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Car Racing Game")
        # Root file path for loading images
        self.root_path = str(Path(__file__).parent)

        self.initialize()

    def initialize(self):
        # Used to restart game if crashed
        self.crashed = False

        # Images
        self.carImg = pygame.image.load(self.root_path + "/img/car.png")

        # Sets coordinates for car spawn (car does not need to move so no speed)
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        # Enemy car (has speed moves toward player)
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
        # Speed background moves
        self.bg_speed = 3
        # Count of background tiles
        self.count = 0

    # Clearer variable names than v3
    def car(self, car_x_coordinate, car_y_coordinate):
        # Spawns car with correct x and y coordinates
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    # Function to run game
    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Race')
        self.run()

    def run(self):
        # Checks if car crashed
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

                # Checks for keydown
                if event.type == pygame.KEYDOWN:
                    # Checks for left keydown
                    if event.key == pygame.K_LEFT:
                        # Moves car to left
                        self.car_x_coordinate -= 50
                    # Checks for right keydown
                    if event.key == pygame.K_RIGHT:
                        # Moves car to right
                        self.car_x_coordinate += 50

            # Fills screen
            self.gameDisplay.fill(self.black)
            # Moved into function
            self.back_ground_road()

            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                # Random spawn location
                self.enemy_car_startx = random.randrange(310, 450)
                self.count += 1

            # Spawns enemy car within rand range
            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.gameDisplay.blit(self.enemy_car, (self.enemy_car_startx, self.enemy_car_starty))

            self.count += 1
            if self.count % 100 == 0:
                self.enemy_car_speed += 1
                self.bg_speed += 1

            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.enemy_car_startx < self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width \
                        or self.enemy_car_startx < self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True
                    highscore = self.read_highscore()
                    self.display_message("Game Over !!!", highscore)

            if self.car_x_coordinate < 310 or self.car_x_coordinate > 460:
                self.crashed = True
                highscore = self.read_highscore()
                self.display_message("Game Over !!!", highscore)

            pygame.display.update()
            # Sets tick speed
            self.clock.tick(60)

        # Resetting the game state and continuing the game loop
        self.run()

    def display_message(self, msg, highscore=None):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))

        if highscore is not None:
            highscore_font = pygame.font.SysFont("comicsansms", 36)
            highscore_text = highscore_font.render("Highscore: " + str(highscore), True, (255, 255, 255))
            self.gameDisplay.blit(highscore_text,
                                  (400 - highscore_text.get_width() // 2, 320 - highscore_text.get_height() // 2))

    def back_ground_road(self):
        # Moved into function
        self
