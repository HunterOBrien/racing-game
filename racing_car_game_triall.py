"""
Racing game v9
 v1 Creates Window (not working yet)
 v2 Adds class with variables for later
 v3 Blits car background and enemy cars, run class created spawns enemies within random x range
 v4 Adds car movement (left + right)
 v5 adds display message if car goes over boundaries, resets game
 v6 moved background stuff into function
 v7 checks for collision with enemy car (game restarting currently bugged) does not work unless key held down
 v8 fixes bug and car speed
 v9 (final) display highscore (from .txt file) and current score
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
        self.count = 0

    # clearer variable names than v3
    def car(self, car_x_coordinate, car_y_coordinate):
        # spawns car with correct x and y coordinates
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    # function to run game
    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        self.run()

    def run(self):
        # checks if car crashed
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

                # checks for keydown
                if event.type == pygame.KEYDOWN:
                    # checks for left keydown
                    if event.key == pygame.K_LEFT:
                        # moves car to left
                        self.car_x_coordinate -= 50
                    # checks for left keydown
                    if event.key == pygame.K_RIGHT:
                        # moves car to right
                        self.car_x_coordinate += 50

            # fills screen
            self.gameDisplay.fill(self.black)
            # moved into function
            self.back_ground_road()

            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height

                # random spawn location
                self.enemy_car_startx = random.randrange(310, 450)
                self.count += 1

            # spawns enemy car within rand range
            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.gameDisplay.blit(self.enemy_car, (self.enemy_car_startx, self.enemy_car_starty))

            self.highscore(self.count)
            self.count += 1
            # increases speed overtime
            if self.count % 100 == 0:
                self.enemy_car_speed = random.randint(3, 10)
                print(self.enemy_car_speed)
                # self.bg_speed += 1

            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.enemy_car_startx < self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width \
                        or self.enemy_car_startx < self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True
                    self.display_message("Game Over !!!")

            if self.car_x_coordinate < 310 or self.car_x_coordinate > 460:
                self.crashed = True
                self.display_message("Game Over !!!")

            pygame.display.update()
            # sets tick speed
            self.clock.tick(60)

        pygame.quit()
        quit()

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        pygame.display.update()
        self.clock.tick(60)
        sleep(1)
        car_racing.initialize()
        car_racing.racing_window()

    def back_ground_road(self):
        # moved into function
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def highscore(self, count):
        # Convert count to string
        score_str = str(count)

        # Read highscore from the text file
        try:
            with open("highscore.txt", "r") as file:
                highscore_str = file.read()
        except FileNotFoundError:
            # If highscore file doesn't exist, set highscore to 0
            highscore_str = "0"

        # Convert highscore to integer
        highscore = int(highscore_str)

        # Update highscore if current score is higher
        if count > highscore:
            highscore = count
            # Write new highscore to the file
            with open("highscore.txt", "w") as file:
                file.write(str(highscore))

        # current score
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

        # Render the highscore on the screen underneath the current score
        highscore_text = font.render("Highscore : " + str(highscore), True, self.white)
        self.gameDisplay.blit(highscore_text, (0, 30))


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.run()
