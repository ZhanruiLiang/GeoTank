import pygame
from pygame.locals import *
display = pygame.display
draw = pygame.draw

display.init()
screen = display.set_mode((400, 400), 0, 32)
def clear():
    screen.fill((255, 255, 255))
    display.flip()
pg = pygame
