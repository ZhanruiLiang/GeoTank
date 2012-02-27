from game import *
from player import Player
from render import Render
import pygame

__metaclass__ = type

class Client:
    def __init__(self):
        self.game = Game()
        self.render = Render(self.game)
        self.player = None
        self.socket = None

    def connect(self, addr):
        pass

    def ask_join(self):
        pass

    def ask_quit(self):
        pass

    def update(self):
        pass

    def mainloop(self):
        timer = pygame.time.Clock()
        while 1:
            timer.tick()

if __name__ == '__main__':
    client = Client()
    try:
        client.mainloop()
    except KeyboardInterrupt:
        pass
