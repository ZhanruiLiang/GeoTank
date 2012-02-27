from basic import *
import config
import pygame
from pygame.locals import *
import math

class Obstacle(GameObj):
    def __init__(self, shape, ssize, pos=None):
        """ size is the surface size """
        super(Obstacle, self).__init__()
        self.pos = pos or Vec2d(0, 0)
        self.shape = shape
        # image
        self.image = pygame.Surface(ssize).convert_alpha()
        self.color = pygame.Color("black")
        self.ssize = ssize
        self.rect = pygame.Rect((0, 0), self.ssize)


    def redraw(self):
        self.image.fill((0, 0, 0, 0))
        v0 = Vec2d(self.rect.size)/2
        pygame.draw.polygon(self.image, self.color, 
                [v0 + v for v in self.shape.vertices])

    def update(self):
        self.rect.center = self.pos

class ObstacleBlock(Obstacle):
    def __init__(self, ssize, pos, color=None):
        shape = ShapeRect(*ssize)
        super(ObstacleBlock, self).__init__(shape, ssize, pos)
        self.pos = pos
        if color:
            self.color = color
        self.redraw()
        self.m = 1000000000

