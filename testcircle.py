import pygame

from basic_class.component import *


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#FFFFFF'))


is_running = True
count = 0
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            circle = RadiusCircle(window_surface, 100, (100, 200))
            circle.show()
    # window_surface.blit(background, (0, 0))

    pygame.display.update()
