from game import Game
from render import Render
from tank import Tank
from obstacle import ObstacleBlock
import pygame
from pygame.locals import *
from player import AIPlayer, HumanPlayer
import config
from vec2d import Vec2d

def pause():
    raw_input('paused...')


def main():
    game = Game()
    render = Render(game)
    timer = pygame.time.Clock()
    players = []

    # add player
    tank = Tank()
    tank.pos = Vec2d(200, 200)
    p1 = HumanPlayer('Ray', tank)
    p1.Mapping = HumanPlayer.MappingSet1

    tank2 = Tank()
    tank2.pos = Vec2d(400, 200)
    p2 = HumanPlayer('Pest', tank2)
    p2.Mapping = HumanPlayer.MappingSet2

    players += [p1, p2]
    for p in players:
        game.add_player(p)

    # add obstacle
    for pos, col in zip([(100, 400), (500, 400)], ['blue', 'red']):
        obs = ObstacleBlock((100, 100), pos,  Color(col))
        game.obstacles.append(obs)

    timer.tick()
    FPS = config.FPS
    dt = 1.0/FPS
    while 1:
        for e in pygame.event.get():
            if e.type == QUIT:
                return
            elif e.type == KEYDOWN:
                for p in players:
                    p.on_keydown(e.key)
                if e.key == K_b or (e.mod & KMOD_LCTRL) and e.key == K_q:
                    return
            elif e.type == KEYUP:
                for p in players:
                    p.on_keyup(e.key)
        game.loop(dt)
        render.draw()
        game.fps = timer.tick(FPS)

if __name__ == '__main__':
    main()
