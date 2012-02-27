from basic import *
import config
import pygame
from pygame.locals import *
import math
from bullet import Bullet

acce1 = config.tankAcce1
acceF = config.acceF
acce2 = config.tankAcce2
draw = pygame.draw

def pos(v):
    return int(v.x), int(v.y)

class Tank(GameObj):
    def __init__(self):
        super(Tank, self).__init__()
        self.w = config.tankW
        self.h = config.tankH
        self.shape = ShapeRect(self.w, self.h)
        self.m = config.tankM
        self.angle1 = self.angle2 = 90
        self.health = 100
        self.maxv1 = config.tankMaxV
        self.maxv2 = config.tankMaxV / 1.5
        self.shootReady = 1
        self._recharge = 0
        self.engineSide = 0
        # image
        self.color = (0, 0, 0xff, 0xff)
        self.color1 = (0, 0xaa, 0xff, 0xff)
        l = self.h * 2.2
        self.image = pygame.Surface((l, l)).convert_alpha()
        self.rect = Rect((0, 0), (l, l))
        self._need_redraw = 1

    def rotate1(self, angle):
        self.angle1 += angle
        self.angle1 %= 360
        self.shape.rotate(angle)
        self.v.rotate(angle)

        self.angle2 += angle
        self.angle2 %= 360

        self._need_redraw = 1

    def rotate2(self, angle):
        self.angle2 += angle
        self.angle2 %= 360
        self._need_redraw = 1

    def _get_gun_pos(self):
        p0 = self.pos
        return p0 + Vec2d(self.h*1.1, 0).rotated(self.angle2)

    def shoot(self):
        bullet = Bullet()
        bullet.pos = self._get_gun_pos()
        bullet.v = Vec2d(config.bulletV, 0).rotated(self.angle2)
        bullet.damage = config.bulletDamage
        self.shootReady = 0
        self._recharge = config.tankRecharge
        return bullet

    def __repr__(self):
        return super(Tank, self).__repr__()[:-1] + (', hp=%s, active=%s)' % (self.health, self.active))

    def apply(self):
        # apply the movement, change v
        dt = self.dt
        v = self.v
        vv = v.normalized()
        vt = Vec2d(1, 0).rotated(self.angle1)

        v += vt * self.engineSide * acce1 * dt
        l = v.length
        if l > 0 and l > acceF *dt:
            v -= vv * acceF * dt
        else:
            v = Vec2d(0, 0)

        if self.engineSide > 0 and v.length > self.maxv1:
            v = v.normalized() * self.maxv1
        if self.engineSide < 0 and v.length > self.maxv2:
            v = v.normalized() * self.maxv2
        self.v = v

        if self._recharge > 0:
            self._recharge -= dt
        else:
            self.shootReady = 1

        self.dt = 0

    def update(self):
        self.rect.center = self.pos
        # update image
        if not self._need_redraw:
            return
        self._need_redraw = 0
        w, h = self.rect.size
        p0 = Vec2d(w/2, h/2)
        # clear
        self.image.fill((0, 0, 0, 0))
        # draw part 1
        vs = self.shape.vertices
        draw.polygon(self.image, (0x55, 0, 0, 0xff), [tuple(p0 + v) for v in vs])
        p1 = p0 + Vec2d(self.w/4.0, 0).rotated(self.angle1)
        draw.polygon(self.image, self.color, [tuple(p1+v*0.7) for v in vs])
        # draw part 2
        p = Vec2d(self.h, 0).rotated(self.angle2)
        draw.polygon(self.image, self.color1, [tuple(p0 + v.rotated(self.angle2-self.angle1)*0.5) for v in vs])
        draw.line(self.image, (0, 0, 0, 0xff), p0-p/4, p0+p, 3)
        # debug draw shape
        # self.draw_shape()
