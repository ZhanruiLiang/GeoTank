import pygame
import math
from vec2d import Vec2d
__metaclass__ = type

Sprite = pygame.sprite.Sprite

class Transferable:
    def __init__(self):
        self.trans1 = []
        self.trans2 = []
    def to_string(self):
        pass
    def from_string(self, s):
        pass

class Shape:
    def __init__(self):
        self.pos = Vec2d(0, 0)
        self.vertices = []
        self.mat = []

    def __repr__(self):
        return "Shape(v0=%s, %s)" % (self.pos, self.vertices)

    def hittest(self, other):
        if self == other: return 0
        vs1 = self.vertices
        vs2 = other.vertices
        p0 = other.pos - self.pos
        # test if any point of vs1 is in shape2
        for v in vs2:
            if self._point_in(v + p0):
                return 1
        # test if any point of vs2 is in shape1
        for v in vs1:
            if other._point_in(v - p0):
                return 1
        return 0

    def rotate(self, angle):
        for v in self.vertices:
            v.rotate(angle)
        self._precalculate()

    def _point_in(self, p):
        # test if a point p in this shape, assume shape is convex
        x, y = p.x, p.y
        
        for A, B, C in self.mat:
            if x * A + y * B + C < 0:
                return 0
        return 1

    def AABB(self):
        vs = self.vertices
        x1 = min(v.x for v in vs)
        x2 = max(v.x for v in vs)
        y1 = min(v.y for v in vs)
        y2 = max(v.y for v in vs)
        return (x1, y1, x2, y2)

    def _precalculate(self):
        # precalculate the perp vectors
        vs = self.vertices
        n = len(vs)
        self.mat = []
        for i in xrange(n):
            v1 = vs[i]
            if i+1 >= n:
                v2 = vs[0]
            else:
                v2 = vs[i+1]
            A = v2.y - v1.y
            B = v1.x - v2.x
            C = v2.cross(v1)
            if C < 0:
                A, B, C = -A, -B, -C
            self.mat.append((A, B, C))

class ShapeRect(Shape):
    def __init__(self, w, h):
        super(ShapeRect, self).__init__()
        self.w = w
        self.h = h
        w /= 2.0
        h /= 2.0
        self.vertices = [Vec2d(v) for v in [(-w, -h), (w, -h), (w, h), (-w, h)]]
        self._precalculate()

class ShapeCircle(ShapeRect):
    def __init__(self, r):
        super(ShapeCircle, self).__init__(r, r)
        self.r = r

class GameObj(Sprite, Transferable):
    def __init__(self):
        super(GameObj, self).__init__()
        self.pos = Vec2d(0, 0)
        self.v = Vec2d(0, 0)
        self.shape = None
        self.active = 1
        self.dt = 0
        self.m = 5

    def hittest(self, other):
        return self.shape.hittest(other.shape)

    def __repr__(self):
        return '%s(p=%s, v=%s)' % (self.__class__.__name__, self.pos, self.v)

    def size(self):
        x1, y1, x2, y2 = self.shape.AABB()
        return (x2-x1, y2-y1)

    def move(self, dt):
        self.pos += dt * self.v
        self.shape.pos = self.pos
        self.dt += dt

    def apply(self):
        self.dt = 0

    def draw_shape(self, color):
        v0 = Vec2d(self.rect.size)/2
        img = pygame.Surface(self.image.get_size()).convert_alpha()
        img.fill((0, 0, 0, 0))
        pygame.draw.polygon(img, color, 
                [v0 + v for v in self.shape.vertices])
        self.image.blit(img, (0, 0))
        
