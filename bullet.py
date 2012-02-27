from basic import *
from pygame import draw, Surface, Rect
import config

Size = (20, 20)
class Bullet(GameObj):
    def __init__(self):
        super(Bullet, self).__init__()
        self.r = config.bulletR
        self.m = config.bulletM
        self.shape = ShapeCircle(self.r)
        self.t = 0
        self.length = 0
        self.I = 0
        self.damage = 0
        # image
        self.image = Surface(Size).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = Rect((0, 0), Size)
        draw.circle(self.image, (0, 0, 0, 0xff), self.rect.center, self.r)

    def size(self):
        return (self.r*2, self.r*2)

    def apply(self):
        self.length += self.v.length * self.dt
        self.dt = 0

    def update(self):
        self.rect.center = self.pos

    def boom(self):
        self.I = 5000000
        self.active = 0
        #TODO return something, maybe an explode

