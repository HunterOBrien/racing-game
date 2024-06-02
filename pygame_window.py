"""
test pygame window
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window dimensions
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)

# Set the window title
pygame.display.set_caption('Basic Pygame Window')

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (RGB tuple)
    screen.fill((0, 0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
