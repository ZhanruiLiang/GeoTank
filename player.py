from basic import Transferable, Vec2d
from tank import Tank
from pygame.locals import *

class Player(Transferable):
    Oprs = ['L', 'R', 'U', 'D', 'S', 'J', 'K']
    def __init__(self, name, tank):
        self.name = name
        self.viewport = None
        self.tank = tank
        self.score = 0

    def __repr__(self):
        return '%s(%s, s=%s)' % (self.__class__.__name__, self.name, self.score)

    def react(self, game):
        pass

class AIPlayer(Player):
    pass

class HumanPlayer(Player):
    MappingSet1 = {
            K_w: 'U',
            K_s: 'D',
            K_a: 'L',
            K_d: 'R',
            K_SPACE: 'S',
            K_q: 'J',
            K_e: 'K',
            }
    MappingSet2 = {
            K_i: 'U',
            K_k: 'D',
            K_j: 'L',
            K_l: 'R',
            K_RETURN: 'S',
            K_u: 'J',
            K_o: 'K',
            }
    def __init__(self, name, tank):
        super(HumanPlayer, self).__init__(name, tank)
        self.Mapping = {}
        self.pressed = set()

    def on_keydown(self, key):
        if key in self.Mapping:
            self.pressed.add(key)

    def on_keyup(self, key):
        if key in self.Mapping:
            self.pressed.remove(key)

    def react(self, game):
        s = ''.join(self.Mapping[key] for key in self.pressed)
        return s
