import pygame
import config
from pygame import display, font
from pygame.locals import *
import itertools

class Render:
    def __init__(self, game):
        self.game = game
        self.viewport = None
        display.init()
        font.init()
        self.fonter = font.SysFont('monospace', 16)

        self.screen = display.set_mode((config.screenW, config.screenH), DOUBLEBUF, 32)
        display.set_caption("Smash the tanks!")

    def draw(self):
        screen = self.screen
        game = self.game
        bullets = game.bullets
        tanks = game.tanks
        screen.fill((0xff, 0xff, 0xff, 0xff))
        for obj in itertools.chain(game.obstacles, tanks, bullets):
            obj.update()
            screen.blit(obj.image, obj.rect)
        self.draw_fps(game.fps)
        display.flip()
        
    def draw_fps(self, fps):
        sur = self.fonter.render('%.1f' % fps, True, (0, 0, 0, 0xff))
        sur1 = sur.copy()
        sur1.fill((0, 0xff, 0, 0x55))
        sur1.blit(sur, (0, 0))
        self.screen.blit(sur1, (0, 0))
