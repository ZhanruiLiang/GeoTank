from basic import Shape, ShapeRect
from render import Render
import pygame
from pygame.locals import *
from vec2d import Vec2d
from config import FPS

w, h = 100, 100
s1 = ShapeRect(w, h)
s2 = ShapeRect(w, h)
s1.pos = Vec2d(200, 200)
s2.pos = Vec2d(400, 200)

color1 = (0, 0xff, 0, 0xff)
color2 = (0xff, 0, 0, 0xff)
color = color1
class SimpleRender(Render):
    def draw(self):
        screen = self.screen
        screen.fill((0xff, 0xff, 0xff, 0xff))
        for s in [s1, s2]:
            pygame.draw.polygon(screen, color, [s.pos+v for v in s.vertices])
        pygame.display.flip()

render = SimpleRender(None)

def pause():
    raw_input('press to continue...')

def move(dp):
    if dp == 'rota':
        s1.rotate(15)
    elif dp == 'span':
        s1.vertices = [v * 1.1 for v in s1.vertices]
        s1._precalculate()
    else:
        dx, dy = dp
        dx *= 5
        dy *= 5
        s1.pos += (dx, dy)

keymap = { K_RETURN: 'span', K_SPACE: 'rota', K_LEFT: (-1, 0), K_RIGHT: (1, 0), K_UP: (0, -1), K_DOWN: (0, 1)}
timer = pygame.time.Clock()
timer.tick()
press = set()
while 1:
    for e in pygame.event.get():
        if e.type == QUIT:
            exit(0)
        elif e.type == KEYDOWN:
            press.add(e.key)
            if e.key == K_q:
                exit(0)
        elif e.type == KEYUP:
            press.remove(e.key)
    for key in press:
        if key in keymap:
            move(keymap[key])
    if s1.hittest(s2):
        color = color2
    else:
        color = color1
    print 's1', s1
    print 's2', s2
    # pause()
    render.draw()
    timer.tick(FPS)
