import os
import pygame
import tkinter as tk
from math import sin, radians, degrees, copysign
from pygame.math import Vector2


class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 30
        self.brake_deceleration = 30
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car Driving")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

        # New: Initialize vertical track offset
        self.track_offset_y = 0

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        track_path = os.path.join(current_dir, "track.png")
        track_path_02 = os.path.join(current_dir, "Track_02.png")
        car_image = pygame.image.load(image_path)
        original_track_image = pygame.image.load(track_path_02)
        car = Car(0, 0)

        ppu = 32

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if car.velocity.x < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 1 * dt
            elif pressed[pygame.K_DOWN]:
                if car.velocity.x > 0:
                    car.acceleration = -car.brake_deceleration
                else:
                    car.acceleration -= 1 * dt
            elif pressed[pygame.K_SPACE]:
                if abs(car.velocity.x) > dt * car.brake_deceleration:
                    car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
                else:
                    car.acceleration = -car.velocity.x / dt
            else:
                if abs(car.velocity.x) > dt * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity.x / dt
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

            if pressed[pygame.K_RIGHT]:
                car.steering -= 70 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 70 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

            # Logic
            car.update(dt)

            # Update the vertical track offset (move downwards)
            self.track_offset_y += 1

            track_x = (self.screen.get_width() - original_track_image.get_width()) / 2
            track_y = (self.screen.get_height() - original_track_image.get_height()) / 2

            if self.track_offset_y > self.screen.get_height():
                self.track_offset_y = 0

            # Drawing
            self.screen.fill((0, 0, 0))
            # using two instances off track tile one offset upwards by the tile size so there is constantly track
            # on screen at all times
            self.screen.blit(original_track_image, (track_x, -720 + self.track_offset_y))
            self.screen.blit(original_track_image, (track_x, track_y + self.track_offset_y))
            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
            pygame.display.flip()
            self.clock.tick(self.ticks)

        pygame.quit()


class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game Start")
        self.root.geometry("1280x720")

        self.label = tk.Label(self.root, text="Main Menu", font=("Helvetica", 24))
        self.label.pack(pady=50)

        self.root.bind("<Escape>", self.exit_menu)

    def exit_menu(self, event):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    game_start = MainMenu()
    game_start.run()
